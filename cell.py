import pygame
import random
from game_object import Game_object

# cell of a maze
class Cell(Game_object):

    def __init__(self, x, y, size, color, wall, destructables):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.wall = wall
        self.hitbox = pygame.Rect(x * size, y * size, size, size)

        #               top, right, bottom, left
        self.walls = [True, True, True, True]
        self.visited = False

        # decides if wall is blocked with silk or not
        self.walled = random.random() <= 0.08 and x != 0 and y != 0
        if self.walled:
            destructables.append(self)


    def draw(self, surface, camera):
        
        x_pix = self.x * self.size
        y_pix = self.y *  self.size

        screen_pos = camera.apply(pygame.Vector2(x_pix, y_pix))

        x_pix = screen_pos.x
        y_pix = screen_pos.y

        if self.visited:
            if self.walled:
                pygame.draw.rect(surface, self.wall, (x_pix, y_pix, self.size, self.size))   
            else:
                pygame.draw.rect(surface, self.color, (x_pix, y_pix, self.size, self.size))

        # wall render
        if self.walls[0]: 
            pygame.draw.line(surface, self.wall, (x_pix, y_pix), (x_pix + self.size, y_pix), 2)
        if self.walls[1]: 
            pygame.draw.line(surface, self.wall, (x_pix + self.size, y_pix), (x_pix + self.size, y_pix + self.size), 2)
        if self.walls[2]: 
            pygame.draw.line(surface, self.wall, (x_pix + self.size, y_pix + self.size), (x_pix, y_pix + self.size), 2)
        if self.walls[3]: 
            pygame.draw.line(surface, self.wall, (x_pix, y_pix + self.size), (x_pix, y_pix), 2)