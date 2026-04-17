from game.environments.base import GameEnv


class Level3(GameEnv):
    def __init__(self):
        super().__init__(level_file="level2")

    def create_ui(self):
        super().create_ui()

    def on_ui_event(self, event):
        super().on_ui_event(event)

    def update_frame(self, delta_time):
        pass
