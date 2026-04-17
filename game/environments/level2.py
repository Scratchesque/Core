from game.environments.base import GameEnv

# making each file seperate again cause i realise sometimes there will be different elements being rendered depending on the level, 
# so like this should be easier to make changes on individual levels
class Level2(GameEnv):
    def __init__(self):
        super().__init__(level_file="level1")

    def create_ui(self):
        super().create_ui()

    def on_ui_event(self, event):
        super().on_ui_event(event)

    def update_frame(self, delta_time):
        pass
