import pygame
import os

# Initialize Pygame
pygame.init()

def create_pacman(size):
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    # Draw yellow circle for Pacman
    pygame.draw.circle(surface, (255, 255, 0), (size//2, size//2), size//2)
    # Draw mouth (triangle)
    pygame.draw.polygon(surface, (0, 0, 0), [
        (size//2, size//2),
        (size, size//4),
        (size, size*3//4)
    ])
    return surface

def create_ghost(size, color):
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    # Draw ghost body
    pygame.draw.rect(surface, color, (0, size//2, size, size//2))
    pygame.draw.circle(surface, color, (size//2, size//2), size//2)
    # Draw eyes
    eye_color = (255, 255, 255)
    pygame.draw.circle(surface, eye_color, (size//3, size//2), size//6)
    pygame.draw.circle(surface, eye_color, (size*2//3, size//2), size//6)
    # Draw pupils
    pupil_color = (0, 0, 255)
    pygame.draw.circle(surface, pupil_color, (size//3, size//2), size//10)
    pygame.draw.circle(surface, pupil_color, (size*2//3, size//2), size//10)
    return surface

# Create images directory if it doesn't exist
if not os.path.exists('images'):
    os.makedirs('images')

# Create and save images
size = 32  # Base size for images
pygame.image.save(create_pacman(size), 'images/pacman.png')
pygame.image.save(create_ghost(size, (255, 0, 0)), 'images/ghost_red.png')
pygame.image.save(create_ghost(size, (255, 128, 0)), 'images/ghost_orange.png')

print("Images created successfully!")
pygame.quit()
