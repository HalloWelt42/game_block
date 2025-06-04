from dataclasses import dataclass
import pygame
from enum import Enum
import random
import pygame_gui
import components.menu_ui as menue_ui
from color_palette.material_colors import MaterialDesign

Settings = {
    "window_size": (800, 600),
    "background_start": MaterialDesign.Grey.M900.value,
    "background_game": MaterialDesign.Grey.M900.value,
}


class GameStates(Enum):
    MAIN_MENU = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4


class ItemNames(Enum):
    LINE = "line"  # Horizontal line
    SQUARE = "square"  # Square block
    L = "l"  # L-shaped block
    T = "t"  # T-shaped  block
    S_LEFT = "s_left"  # Left S-shaped block
    S_RIGHT = "s_right"  # Right S-shaped block


@dataclass
class Item:
    name: ItemNames
    color: MaterialDesign.ColorBase
    grid: list[list[int]]  # 2D grid representing the item layout


@dataclass
class Items:
    items: list[Item]

    def __init__(self):
        self.items = [
            Item(ItemNames.LINE, MaterialDesign.LightBlue.M600, [[1, 1, 1, 1, 1]]),
            Item(ItemNames.SQUARE, MaterialDesign.Green.M600, [[1, 1, 1], [1, 1, 1], [1, 1, 1]]),
            Item(ItemNames.L, MaterialDesign.Orange.M600, [[1, 0, 0], [1, 1, 1]]),
            Item(ItemNames.T, MaterialDesign.Purple.M600, [[0, 1, 0], [1, 1, 1]]),
            Item(ItemNames.S_LEFT, MaterialDesign.Red.M600, [[0, 1, 1], [1, 1, 0]]),
            Item(ItemNames.S_RIGHT, MaterialDesign.Yellow.M600, [[1, 1, 0], [0, 1, 1]]),
        ]

    def rand(self) -> Item:
        return random.choice(self.items)

    def get(self, name: ItemNames) -> Item:
        for item in self.items:
            if item.name == name:
                return item
        raise ValueError(f"Item with name {name.value} not found.")


class GameStateManager:
    def __init__(self):
        self.__current_state = GameStates.MAIN_MENU

    def change_state(self, new_state: GameStates):
        self.__current_state = new_state

    def get_current_state(self) -> GameStates:
        return self.__current_state


class GameBoard:
    def __init__(self,
                 manager: pygame_gui.UIManager,
                 screen: pygame.Surface,
                 ):
        self.manager = manager
        self.screen = screen
        self.rows = 8
        self.cols = self.rows
        self.field_size = 50
        self.field_boarder = 2
        self.position = (10, 10)
        self.grid = [[0 for _ in range(self.rows)] for _ in range(self.cols)]

    def reset(self):
        self.grid = [[0 for _ in range(self.rows)] for _ in range(self.cols)]

    def draw(self):
        for y in range(self.cols):
            for x in range(self.rows):
                pygame.draw.rect(
                    self.screen, pygame.Color(MaterialDesign.Grey.M800.value), (
                        x * self.field_size + self.position[0],
                        y * self.field_size + self.position[1],
                        self.field_size + self.field_boarder,
                        self.field_size + self.field_boarder
                    ), self.field_boarder
                )


class ItemBoard:
    def __init__(self,
                 manager: pygame_gui.UIManager,
                 screen: pygame.Surface,
                 ):
        # self.item = Item()
        self.items = None
        self.manager = manager
        self.screen = screen
        self.rows = 5
        self.cols = self.rows
        self.field_size = 50
        self.field_boarder = 2
        self.position = (450, 10)
        self.grid = [[0 for _ in range(self.rows)] for _ in range(self.cols)]

    def draw(self):
        for y in range(self.cols):
            for x in range(self.rows):
                pygame.draw.rect(
                    self.screen, pygame.Color(MaterialDesign.Grey.M800.value), (
                        x * self.field_size + self.position[0],
                        y * self.field_size + self.position[1],
                        self.field_size + self.field_boarder,
                        self.field_size + self.field_boarder
                    ), self.field_boarder
                )

    def set_item(self, item: Item):
        self.item = item
        # correct the position of the item in the item board
        #   calculate center position
        grid_x = (self.cols - len(item.grid[0])) // 2
        grid_y = (self.rows - len(item.grid)) // 2

        # Draw the item on the item board
        for y in range(len(item.grid)):
            for x in range(len(item.grid[y])):
                # Check if the grid cell is occupied
                if item.grid[y][x] == 1:
                    pygame.draw.rect(
                        self.screen, pygame.Color(item.color.value), (
                            x * self.field_size + self.position[0] + self.field_boarder +
                            (grid_x * self.field_size),
                            y * self.field_size + self.position[1] + self.field_boarder +
                            (grid_y * self.field_size),
                            self.field_size - self.field_boarder,
                            self.field_size - self.field_boarder
                        )
                    )

    def check_click_on(self, event) -> bool:
        mouse_x, mouse_y = event.pos
        grid_x, grid_y = self.position
        grid_x2 = grid_x + self.cols * self.field_size
        grid_y2 = grid_y + self.rows * self.field_size

        # Check if the click is within the bounds of the item board
        if grid_x <= mouse_x <= grid_x2 and grid_y <= mouse_y <= grid_y2:
            # detect grid number
            grid_col = (mouse_x - grid_x) // self.field_size
            grid_row = (mouse_y - grid_y) // self.field_size
            print(mouse_x, mouse_y, grid_col, grid_row)
            return True
        return False


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Quick Start')

        self.screen = pygame.display.set_mode(Settings["window_size"])
        self.background = pygame.Surface(Settings["window_size"])
        self.background.fill(pygame.Color(Settings["background_start"]))
        self.manager = pygame_gui.UIManager(Settings["window_size"])
        self.menue_ui = menue_ui.MainMenuScene(self.manager)

        self.clock = pygame.time.Clock()
        self.is_running = True

        # Set up the game state manager
        self.game_state = GameStateManager()

        # Initialize the game board
        self.board = GameBoard(
            self.manager, self.screen
        )

        # Initialize the item board
        self.item_board = ItemBoard(
            self.manager, self.screen
        )

        # Initialize the selected item
        self.selected_item = Items().rand()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                self.game_state.change_state(GameStates.PLAYING)
                self.background.fill(pygame.Color(Settings["background_game"]))

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.item_board.check_click_on(event)

            # todo: remove this
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                self.selected_item = Items().rand()

            self.manager.process_events(event)

    def update(self, time_delta):
        self.manager.update(time_delta)
        pass

    def render(self):
        self.screen.blit(self.background, (0, 0))
        if self.game_state.get_current_state() == GameStates.MAIN_MENU:
            self.manager.draw_ui(self.screen)

        if self.game_state.get_current_state() == GameStates.PLAYING:
            self.board.draw()
            self.item_board.draw()
            self.item_board.set_item(self.selected_item)

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
