import pygame

# displays relevant data in bottom of screen
class Display:

    def __init__(self, boss, player, width, height):
        self.boss = boss
        self.player = player
        self.width = width
        self.height = height
        self.data = []
        self.font = pygame.font.Font(None, 24)


    def draw(self, screen):
        width = self.width
        height = self.height
        pygame.draw.rect(screen, (0, 0, 0), (0, height - height * 0.2, width, height * 0.2))
        for i, data in enumerate(self.data):
            text = self.font.render(str(data), True, (255, 255, 255))
            screen.blit(text, (5, (height - height * 0.2) + i * 15))



    def update(self):
        gms = self.boss
        plr = self.player

        accuracy = 0
        if gms.avg_accuracy[1] > 0:
            accuracy = gms.avg_accuracy[0] / gms.avg_accuracy[1] * 100
        
        self.data = [
            f"Player Candies: {plr.score}",
            f"Player Position: ({plr.x}, {plr.y})",
            f"Boss Position: ({gms.x}, {gms.y})",
            f"Last Player Move: {gms.last_player_move}",
            f"Predicted Position: {gms.predicted}",
            f"Prediction Accuracy: {accuracy:.1f}%",
            f"Boss State: {gms.state}",
            f"Current Path Length: {len(gms.current_path)}",
            f"Recency Bias: {gms.recency_bias}",
        ]