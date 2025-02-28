import pygame
import random
from constants import *
from images import load_game_images
import math

class Hero:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.speed = HERO_SPEED
        self.score = 0
        self.image = image
        self.direction = RIGHT  # Current facing direction
        self.animation_frame = 0
        
    def move(self, dx, dy, walls):
        # Update facing direction
        if dx != 0 or dy != 0:
            if dx > 0:
                self.direction = RIGHT
            elif dx < 0:
                self.direction = LEFT
            elif dy > 0:
                self.direction = DOWN
            elif dy < 0:
                self.direction = UP
            
            # Update animation
            self.animation_frame = (self.animation_frame + 1) % 30
        
        # Move horizontally
        new_x = self.x + (dx * self.speed)
        new_rect = pygame.Rect(new_x, self.y, HERO_SIZE, HERO_SIZE)
        can_move = True
        for wall in walls:
            if new_rect.colliderect(wall.rect):
                can_move = False
                break
        if can_move:
            self.x = new_x

        # Move vertically
        new_y = self.y + (dy * self.speed)
        new_rect = pygame.Rect(self.x, new_y, HERO_SIZE, HERO_SIZE)
        can_move = True
        for wall in walls:
            if new_rect.colliderect(wall.rect):
                can_move = False
                break
        if can_move:
            self.y = new_y

    def collect_bonus(self, bonus_blocks):
        hero_rect = pygame.Rect(self.x, self.y, HERO_SIZE, HERO_SIZE)
        for bonus in bonus_blocks:
            if not bonus.collected and hero_rect.colliderect(bonus.rect):
                bonus.collected = True
                self.score += BONUS_POINTS
                return True
        return False

    def draw(self, screen):
        # Create a rotated copy of the image based on direction
        angle = {
            RIGHT: 0,
            LEFT: 180,
            UP: 90,
            DOWN: 270
        }.get(self.direction, 0)
        
        # Animate mouth opening/closing
        if self.animation_frame < 15:  # Open mouth more
            scaled_size = int(HERO_SIZE * 0.8)  # Make slightly smaller for animation
            pos_offset = (HERO_SIZE - scaled_size) // 2
            rotated_image = pygame.transform.scale(self.image, (scaled_size, scaled_size))
        else:  # Normal size
            rotated_image = self.image
            pos_offset = 0
            
        rotated_image = pygame.transform.rotate(rotated_image, angle)
        screen.blit(rotated_image, (self.x + pos_offset, self.y + pos_offset))


class Enemy:
    def __init__(self, x, y, image, is_red=False):
        self.x = float(x)
        self.y = float(y)
        self.speed = ENEMY_SPEED
        self.image = image
        self.is_red = is_red
        self.direction = (0, 0)
        self.animation_frame = 0
        self.state = 'chase'
        self.state_timer = 0

    def move(self, walls, hero):
        self.animation_frame = (self.animation_frame + 1) % 20
        
        # Update state every 5 seconds
        self.state_timer += 1
        if self.state_timer >= 300:
            self.state = 'scatter' if self.state == 'chase' else 'chase'
            self.state_timer = 0

        # Determine target position based on state
        if self.state == 'chase':
            target_x = hero.x
            target_y = hero.y
        else:  # scatter mode
            if self.is_red:
                target_x, target_y = SCREEN_WIDTH - CELL_SIZE, 0
            else:
                target_x, target_y = 0, SCREEN_HEIGHT - CELL_SIZE

        # Calculate direction to target
        dx = target_x - self.x
        dy = target_y - self.y

        # Try to move towards target
        new_direction = [0, 0]
        if abs(dx) > abs(dy):
            # Try horizontal movement first
            new_direction[0] = 1 if dx > 0 else -1
            if not self.check_collision(self.x + new_direction[0] * self.speed, self.y, walls):
                self.x += new_direction[0] * self.speed
            else:
                # If horizontal blocked, try vertical
                new_direction[0] = 0
                new_direction[1] = 1 if dy > 0 else -1
                if not self.check_collision(self.x, self.y + new_direction[1] * self.speed, walls):
                    self.y += new_direction[1] * self.speed
        else:
            # Try vertical movement first
            new_direction[1] = 1 if dy > 0 else -1
            if not self.check_collision(self.x, self.y + new_direction[1] * self.speed, walls):
                self.y += new_direction[1] * self.speed
            else:
                # If vertical blocked, try horizontal
                new_direction[1] = 0
                new_direction[0] = 1 if dx > 0 else -1
                if not self.check_collision(self.x + new_direction[0] * self.speed, self.y, walls):
                    self.x += new_direction[0] * self.speed

        self.direction = tuple(new_direction)

    def check_collision(self, x, y, walls):
        """Check if moving to position (x, y) would result in a collision."""
        test_rect = pygame.Rect(x, y, ENEMY_SIZE, ENEMY_SIZE)
        for wall in walls:
            if test_rect.colliderect(wall.rect):
                return True
        return False

    def draw(self, screen):
        # Add subtle floating animation
        offset = math.sin(self.animation_frame * 0.3) * 1
        screen.blit(self.image, (int(self.x), int(self.y + offset)))


class Wall:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)


