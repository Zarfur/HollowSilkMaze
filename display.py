import pygame

# displays relevant data in bottom of screen
class Display:

    def __init__(self, boss, player, width, height):
        self.boss = boss
        self.player = player
        self.width = width
        self.height = height
        self.data = ["score", "wah uwa wa uwa", "uwa wa taku taku", "cha o", "uwa", "wa wa wa uwa waai wo toreli", "uwa wa wa wai wai", "taichairo"]
        self.font = pygame.font.Font(None, 24)


    def draw(self, screen):
        width = self.width
        height = self.height
        pygame.draw.rect(screen, (0, 0, 0), (0, height - height * 0.2, width, height * 0.2))
        for i, data in enumerate(self.data):
            text = self.font.render(str(data), True, (255, 255, 255))
            screen.blit(text, (5, (height - height * 0.2) + i * 15))



    def update(self):
        self.data[0] = f"Player Candies: {self.player.score}"