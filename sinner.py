import heapq

from game_object import Game_object
import random
import pygame

class Sinner(Game_object):
    def __init__(self, x, y, image, CELL_SIZE, hp, target, grid):
        super().__init__(x, y, image, CELL_SIZE)
        self.hp = hp
        self.state = "patrol"
        self.movement_rate = 250
        self.global_target = target

        self.grid = grid
        self.current = self.grid[self.y][self.x]
        self.move_cooldown = 250
        self.RANGE = 8
        self.visible_tiles = []
        self.last_move = 0
        self.last_search = 0
        self.search_cd = 3000
        self.current_path = []
        self.debug_color = (255, 0, 0)
        self.pursuit_speed = 150

        self.font = pygame.font.Font(None, 24)

    # patrol/search state-- randomly goes to valid options
    def patrol(self):
        
        self.current = self.grid[self.y][self.x]

        options = self.possible_options(self.grid)  

        if options:
            dx, dy = random.choice(options)
            self.move(dx, dy, self.grid)
            self.current = self.grid[self.y][self.x]

        if self.manhattan(self.global_target.current, self.current) <= self.RANGE or self.global_target.current in self.visible_tiles:
            self.state = "pursuit"

    # sets target
    def set_target(self, target):
        if self.global_target is None:
            self.global_target = target

    # heuristic distance
    def manhattan(self, a, b):
        if isinstance(a, tuple): ax, ay = a
        else: ax, ay = a.x, a.y
        if isinstance(b, tuple): bx, by = b
        else: bx, by = b.x, b.y

        return abs(ax - bx) + abs(ay - by)

    # astar algorithm
    def astar(self, start, target):
        if start == target:
            return [start]
        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {start: None}
        cost_so_far = {start: 0}
        height = len(self.grid)
        width = len(self.grid[0])

        while frontier:
            _, current = heapq.heappop(frontier)
            if current == target:
                break
            cx, cy = current
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                next_node = (cx + dx, cy + dy)
                nx, ny = next_node

                if 0 <= nx < width and 0 <= ny < height:
                    current_cell = self.grid[cy][cx]
                    
                    if dx == -1: blocked = current_cell.walls[3]
                    elif dx == 1: blocked = current_cell.walls[1]
                    elif dy == -1: blocked = current_cell.walls[0]
                    else: blocked = current_cell.walls[2]

                    if blocked: continue
                
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

    # pursuit method--while parameters, chases player
    def pursuit(self):
        
        start = (self.x, self.y)
        target = (self.global_target.x, self.global_target.y)
        astar_path = self.astar(start, target)
        self.current_path = astar_path

        if len(astar_path) > 1:
            nx, ny = astar_path[1]
            dx = nx - self.x
            dy = ny - self.y
            self.move(dx, dy, self.grid)
            self.current = self.grid[self.y][self.x]

        if self.manhattan(self.global_target.current, self.current) >= self.RANGE and not self.global_target.current in self.visible_tiles:
            self.state = "search"
            self.last_search = pygame.time.get_ticks()

    # checks line of sight to player--easier tracking with less walls
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

    # check possible movement options
    def possible_options(self, grid):
        options = []

        height = len(grid)
        width = len(grid[0])
        if self.y > 0:
            if not self.current.walls[0] and grid[self.y - 1][self.x]:
                options.append((0, -1))
        if self.x < width - 1:
            if not self.current.walls[1] and grid[self.y][self.x + 1]:
                options.append((1, 0))
        if self.y < height - 1:
            if not self.current.walls[2] and grid[self.y + 1][self.x]:
                options.append((0, 1))
        if self.x > 0:
            if not self.current.walls[3] and grid[self.y][self.x - 1]:
                options.append((-1, 0))
        return options

        # updates line of sight and state
    def update(self, grid, current_time):
        super().update(grid, current_time)
        self.current = self.grid[self.y][self.x]
        self.line_of_sight()

        if current_time - self.last_move > self.move_cooldown * 2: 
            self.last_move = current_time
            #print(f"current state: {self.state}")
            #print(f"target: {self.global_target}")
            if self.state == "pursuit":
                self.move_cooldown = self.pursuit_speed
                self.pursuit()
            elif self.state == "search":
                if current_time - self.last_search >= self.search_cd:
                    self.last_search = 0
                    self.state = "patrol"
                self.move_cooldown = self.movement_rate - 200
                self.patrol()
            else:
                self.move_cooldown = self.movement_rate
                self.patrol()

    # take damage or die
    def take_damage(self, enemies, destructables):
        #print(f"current hp: {self.hp}")
        self.hp -= 1
        if self.hp <= 0:
            self.global_target.score += 7
            if self in enemies:
                enemies.remove(self)
                destructables.remove(self)

                del self

    # draws path for debug mode
    def draw_path(self, screen, camera):
        if not self.current_path: return
        for x, y in self.current_path:
            center_x = x * self.CELL_SIZE + self.CELL_SIZE // 2
            center_y = y * self.CELL_SIZE + self.CELL_SIZE //2

            draw_pos = camera.apply(pygame.Vector2(center_x, center_y))
            pygame.draw.circle(screen, self.debug_color, (draw_pos.x, draw_pos.y), 5)
        

    # draws state for debug mode
    def debug_draw(self, screen, camera):
        center_x = (self.x * self.CELL_SIZE) + (self.CELL_SIZE // 2) - (self.image.get_width() // 2)
        center_y = (self.y * self.CELL_SIZE) + (self.CELL_SIZE // 2) - (self.image.get_height() // 2) - 10
        pos = pygame.Vector2(center_x, center_y)
        text = self.font.render(str(self.state), True, (255, 255, 255))
        screen.blit(text, camera.apply(pos))

    # returns if player is killed or not
    def end_game(self):
        if self.position == self.global_target.position:
            return True
        return False
