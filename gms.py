from game_object import Game_object
from sinner import Sinner


class GMS(Sinner):

    def __init__(self, x, y, image, CELL_SIZE, hp, target, grid):
        super().__init__(x, y, image, CELL_SIZE, hp, target, grid)
        self.transition = [
            100, .7, 25, 25,
            .7, 100, 25, 25,
            25, 25, 100, .7,
            25, 25, .7, 100
        ]
        

        
    def predict():
        pass

    def data_intake(self, most_recent_move):
        pass