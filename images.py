import os
import pygame

# Get the directory where this script is located
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(CURRENT_DIR, "images")

def load_image(name, size=None):
    """Load an image and scale it if size is provided."""
    try:
        image = pygame.image.load(os.path.join(IMAGE_DIR, name))
        if size:
            image = pygame.transform.scale(image, size)
        return image
    except:
        print(f"Error loading image: {name}")
        return None

# Load images
def load_game_images(hero_size, enemy_size):
    """Load and return all game images scaled to the appropriate sizes."""
    images = {
        'pacman': load_image('pacman.png', (hero_size, hero_size)),
        'ghost_red': load_image('ghost_red.png', (enemy_size, enemy_size)),
        'ghost_orange': load_image('ghost_orange.png', (enemy_size, enemy_size))
    }
    
    # Create fallback surfaces if images fail to load
    if not images['pacman']:
        surface = pygame.Surface((hero_size, hero_size))
        surface.fill((255, 255, 0))  # Yellow for Pacman
        images['pacman'] = surface
        
    if not images['ghost_red']:
        surface = pygame.Surface((enemy_size, enemy_size))
        surface.fill((255, 0, 0))  # Red ghost
        images['ghost_red'] = surface
        
    if not images['ghost_orange']:
        surface = pygame.Surface((enemy_size, enemy_size))
        surface.fill((255, 128, 0))  # Orange ghost
        images['ghost_orange'] = surface
    
    return images
