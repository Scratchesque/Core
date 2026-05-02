from pygame import Rect, KEYUP, K_ESCAPE, Color
from pygame_gui.elements import UIPanel

from game.app.block_interpreter import InterpreterPanel
from game.app.board import Board
from game.app.code_blocks import CodeBlocks
from game.app.panels import ConfirmationPanel, LevelText, SettingsMenu, MessagePanel
from game.core.images import load_image
from game.core.paths import resolve_project_path
from game.core.constants import *
from game.core.events import *
from game.support.files import import_map_layout, load_json
from game.support.ui import UIFactory


# New environemnts/screens that are loaded through the game manager should inherit this class
class BaseEnvironment:
    # When an environemnt using this class init's, it loads all relevant data from 'environments/data/{level_file}.json" to be used
    def __init__(self, level_file):
        root_dir = "game/environments/data/"
        default_data = load_json(f"{root_dir}default.json")
        self.env_data = load_json(f"{root_dir}{level_file}.json")

        if not hasattr(default_data, "env"):
            raise ValueError("Default environment data is missing an 'env' section.")
        if not hasattr(self.env_data, "env"):
            raise ValueError(f"Environment data for '{level_file}' is missing an 'env' section.")

        env_data = self.env_data.env
        self.title = env_data.title
        self.theme_path = str(resolve_project_path(f"game/environments/themes/{env_data.theme}.json"))

        self.background_colour = Color(f'#{default_data.env.background}')
        if hasattr(env_data, 'background'):
            self.background_colour = Color(f'#{env_data.background}')

    def create_ui(self):
        pass

    def on_ui_event(self, event):
        if event.type == QUIT_EMV_CONFIRMED:
            self.game_manager.change_env('QUIT')
        if event.type == NEXT_ENV_CONFIRMED:
            next_env = getattr(self.env_data.env, "next_env", None)
            if next_env:
                self.game_manager.change_env(next_env)
        if event.type == RESET_ENV_CONFIRMED:
            self.game_manager.change_env('RESET')
        if event.type == LEVEL_COMPLETED:
            next_env = getattr(self.env_data.env, "next_env", None)
            self.game_manager.mark_level_completed(
                self.title,
                next_env,
            )
            if next_env:
                self.game_manager.change_env(next_env)

    def update_frame(self, delta_time):
        # Per-frame updates (e.g., typing effects, animations).
        pass
     
    # This is called when the screen is to be reset to recreate ui elements, it can also change the level from a level file
    def reset(self):
        self.ui_manager.clear_and_reset()
        self.game_manager.display.create_cursor()
        self.create_ui()
 
# This contains all of the info that will be consistent accross each of the levels
class GameEnv(BaseEnvironment):
    BOARD_PANEL_PADDING = 28
    BOARD_PANEL_MIN_SCALE = 1
    PANEL_SHADOW_SPREAD = 10
    BLOCKS_PANEL_MIN_WIDTH = 700
    BLOCKS_PANEL_WIDTH_RATIO = 0.39
    CONFIRM_PANEL_SIZE = (550, 220)

    def get_board_grid_size(self):
        for map_layer in self.env_data.map.__dict__.values():
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
            starting_height=1,
        )

    def configure_layout(self):
        outer_margin = 40
        panel_gap = 20
        available_width = SCREEN_WIDTH - (outer_margin * 2) - panel_gap
        available_height = SCREEN_HEIGHT - (outer_margin * 2)

        blocks_width = max(
            self.BLOCKS_PANEL_MIN_WIDTH,
            int(available_width * self.BLOCKS_PANEL_WIDTH_RATIO),
        )
        board_max_width = available_width - blocks_width

        self.board_size = self.get_board_panel_size(board_max_width, available_height)
        self.board_pos = (outer_margin, outer_margin + ((available_height - self.board_size[1]) // 2))
        self.blocks_size = (blocks_width, available_height)
        self.blocks_pos = (SCREEN_WIDTH - outer_margin - blocks_width, outer_margin)

    def create_ui(self):
        self.configure_layout()

        self.create_shadow_panel(self.board_pos, self.board_size)

        # Takes data passed through and starts creating the tiles/player/goal
        self.board = Board(
            panel_pos=self.board_pos,
            panel_size=self.board_size,
            env_data=self.env_data, 
            manager=self.ui_manager)
        
        # Setting level text from getting the env title
        LevelText(
            panel_pos=(10,-5), 
            panel_size=(220, 50),
            text=self.title, 
            manager=self.ui_manager)

        self.confirmation_panel = None

        square_size = 30
        self.settings_button = UIFactory.button_img(
            pos=(SCREEN_WIDTH-square_size-5, 5),
            size=(square_size,square_size),
            text="",
            image_path='game/assets/levels/hamburger_icon.png',
            manager=self.ui_manager,
            object_id="#transparent"
        )
        self.settings_panel = None
        
    def on_ui_event(self, event):
        super().on_ui_event(event)
        if (event.type == KEYUP and event.key == K_ESCAPE) or self.settings_button.on_click(event):
            if self.settings_panel is None or not self.settings_panel.alive():
                self.settings_panel = SettingsMenu(
                    panel_size=(200,250), 
                    manager=self.ui_manager
                )
            else:
                self.settings_panel.kill()
                self.settings_panel = None
        if event.type == QUIT_EMV_REQUESTED:
            self.open_confirmation_panel(
                title="Quit game?",
                message="Exit the program on this level.",
                confirm_event_type=QUIT_EMV_CONFIRMED,
            )
            return
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
    
    def update_frame(self, delta_time):
        self.check_level_complete()
        
    def check_level_complete(self):
        if self.board.completed_level == False:
            player = self.board.player
            goal = self.board.goal
            if player.goal_check(goal):
                self.board.completed_level = True
                info_size = (275,160)
                info_pos = ((SCREEN_WIDTH-info_size[0])//2), ((SCREEN_HEIGHT-info_size[1])//2)
                MessagePanel(panel_pos=info_pos,
                    panel_size=info_size,
                    title="You Win!",
                    message="Loading next level...",
                    manager=self.ui_manager)
                level_complete_event = pygame.event.Event(LEVEL_COMPLETED)
                pygame.event.post(level_complete_event)
                return
        
            if player.current_health <= 0:
                info_size = (275,160)
                info_pos = ((SCREEN_WIDTH-info_size[0])//2), ((SCREEN_HEIGHT-info_size[1])//2)
                MessagePanel(panel_pos=info_pos,
                    panel_size=info_size,
                    title="Level Reset!",
                    message="No energy remaining",
                    manager=self.ui_manager)
                reset_event = pygame.event.Event(RESET_ENV_CONFIRMED)
                pygame.event.post(reset_event)
                return

class BlockEnv(GameEnv):
    
    def create_ui(self):
        super().create_ui()
        
        self.create_shadow_panel(self.blocks_pos, self.blocks_size)
    
        # Where our code blocks will be placed and initalised
        self.blocks = CodeBlocks(
            panel_pos=self.blocks_pos,
            panel_size=self.blocks_size,
            manager=self.ui_manager, 
            player=self.board.player,
            allowed_blocks=self.get_allowed_blocks(),
        )    
class InterpreterEnv(BlockEnv):

    def create_ui(self):
        super().create_ui()

        InterpreterPanel(
            panel_pos=self.blocks_pos,
            panel_size=self.blocks_size, 
            manager=self.ui_manager,
            code_blocks=self.blocks,
            level_title=self.title
        )
