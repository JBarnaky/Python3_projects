import numpy as np
import pygame
import time

# Initialize Pygame
pygame.init()

# Set the screen resolution
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the frame rate (frames per second)
fps = 60
clock = pygame.time.Clock()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Generate white noise
    white_noise = np.random.randint(0, 256, (screen_height, screen_width, 3), dtype=np.uint8)

    # Convert the numpy array to a Pygame surface
    noise_surface = pygame.surfarray.make_surface(white_noise)

    # Blit the surface to the screen
    screen.blit(pygame.transform.scale(noise_surface, (screen_width, screen_height)), (0, 0))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(fps)

# Quit Pygame
pygame.quit()