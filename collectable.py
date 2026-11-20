from game_object import Game_object


# collectable for score
class Collectable(Game_object):

    def __init__(self, x, y, image, CELL_SIZE, type, player, collectables):
        super().__init__(x, y, image, CELL_SIZE)
        self.type = type
        self.value = 1
        if self.type == "flea":
            self.value = 125
        if self.type == "candy":
            self.value = 15
        self.collected = False
        self.player = player
        self.collectables = collectables

    def collect(self, player):
        # might collect the item multiple times
        if player.x == self.x and player.y == self.y:
            player.score += self.value
            self.collected = True

    def update(self, grid, time):
        super().update(grid, time)

        if self.collide(self.player):
            
            self.player.score += self.value

            if self in self.collectables:
                self.collectables.remove(self)
                del self

    

