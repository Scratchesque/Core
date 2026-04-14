from game.window.ui_windows import *
from game.core.constants import *
from game.environments.base import BaseEnvironment
from game.app.base import MainApp

class TestingEnv(BaseEnvironment):
    def __init__(self):
        title = "Testing"
        background_file = "menu/background.png"
        theme_file = "level1"
        level_file = "intro"
        super().__init__(title, background_file, theme_file, level_file)

    def create_ui(self, ui_manager):
        self.game = MainApp(self.level_data, ui_manager)

    def on_ui_event(self, event):
        self.game.board.on_ui_event(event)
        if event.type == UI_CONFIRMATION_DIALOG_CONFIRMED:
            self.game_manager.change_env("BACK")

    def update_frame(self, delta_time):
        pass
