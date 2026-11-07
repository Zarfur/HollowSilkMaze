import pygame

from Mazes.MazeProject.HollowSilkMaze.game_object import Game_object

class Cell(Game_object):

    def __init__(self, x, y, size, color, wall):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.wall = wall

        #               top, right, bottom, left
        self.walls = [True, True, True, True]
        self.visited = False

    def draw(self, surface, camera):
        
        x_pix = self.x * self.size
        y_pix = self.y *  self.size

        screen_pos = camera.apply(pygame.Vector2(x_pix, y_pix))

        x_pix = screen_pos.x
        y_pix = screen_pos.y

        # draws bg during generation
        if self.visited:
            pygame.draw.rect(surface, self.color, (x_pix, y_pix, self.size, self.size))

        # wall render
        if self.walls[0]: # top
            pygame.draw.line(surface, self.wall, (x_pix, y_pix), (x_pix + self.size, y_pix), 2)
        if self.walls[1]: # right
            pygame.draw.line(surface, self.wall, (x_pix + self.size, y_pix), (x_pix + self.size, y_pix + self.size), 2)
        if self.walls[2]: # bottom
            pygame.draw.line(surface, self.wall, (x_pix + self.size, y_pix + self.size), (x_pix, y_pix + self.size), 2)
        if self.walls[3]: # left
            pygame.draw.line(surface, self.wall, (x_pix, y_pix + self.size), (x_pix, y_pix), 2)