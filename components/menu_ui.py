import pygame
import pygame_gui


class MainMenuScene:
    def __init__(self, manager):
        self.manager = manager

        # buttons
        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(0, -40, 200, 50),
            text='Start Game',
            manager=self.manager,
            anchors={'center': 'center'},
            object_id=pygame_gui.core.ObjectID('start_button')
        )

    def handle_events(self, events):
        for event in events:
            self.manager.process_events(event)

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.start_button:
                    pass

    def update(self, time_delta):
        self.manager.update(time_delta)

    def render(self, surface):
        surface.fill(pygame.Color('darkgray'))
        self.manager.draw_ui(surface)
