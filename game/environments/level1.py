from game.environments.base import GameEnv
from game.app.panels import DialoguePanel
from game.core.constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Level1(GameEnv):
    def __init__(self):
        super().__init__(level_file="start")

    def create_ui(self):
        super().create_ui()
        # Here we will make each level different to teach the user about each new thing individually (maybe?)
        

    def on_ui_event(self, event):
        super().on_ui_event(event)

    def update_frame(self, delta_time):
        pass
