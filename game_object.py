import pygame

# game object base for other game objects to be built on
class Game_object:

    def __init__(self, x, y, image, CELL_SIZE):
        self.image = image

        self.x = x
        self.y = y
        self.position = pygame.Vector2(x, y)
        self.hitbox = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())

        self.CELL_SIZE = CELL_SIZE

    # draws in offset position
    def draw(self, screen, camera):
        center_x = (self.x * self.CELL_SIZE) + (self.CELL_SIZE // 2)
        center_y = (self.y * self.CELL_SIZE) + (self.CELL_SIZE // 2)

        draw_x = center_x - (self.image.get_width() // 2)
        draw_y = center_y - (self.image.get_height() // 2)

        draw_pos = pygame.Vector2(draw_x, draw_y)
        screen.blit(self.image, camera.apply(draw_pos))

    # update abstract
    def update(self, grid, time):
        self.position = pygame.Vector2(self.x, self.y)
        
        center_x = (self.x * self.CELL_SIZE) + (self.CELL_SIZE // 2)
        center_y = (self.y * self.CELL_SIZE) + (self.CELL_SIZE // 2)

        self.hitbox.center = (center_x, center_y)

    # apply movement
    def move(self, dx, dy, grid):
        current_cell = grid[self.y][self.x]
        
        if dx == 1 and not current_cell.walls[1] and not grid[self.y][self.x + 1].walled:    
            #print("right")
            self.x += 1
        elif dx == -1 and not current_cell.walls[3] and not grid[self.y][self.x -1].walled:  
            #print("left")
            self.x -= 1
        elif dy == 1 and not current_cell.walls[2] and not grid[self.y + 1][self.x].walled:   
            #print("bottom")
            self.y += 1
        elif dy == -1 and not current_cell.walls[0] and not grid[self.y - 1][self.x].walled:  
            #print("up")
            self.y -= 1

    # check collisions
    def collide(self, other):
        if isinstance(other, Game_object):
            return self.hitbox.colliderect(other.hitbox)