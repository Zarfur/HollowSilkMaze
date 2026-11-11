import pygame

class Camera:

    def __init__(self, x, y, width, height, game_width, game_height, cell_size):
        self.position = pygame.Vector2(x, y)
        self.width = width
        self.height = height
        self.game_width = game_width
        self.game_height = game_height
        self.CELL_SIZE = cell_size


    def apply(self, target):
        draw_x = target.x - self.position.x
        draw_y = target.y - self.position.y
        return pygame.Vector2(draw_x, draw_y)

    def update(self, target):

        center_x = (target.x * self.CELL_SIZE) + (self.CELL_SIZE // 2)
        center_y = (target.y * self.CELL_SIZE) + (self.CELL_SIZE // 2)


        camera_x = center_x - self.width / 2
        camera_x = max(0, min(camera_x, self.game_width - self.width))
        camera_y = center_y - self.height / 2
        camera_y = max(0, min(camera_y, self.game_height - self.height))
        self.position = pygame.Vector2(camera_x, camera_y)
