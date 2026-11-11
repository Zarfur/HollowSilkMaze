import pygame

class Game_object:

    def __init__(self, x, y, image, CELL_SIZE):
        self.image = image
        self.image_right = image
        self.image_left = pygame.transform.flip(image, True, False)
        self.facing_right = True 

        self.x = x
        self.y = y
        self.position = pygame.Vector2(x, y)
        self.hitbox = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())

        self.CELL_SIZE = CELL_SIZE


    def draw(self, screen, camera):
        center_x = (self.x * self.CELL_SIZE) + (self.CELL_SIZE // 2)
        center_y = (self.y * self.CELL_SIZE) + (self.CELL_SIZE // 2)

        draw_x = center_x - (self.image.get_width() // 2)
        draw_y = center_y - (self.image.get_height() // 2)

        draw_pos = pygame.Vector2(draw_x, draw_y)
        screen.blit(self.image, camera.apply(draw_pos))
    
    def update(self, grid):

        self.position = pygame.Vector2(self.x, self.y)




    def move(self, dx, dy, grid):
        current_cell = grid[self.y][self.x]
        
        if dx == 1 and not current_cell.walls[1] and not grid[self.x + 2][self.y].walled:    
            #print("right")
            self.x += 1
        elif dx == -1 and not current_cell.walls[3] and not grid[self.x - 2][self.y].walled:  
            #print("left")
            self.x -= 1
        elif dy == 1 and not current_cell.walls[2] and not grid[self.x][self.y + 2].walled:   
            #print("bottom")
            self.y += 1
        elif dy == -1 and not current_cell.walls[0] and not grid[self.x][self.y - 2].walled:  
            #print("up")
            self.y -= 1

    def take_damage(self, m1_hitbox):
        pass

    def collide_other(self, other):
        pass