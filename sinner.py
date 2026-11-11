import heapq

from game_object import Game_object
import random

class Sinner(Game_object):
    def __init__(self, x, y, image, CELL_SIZE, hp, target, grid):
        super().__init__(x, y, image, CELL_SIZE)
        self.hp = hp
        self.state = "pursuit"
        self.movement_rate = 5
        self.global_target = target
        self.current_target = None

        self.grid = grid
        self.current = self.grid[self.x][self.y]
        self.move_cooldown = 150
        self.RANGE = 8
        self.visible_tiles = []

    def patrol(self, grid):
        self.current = grid[self.y][self.x]

        options = self.possible_options(grid)  

        if options:
            dx, dy = random.choice(options)
            self.move(dx, dy, grid)
            self.current = grid[self.y][self.x]
            self.visited.append(self.current)
            self.path.append(self.current)

    def set_target(self, target):
        if self.global_target is None:
            self.global_target = target


    def manhattan(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
        
    def astar(self, start, target):
        if start == target:
            return [start]
        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {start: None}
        cost_so_far = {start: 0}

        while frontier:
            _, current = heapq.heappop(frontier)
            if current == target:
                break
            cx, cy = current
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                next_node = (cx + dx, cy + dy)
                nx, ny = next_node

                if 0 <= nx < 50 and 0 <= ny < 50 and self.grid[ny][nx] == 0:
                    new_cost = cost_so_far[current] + 1
                    if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                        cost_so_far[next_node] = new_cost
                        priority = new_cost + self.manhattan(target, next_node)
                        heapq.heappush(frontier, (priority, next_node))
                        came_from[next_node] = current
        if target not in came_from:
            return [] 
        
        path = []
        curr = target
        while curr is not None:
            path.append(curr)
            curr = came_from[curr]
        path.reverse()
        return path

    def pursuit(self):
        
        if len(astar_path) > 1:
            curr_pos = list(astar_path[1])
        
            astar_path = self.astar(self.grid, tuple(curr_pos), tuple(self.current_target.position))

        position = self.current_target.position
        target_tile = self.grid[position.y][position.x]

        if not (target_tile in self.visible_tiles or self.manhattan(target_tile, self.current) <= self.RANGE):
            self.state = "search"

    def line_of_sight(self):
        available_directions = self.possible_options(self.grid)
        self.visible_tiles = [self.current]
        for dx, dy in available_directions:
            x, y = self.x, self.y
            for i in range(66):
                x += dx
                y += dy
                if not (0 <= x < len(self.grid[0]) and 0 <= y < len(self.grid)): break
                self.visible_tiles.append(self.grid[y][x])

                next_cell = self.grid[y][x]

                if dx == 0 and dy == -1 and next_cell.walls[0]: break
                elif dx == 1 and dy == 0 and next_cell.walls[1]: break
                elif dx == 0 and dy == 1 and next_cell.walls[2]: break
                elif dx == -1 and dy == 0 and next_cell.walls[3]: break


    def possible_options(self, grid):
        options = []
        if not self.current.walls[0] and grid[self.y - 1][self.x]:
            options.append((0, -1))
        if not self.current.walls[1] and grid[self.y][self.x + 1]:
            options.append((1, 0))
        if not self.current.walls[2] and grid[self.y + 1][self.x]:
            options.append((0, 1))
        if not self.current.walls[3] and grid[self.y][self.x - 1]:
            options.append((-1, 0))
        return options

    
    def update(self, grid, current_time):
        last_move = current_time
        super().update(grid, current_time)

        self.current = self.grid[self.x][self.y]
        self.line_of_sight()

        if current_time - last_move > self.move_cooldown * 2: 
            if self.state == "pursuit":
                self.move_cooldown = 150
                self.pursuit(grid)
            elif self.state == "search":
                self.move_cooldown = 100
                self.patrol(grid)
            else:
                self.move_cooldown = 250
                self.patrol(grid)


        
