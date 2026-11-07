

import pygame

GAME_WIDTH = 2400
GAME_HEIGHT = 2400
WIDTH = 800
HEIGHT = 800

FPS = 60
GRID_SIZE = 25  
CELL_SIZE = WIDTH // GRID_SIZE

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hollow Silk Maze")
clock = pygame.time.Clock()