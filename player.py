from game_object import Game_object
import pygame
from sinner import Sinner
from cell import Cell


class Player(Game_object):

    def __init__(self, x, y, image, CELL_SIZE, hp, enemies, destructables, m1rng):
        super().__init__(x, y, image, CELL_SIZE)
        self.hp = hp
        self.score = 0
        self.current = None
        self.enemies = enemies
        self.destructables = destructables

        self.m1_effect_timer = 0
        self.m1_effect_duration = 230  
        self.m1_effect_pos = None
        self.m1_effect_radius = 0
        self.m1_range = m1rng


    def m1(self, destructables):
        center_x = (self.x * self.CELL_SIZE) + (self.CELL_SIZE // 2)
        center_y = (self.y * self.CELL_SIZE) + (self.CELL_SIZE // 2)
        m1_box = pygame.Rect(0, 0, self.image.get_width() * self.m1_range, self.image.get_height() * self.m1_range)
        m1_box.center = (center_x, center_y)

        self.m1_effect_pos = m1_box.center
        self.m1_effect_radius = m1_box.width / 2
        self.m1_effect_timer = pygame.time.get_ticks()

        
        for obj in destructables:
            #print(f"{obj}")
            if obj.hitbox.colliderect(m1_box):
                #print("m1 collided!")
                if isinstance(obj, Sinner):
                    obj.take_damage(self.enemies, self.destructables)
                elif isinstance(obj, Cell):
                    obj.walled = False

        del m1_box
                    


    def update(self, grid, time):
        super().update(grid, time)
        self.current = grid[self.y][self.x]

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
            self.m1(self.destructables)

    def draw_m1(self, screen, camera):
        if self.m1_effect_pos is None:
            return
        if pygame.time.get_ticks() - self.m1_effect_timer > self.m1_effect_duration:
            self.m1_effect_pos = None
            return

        r = self.m1_effect_radius

        surface = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        pygame.draw.circle(surface, (255, 255, 255, 150), (r, r), r)

        center_x, center_y = self.m1_effect_pos
        draw_pos = pygame.Vector2(center_x - r, center_y - r)
        screen.blit(surface, camera.apply(draw_pos))


