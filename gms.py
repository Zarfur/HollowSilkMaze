from sinner import Sinner
import random

import pygame



MOVES = {"up": 0, "down": 1, "left": 2, "right": 3} # rows of transition matrix 
DIRECTIONS = {0: (0, -1), 1: (0, 1), 2: (-1, 0), 3: (1, 0)} # movement represented as change in pos (x , y)

WALL = {0: 0, 1: 2, 2: 3, 3: 1}
# UP RIGHT DOWN LEFT 


class GMS(Sinner):


    # got help from HENRY LI Ethan Jones
    def __init__(self, x, y, image, CELL_SIZE, hp, target, grid):
        super().__init__(x, y, image, CELL_SIZE, hp, target, grid)
        self.transition_matrix = [
            [100, .7, 25, 25],
            [.7, 100, 25, 25],
            [25, 25, 100, .7],
            [25, 25, .7, 100]
            # row is move taken before
            #column is lieklihood of the move to be the next move 
        ] # starting prediction 
        self.path = []
        self.avg_accuracy = [1,1] # correct guesses out of total guesses 
        self.recency_bias = 0.8 # when gms forgets previous movement 
        self.predicted = None
        self.last_player_move = None

        self.pursuit_speed = 250
        self.movement_rate = 50
        self.RANGE = 66
        self.debug_color = (255, 255, 255)
        self.boss = True
        
    def predict(self, last_player_move):
        # no move seen yet so just direct chase player
        if last_player_move not in MOVES:
            return (self.global_target.x, self.global_target.y)

        px, py = self.global_target.x, self.global_target.y #pos
        dist = self.manhattan((self.x, self.y), (px, py)) #dist from gms
        if dist < 5:
            lookahead = 0
        elif dist < 10:
            lookahead = 2
        elif dist < 20:
            lookahead = 5
        else:
            lookahead = 10

            # "lookahead" gms devides how many moves to predict baased on the distance between player and gms
        move = MOVES[last_player_move] # which row in matrx
        for _ in range(lookahead):
            row = self.transition_matrix[move] #odds 
            cell = self.grid[py][px]  #pos 
            weights = [] # will hold final odds 
            for i in range(4): 
                dx, dy = DIRECTIONS[i]
                nx, ny = px + dx, py + dy
                in_bounds = 0 <= nx < len(self.grid[0]) and 0 <= ny < len(self.grid)
                weights.append(row[i] if in_bounds and not cell.walls[WALL[i]] else 0)
            if sum(weights) == 0:
                break
            move = random.choices(range(4), weights=weights)[0]
            px += DIRECTIONS[move][0]
            py += DIRECTIONS[move][1]
        return (px, py)

    def data_intake(self, last_plr_move, current_plr_move):
        if last_plr_move not in MOVES or current_plr_move not in MOVES:
                return
        last_i, cur_i = MOVES[last_plr_move], MOVES[current_plr_move]
        row = self.transition_matrix[last_i]

        guess = row.index(max(row))
        self.avg_accuracy[0] *= self.recency_bias
        self.avg_accuracy[1] *= self.recency_bias
        if guess == cur_i:
            self.avg_accuracy[0] += 1
        self.avg_accuracy[1] += 1

        for i in range(4):
            row[i] *= self.recency_bias
        row[cur_i] += 10

    def pursuit(self):
        self.predicted = self.predict(self.last_player_move)
        path = self.astar((self.x, self.y), self.predicted)
        if not path:  # predicted tile unreachable -> fall back to the player
            path = self.astar((self.x, self.y), (self.global_target.x, self.global_target.y))
        self.current_path = path

        if len(path) > 1:
            nx, ny = path[1]
            self.move(nx - self.x, ny - self.y, self.grid)
            self.current = self.grid[self.y][self.x]

        if (self.manhattan(self.global_target.current, self.current) >= self.RANGE
                and self.global_target.current not in self.visible_tiles):
            self.state = "search"
            self.last_search = pygame.time.get_ticks()

    def debug_draw(self, screen, camera):
        super().debug_draw(screen, camera)
        if self.predicted is not None:
            px, py = self.predicted

            tile = pygame.Rect(px * self.CELL_SIZE, py * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)

            tile_shift = camera.apply(pygame.Vector2(tile.x, tile.y))

            highlighted = pygame.Rect(tile_shift.x, tile_shift.y, self.CELL_SIZE, self.CELL_SIZE)
            highlight_surface = pygame.Surface((self.CELL_SIZE, self.CELL_SIZE), pygame.SRCALPHA)

        highlight_surface.fill((180, 0, 255, 90))

        screen.blit(highlight_surface, highlighted.topleft)