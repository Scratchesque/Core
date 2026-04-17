import pygame
from pygame import Rect
from pygame_gui.elements import UIImage, UIPanel
from pygame_gui._constants import *

from game.app.board import Board
from game.app.code_blocks import CodeBlocks
from game.app.panels import ConfirmationPanel, LevelText
from game.core.images import load_image
from game.core.json_support import load_json
from game.core.paths import resolve_project_path
from game.core.ui import UIFactory
from game.core.constants import IMG_TILE_SIZE, LEVEL_COMPLETED, MENU_ENV_CONFIRMED, MENU_ENV_REQUESTED, NEXT_ENV_CONFIRMED, RESET_ENV_CONFIRMED, RESET_ENV_REQUESTED, SCREEN_HEIGHT, SCREEN_WIDTH
from game.core.csv_support import import_map_layout

# New environemnts/screens that are loaded through the game manager should inherit this class
class BaseEnvironment:
    # When an environemnt using this class init's, it loads all relevant data from 'environments/data/{level_file}.json" to be used
    def __init__(self, level_file):
        root_dir = "game/environments/data/"
        env_path = f"{root_dir}{level_file}.json"
        self.env_data = load_json(env_path)
        if not self.env_data:
            print(f'Using default env data. Could not find env data: {level_file}')
            default_path = f"{root_dir}default.json"
            self.env_data = load_json(default_path)

        init_data = self.env_data.env.init

        self.title = init_data.title
        img_path = f'game/assets/{init_data.background}'
        self.background_img = load_image(img_path)
        self.theme_path = str(resolve_project_path(f"game/environments/themes/{init_data.theme}.json"))

    def create_ui(self):
        pass

    def on_ui_event(self, event):
        if event.type == NEXT_ENV_CONFIRMED:
            self.game_manager.change_env(self.env_data.env.init.next_env)
        if event.type == RESET_ENV_CONFIRMED:
            self.reset()
        if event.type == LEVEL_COMPLETED:
            next_env = getattr(self.env_data.env.init, "next_env", None)
            self.game_manager.mark_level_completed(
                self.title,
                next_env,
            )
            if next_env:
                self.game_manager.change_env(next_env)

    def update_frame(self, delta_time):
        # Per-frame updates (e.g., typing effects, animations).
        pass
     
    # Gets the resolution set in 'window/display.py' from the game manager
    def render_background(self):
        width = self.game_manager.display.resolution[0]
        height = self.game_manager.display.resolution[1]
        UIImage(relative_rect=Rect((0,0),(width,height)), image_surface=self.background_img, manager=self.ui_manager)
        
    # This is called when the screen is to be reset to recreate ui elements, it can also change the level from a level file
    def reset(self):
        self.ui_manager.clear_and_reset()
        self.render_background()
        self.create_ui()
 
