from sinner import Sinner
import random


class GMS(Sinner):
    # got help from HENRY LI Ethan Jones
    def __init__(self, x, y, image, CELL_SIZE, hp, target, grid):
        super().__init__(x, y, image, CELL_SIZE, hp, target, grid)
        self.transition_matrix = [
            100, .7, 25, 25,
            .7, 100, 25, 25,
            25, 25, 100, .7,
            25, 25, .7, 100
        ]
        self.path = []
        self.avg_accuracy = [1,1]
        self.recency_bias = 0.8
        
    # ehhhh find a comment to describe this...
    def predict(self, last_player_move):
        transitions = {"up": 0, "down": 1, "left": 2, "right": 3}
        move_dict = {0: (0, -1), 1: (0, 1), 2: (-1, 0), 3: (1, 0)}
        next_move = transitions[last_player_move]
        target_pos = self.global_target.position
        lookahead = 10
        if self.manhattan(tuple(self.position), tuple(target_pos)) < 5:
            lookahead = 0
        elif self.manhattan(tuple(self.position), tuple(target_pos)) < 10:
            lookahead = 2
        elif self.manhattan(tuple(self.position), tuple(target_pos)) < 20:
            lookahead = 5
        for i in range(lookahead):
            current_row = self.transition_matrix[next_move]
        filtered = []
        for i in range(4):
            dx, dy = move_dict[i]
            new_x = target_pos[0] + dx
            new_y = target_pos[1] + dy
            if 0 <= new_x < len(self.grid) and 0 <= new_y < len(self.grid[0]):
                    filtered.append((current_row[i], (new_x, new_y)))
            else:
                    filtered.append((0, (new_x, new_y)))
            if filtered:
                next_move = random.choices([i for i in range(4)], weights=[f[0] for f in filtered])[0]
                target_pos = filtered[next_move][1]

    # this one too!
    def data_intake(self, last_plr_move, current_plr_move):
        transitions = {"up": 0, "down": 1, "left": 2, "right": 3}
        self.avg_accuracy[0] *= self.recency_bias
        self.avg_accuracy[1] *= self.recency_bias
        if (random.choices([0, 1, 2, 3], weights=self.transition_matrix[transitions[last_plr_move]]))[0] == transitions[current_plr_move]:
            self.avg_accuracy[0] += 1
        self.avg_accuracy[1] += 1
        last_move_index = transitions[last_plr_move]
        current_move_index = transitions[current_plr_move]
        for i in range(4):
            self.transition_matrix[last_move_index][i] *= self.recency_bias
        self.transition_matrix[last_move_index][current_move_index] += 1

