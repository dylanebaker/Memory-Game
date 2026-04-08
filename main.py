import pygame
import sys

from constants import *
from game import Game
from tile import Tile

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Memory Game")
clock = pygame.time.Clock()

game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            game.handle_click(event.pos)

    screen.fill((BLACK))
    game.update()
    game.draw(screen)

    pygame.display.update()
    clock.tick(FPS)
