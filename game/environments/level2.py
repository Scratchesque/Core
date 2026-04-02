from game.core.constants import *
from game.core.ui import UIFactory


class Level2(BaseEnvironment):
    def __init__(self):
        title = "Level 2"
        background_hex = "000000"
        theme = "level2"
        super().__init__(title, background_hex, theme)

    def create_ui(self, ui_manager):

        self.quit_button = UIFactory.button((250, 175), (150, 50), "Quit", ui_manager, object_id="quit")
        self.back_button = UIFactory.button((100, 175), (100, 50), "Back", ui_manager)

    def on_ui_event(self, event):
        quit_result = self.quit_button.on_click(event)
        back_result = self.back_button.on_click(event)
        if quit_result:
            print("Quit Game!")
            return False
        if back_result:
            self.game_manager.change_env("Main Menu")

    def update_frame(self, delta_time):
        # Per-frame updates (e.g., typing effects, animations).
        pass