# This contains all of the info that will be consistent accross each of the levels
class GameEnv(BaseEnvironment):
    BOARD_PANEL_PADDING = 28
    BOARD_PANEL_MIN_SCALE = 1
    PANEL_SHADOW_SPREAD = 10
    BLOCKS_PANEL_MIN_WIDTH = 700
    BLOCKS_PANEL_WIDTH_RATIO = 0.39
    DEBUG_MENU_BUTTON_MARGIN = 18
    DEBUG_MENU_BUTTON_SIZE = (120, 44)
    CONFIRM_PANEL_SIZE = (520, 220)

    # The BaseEnvironment in 'environments/base.py', init's the level file
    def __init__(self, level_file): # This file is where the env gets/loads inital data for the level
        super().__init__(level_file)

    def get_board_grid_size(self):
        for map_layer in self.env_data.board.map.__dict__.values():
            csv_layout = import_map_layout(map_layer[0])
            if csv_layout:
                return len(csv_layout[0]), len(csv_layout)
        raise RuntimeError("Board map data is empty.")

    def get_board_panel_size(self, max_width, max_height):
        grid_width, grid_height = self.get_board_grid_size()
        max_scale_x = max_width // (grid_width * IMG_TILE_SIZE)
        max_scale_y = max_height // (grid_height * IMG_TILE_SIZE)
        tile_scale = max(self.BOARD_PANEL_MIN_SCALE, min(max_scale_x, max_scale_y))

        board_width = grid_width * IMG_TILE_SIZE * tile_scale
        board_height = grid_height * IMG_TILE_SIZE * tile_scale
        return (
            board_width + (self.BOARD_PANEL_PADDING * 2),
            board_height + (self.BOARD_PANEL_PADDING * 2),
        )

    def create_shadow_panel(self, panel_pos, panel_size):
        shadow_rect = Rect(
            (panel_pos[0] - self.PANEL_SHADOW_SPREAD, panel_pos[1] - self.PANEL_SHADOW_SPREAD),
            (
                panel_size[0] + (self.PANEL_SHADOW_SPREAD * 2),
                panel_size[1] + (self.PANEL_SHADOW_SPREAD * 2),
            ),
        )
        UIPanel(
            relative_rect=shadow_rect,
            manager=self.ui_manager,
            object_id="#panel_shadow",
            starting_height=0,
        )

    def create_ui(self):
        outer_margin = 40
        panel_gap = 20
        available_width = SCREEN_WIDTH - (outer_margin * 2) - panel_gap
        available_height = SCREEN_HEIGHT - (outer_margin * 2)

        blocks_width = max(
            self.BLOCKS_PANEL_MIN_WIDTH,
            int(available_width * self.BLOCKS_PANEL_WIDTH_RATIO),
        )
        board_max_width = available_width - blocks_width
        board_size = self.get_board_panel_size(board_max_width, available_height)
        board_pos = (outer_margin, outer_margin + ((available_height - board_size[1]) // 2))
        blocks_pos = (SCREEN_WIDTH - outer_margin - blocks_width, outer_margin)
        blocks_size = (blocks_width, available_height)

        self.create_shadow_panel(board_pos, board_size)
        self.create_shadow_panel(blocks_pos, blocks_size)

        # Takes data passed through and starts creating the tiles/player/goal and more in the future possibly
        self.board = Board(
            panel_pos=board_pos,
            panel_size=board_size,
            board_data=self.env_data.board, 
            manager=self.ui_manager)

        # A temporary placeholder of where our code blocks could be placed and initalised when finished programming
        self.blocks = CodeBlocks(
            panel_pos=blocks_pos,
            panel_size=blocks_size,
            manager=self.ui_manager, 
            player=self.board.player,
            allowed_blocks=self.get_allowed_blocks())
        
        # Setting level text from getting the env title
        LevelText(
            panel_pos=(0,0), 
            panel_size= (100, 50),
            text=self.title, 
            manager=self.ui_manager)

        self.debug_menu_button = None
        self.confirmation_panel = None
        if getattr(self.game_manager, "debug", False):
            self.debug_menu_button = UIFactory.button(
                pos=(self.DEBUG_MENU_BUTTON_MARGIN, SCREEN_HEIGHT - self.DEBUG_MENU_BUTTON_MARGIN),
                size=self.DEBUG_MENU_BUTTON_SIZE,
                text="Menu",
                manager=self.ui_manager,
                object_id="#edit_button",
                anchor="bottomleft",
            )
        
    def on_ui_event(self, event):
        # using the ui super event from base.py to check for next/reset env 
        super().on_ui_event(event)
        if event.type == RESET_ENV_REQUESTED:
            self.open_confirmation_panel(
                title="Reset level?",
                message="Your current script will be cleared and the level will restart.",
                confirm_event_type=RESET_ENV_CONFIRMED,
            )
            return
        if event.type == MENU_ENV_REQUESTED:
            self.open_confirmation_panel(
                title="Return to menu?",
                message="Leave this level and go back to the main menu.",
                confirm_event_type=MENU_ENV_CONFIRMED,
            )
            return
        if event.type == MENU_ENV_CONFIRMED:
            self.game_manager.change_env("Main Menu")
            return
        if self.debug_menu_button and self.debug_menu_button.on_click(event):
            menu_event = pygame.event.Event(MENU_ENV_REQUESTED)
            pygame.event.post(menu_event)

    def open_confirmation_panel(self, title, message, confirm_event_type):
        if self.confirmation_panel and self.confirmation_panel.alive():
            self.confirmation_panel.kill()

        panel_x = (SCREEN_WIDTH - self.CONFIRM_PANEL_SIZE[0]) // 2
        panel_y = (SCREEN_HEIGHT - self.CONFIRM_PANEL_SIZE[1]) // 2
        self.confirmation_panel = ConfirmationPanel(
            panel_pos=(panel_x, panel_y),
            panel_size=self.CONFIRM_PANEL_SIZE,
            title=title,
            message=message,
            confirm_event_type=confirm_event_type,
            manager=self.ui_manager,
        )
        

    def get_allowed_blocks(self):
        systems_data = getattr(self.env_data, "systems", None)
        if systems_data is None:
            return None
        return getattr(systems_data, "allowed_blocks", None)
        
        
