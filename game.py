import pygame
from enum import Enum
import pygame_gui
import components.menu_ui as menue_ui

class GameUI:
    def __init__(self, manager):
        self.manager = manager

    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            pass


    def update(self, time_delta):
        pass  # Falls später Animation oder anderes nötig wird


class GameStates(Enum):
    MAIN_MENU = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4


class GameStateManager:
    def __init__(self):
        self.current_state = GameStates.MAIN_MENU

    def change_state(self, new_state):
        self.current_state = new_state


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Quick Start')

        self.window_surface = pygame.display.set_mode((800, 600))
        self.background = pygame.Surface((800, 600))
        self.background.fill(pygame.Color('#000000'))

        self.manager = pygame_gui.UIManager((800, 600))
        self.menue_ui = menue_ui.MainMenuScene(self.manager)
        self.ui = GameUI(self.manager)

        self.clock = pygame.time.Clock()
        self.is_running = True

        # Set up the game state manager
        self.game_state_manager = GameStateManager()



    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

            self.ui.handle_event(event)
            self.manager.process_events(event)

    def update(self, time_delta):
        self.manager.update(time_delta)
        self.ui.update(time_delta)
        pass

    def render(self):
        self.window_surface.blit(self.background, (0, 0))
        self.manager.draw_ui(self.window_surface)
        pygame.display.update()

    def run(self):
        while self.is_running:
            time_delta = self.clock.tick(60) / 1000.0
            self.handle_events()
            self.update(time_delta)
            self.render()


if __name__ == "__main__":
    game = Game()
    game.run()
