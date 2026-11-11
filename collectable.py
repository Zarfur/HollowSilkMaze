from game_object import Game_object


class Collectable(Game_object):

    def __init__(self, x, y, image, CELL_SIZE, type):
        super().__init__(x, y, image, CELL_SIZE)
        self.type = type
        self.value = 1
        if self.type == "flea":
            self.value = 5

    

    pass