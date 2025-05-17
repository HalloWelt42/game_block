import pygame
import color_palette.material_colors as colors


class Board:
    def __init__(self):
        self.size = (8, 8)

    def draw(self, screen):
        start, end, unfilled = 50, 100, True

        for x in range(self.size[0]):
            for y in range(self.size[1]):
                unfilled = True
                row = start + (x * 40)
                col = end + (y * 40)
                pygame.draw.rect(screen, colors.Grey.M800.value, (
                    row, col, 40, 40
                ), unfilled)
        pass

    def update(self, screen):

        pass



# Main game class
class Game:
    def __init__(self, width=800, height=600, fps=60):
        pygame.init()
        self.size = (width, height)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Blocks")
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self, delta_time):
        # Logik später hier rein
        pass

    def draw(self):
        self.screen.fill(colors.Grey.M900.value)
        self.board = Board()
        self.board.draw(self.screen)
        pygame.display.update()

    def run(self):
        while self.running:
            delta_time = self.clock.tick(self.fps) / 1000.0
            self.handle_events()
            self.update(delta_time)
            self.draw()

        pygame.quit()

    pass


if __name__ == "__main__":
    game = Game()
    game.run()
