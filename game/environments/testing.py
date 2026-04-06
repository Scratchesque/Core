from game.window.ui_windows import *
from game.core.constants import *
from game.environments.base import BaseEnvironment
from game.core.ui import UIFactory, TypingTextBox
from pygame_gui.elements import UIButton
from game.core.player import Player

class TestingEnv(BaseEnvironment):
    def __init__(self):
        title = "Testing"
        background_hex = "background.jpg"
        theme = "level1"
        super().__init__(title, background_hex, theme)

    def create_ui(self, ui_manager):
        self.player = Player((5, int(SCREEN_HEIGHT/2)), ui_manager)

        self.test_button = UIFactory.button(
            (SCREEN_WIDTH // 2+75, SCREEN_HEIGHT - 40),
            (100, 50),
            "Movement",
            ui_manager,
            object_id="move",
            anchor="midbottom",
        )

        self.quit_buttom = UIFactory.button(
            (SCREEN_WIDTH // 2-75, SCREEN_HEIGHT - 40),
            (100, 50),
            "Quit",
            ui_manager,
            object_id="quit",
            anchor="midbottom",
        )

    def on_ui_event(self, event):
        ui_manager = self.game_manager.display.ui_manager
        if self.test_button.on_click(event):
            MovementWindow(pygame.Rect((150, 150), (250, 250)), ui_manager, self.player)
        if self.quit_buttom.on_click(event):
            self.game_manager.change_env("QUIT")

    def update_frame(self, delta_time):
        self.player.update(delta_time)