class BonusBlock:
    def __init__(self, x, y):
        # Center the bonus point in the cell and keep position fixed
        self.x = x + (CELL_SIZE - BONUS_SIZE) // 2
        self.y = y + (CELL_SIZE - BONUS_SIZE) // 2
        self.collected = False
        self.rect = pygame.Rect(self.x, self.y, BONUS_SIZE, BONUS_SIZE)
        self.animation_timer = 0
        self.base_size = BONUS_SIZE
        self.position = (self.x + self.base_size // 2, self.y + self.base_size // 2)  # Center position

    def draw(self, screen):
        if not self.collected:
            # Create gentle pulsing animation
            self.animation_timer = (self.animation_timer + 1) % 120
            pulse = abs(math.sin(self.animation_timer * 0.05))  # Slower, gentler pulse
            
            # Calculate color with minimal variation
            r = int(255)
            g = int(182 + (30 * pulse))  # Reduced color variation
            b = int(255)
            
            # Draw the main circle with fixed position
            pygame.draw.circle(screen, (r, g, b), self.position, self.base_size // 2)
            
            # Add subtle glow
            glow_surface = pygame.Surface((self.base_size + 4, self.base_size + 4), pygame.SRCALPHA)
            glow_alpha = int(64 * pulse)  # Pulsing transparency
            pygame.draw.circle(glow_surface, (r, g, b, glow_alpha), 
                            (self.base_size // 2 + 2, self.base_size // 2 + 2), 
                            self.base_size // 2 + 1)
            screen.blit(glow_surface, (self.x - 2, self.y - 2))


def create_level_objects():
    walls = []
    bonus_blocks = []
    for row in range(len(LEVEL_MAP)):
        for col in range(len(LEVEL_MAP[0])):
            cell = LEVEL_MAP[row][col]
            if cell == 1:
                walls.append(Wall(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif cell == 2:
                bonus_blocks.append(BonusBlock(col * CELL_SIZE, row * CELL_SIZE))
    return walls, bonus_blocks


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pacman Game")
    clock = pygame.time.Clock()

    # Load images
    images = load_game_images(HERO_SIZE, ENEMY_SIZE)

    # Create level objects
    walls, bonus_blocks = create_level_objects()

    # Create game objects with better starting positions
    hero = Hero(50, 50, images['pacman'])
    enemies = [
        Enemy(SCREEN_WIDTH - 100, 50, images['ghost_red'], True),  # Red ghost
        Enemy(50, SCREEN_HEIGHT - 100, images['ghost_orange'], False)  # Orange ghost
    ]

    running = True
    game_over = False
    score = 0
    level = 1
    level_complete = False
    level_transition_timer = 0

    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r and game_over:
                    # Reset game
                    hero = Hero(50, 50, images['pacman'])
                    enemies = [
                        Enemy(SCREEN_WIDTH - 100, 50, images['ghost_red'], True),
                        Enemy(50, SCREEN_HEIGHT - 100, images['ghost_orange'], False)
                    ]
                    for bonus in bonus_blocks:
                        bonus.collected = False
                    game_over = False
                    score = 0
                    level = 1
                    level_complete = False
                    level_transition_timer = 0

        if not game_over:
            if level_complete:
                # Show level complete message for 2 seconds
                level_transition_timer += 1
                if level_transition_timer > 120:  # 2 seconds at 60 FPS
                    # Reset for next level
                    level += 1
                    hero = Hero(50, 50, images['pacman'])
                    enemies = [
                        Enemy(SCREEN_WIDTH - 100, 50, images['ghost_red'], True),
                        Enemy(50, SCREEN_HEIGHT - 100, images['ghost_orange'], False)
                    ]
                    for bonus in bonus_blocks:
                        bonus.collected = False
                    level_complete = False
                    level_transition_timer = 0
            else:
                # Speed up enemies based on level (with smaller increments)
                for enemy in enemies:
                    enemy.speed = ENEMY_SPEED + (level * 0.15)  # Even smaller speed increase

                # Handle keyboard input for movement
                dx = 0
                dy = 0
                keys = pygame.key.get_pressed()
                
                if keys[pygame.K_LEFT]:
                    dx = -1
                if keys[pygame.K_RIGHT]:
                    dx = 1
                if keys[pygame.K_UP]:
                    dy = -1
                if keys[pygame.K_DOWN]:
                    dy = 1

                # Move hero
                hero.move(dx, dy, walls)
                
                # Check for bonus collection
                if hero.collect_bonus(bonus_blocks):
                    score += BONUS_POINTS
                    
                    # Check if all bonus blocks are collected
                    all_collected = True
                    for bonus in bonus_blocks:
                        if not bonus.collected:
                            all_collected = False
                            break
                    
                    if all_collected:
                        level_complete = True

                # Move enemies
                for enemy in enemies:
                    enemy.move(walls, hero)

                # Check collision with enemies
                hero_rect = pygame.Rect(hero.x, hero.y, HERO_SIZE, HERO_SIZE)
                for enemy in enemies:
                    enemy_rect = pygame.Rect(round(enemy.x), round(enemy.y), ENEMY_SIZE, ENEMY_SIZE)
                    if hero_rect.colliderect(enemy_rect):
                        game_over = True

        # Drawing
        screen.fill(BLACK)
        
        # Draw walls and bonus blocks
        for wall in walls:
            wall.draw(screen)
        for bonus in bonus_blocks:
            bonus.draw(screen)
        
        # Draw game objects
        hero.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)

        # Draw score and level
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {score}  Level: {level}', True, WHITE)
        screen.blit(score_text, (10, 10))

        # Draw level complete message
        if level_complete:
            font = pygame.font.Font(None, 74)
            text = font.render(f'Level {level} Complete!', True, GREEN)
            text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            screen.blit(text, text_rect)

        # Draw game over message
        if game_over:
            font = pygame.font.Font(None, 74)
            text = font.render(f'Game Over! Level {level}', True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 40))
            screen.blit(text, text_rect)
            
            font = pygame.font.Font(None, 50)
            text = font.render(f'Final Score: {score}', True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 20))
            screen.blit(text, text_rect)
            
            text = font.render('Press R to Restart', True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 70))
            screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
