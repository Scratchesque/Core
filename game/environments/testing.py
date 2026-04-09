from game.window.ui_windows import *
from game.core.constants import *
from game.environments.base import BaseEnvironment
from game.core.ui import UIFactory, TypingTextBox
from pygame_gui.elements import UIButton
from game.board.base import GameBoard

class TestingEnv(BaseEnvironment):
    def __init__(self):
        title = "Testing"
        background_hex = "menu/background.png"
        theme = "level1"
        super().__init__(title, background_hex, theme)

    def create_ui(self, ui_manager):
        self.board = GameBoard((50,50), SCREEN_HEIGHT-100, 5, ui_manager)

    def on_ui_event(self, event):
        self.board.on_ui_event(event)
        if event.type == UI_CONFIRMATION_DIALOG_CONFIRMED:
            self.game_manager.change_env("BACK")

    def update_frame(self, delta_time):
        pass
