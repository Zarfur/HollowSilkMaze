from game_object import Game_object
import pygame


class Player(Game_object):

    def __init__(self, x, y, image, CELL_SIZE, hp):
        super().__init__(x, y, image, CELL_SIZE)
        self.hp = hp


    def find_nearest_target(self, grid):
        pass
    
    def m1(self):
        pass

    def update(self, grid):
        super.update(grid)
        self.find_nearest_target(grid)

    def get_inputs(self, key, grid):
        if key == pygame.K_UP:
            self.move(0, -1, grid)
        elif key == pygame.K_DOWN:
            self.move(0, 1, grid)
        elif key == pygame.K_LEFT:
            self.move(-1, 0, grid)
        elif key == pygame.K_RIGHT:
            self.move(1, 0, grid)
        elif key == pygame.K_x:
            self.m1()

    
