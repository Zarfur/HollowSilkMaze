from game_object import Game_object
import random

class Sinner(Game_object):
    def __init__(self, x, y, image, CELL_SIZE, hp, target, grid):
        super().__init__(x, y, image, CELL_SIZE)
        self.hp = hp
        self.state = "patrol"
        self.movement_rate = 5
        self.global_target = target
        self.current_target = None

        self.grid = grid
        self.current = self.grid[self.x][self.y]

    def patrol(self, grid):
        self.current = grid[self.y][self.x]

        options = self.possible_options(grid)  

        if options:
            dx, dy = random.choice(options)
            self.move(dx, dy, grid)
            self.current = grid[self.y][self.x]
            self.visited.append(self.current)
            self.path.append(self.current)

    def pursuit(self):
        pass

    def a_star(self):
        pass

    def search(self):
        pass

    def line_of_sight(self):
        pass 


    def possible_options(self, grid):
        options = []
        if not self.current.walls[0] and grid[self.y - 1][self.x] not in self.visited:
            options.append((0, -1))
        if not self.current.walls[1] and grid[self.y][self.x + 1] not in self.visited:
            options.append((1, 0))
        if not self.current.walls[2] and grid[self.y + 1][self.x] not in self.visited:
            options.append((0, 1))
        if not self.current.walls[3] and grid[self.y][self.x - 1] not in self.visited:
            options.append((-1, 0))
        return options

    
    def update(self, grid):
        super.update()
        if self.state == "pursuit":
            self.pursuit(grid)
        elif self.state == "search":
            self.search(grid)
        else:
            self.patrol(grid)
        
