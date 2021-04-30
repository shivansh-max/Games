# Imports
import pygame
import sys

pygame.init()

# load images
Bg = pygame.image.load("BG.png")
Icon = pygame.image.load("Bird.png")

# Screen
Width = 500
Height = 700
win = pygame.display.set_mode((Width,Height))
pygame.display.set_caption("Flappy bird")
pygame.display.set_icon(Icon)

# Main loop
game_over = False
while not(game_over):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    win.blit(Bg, (0,0))

    pygame.display.update()

sys.exit()