from game.environments.base import GameEnv
from game.app.panels import DialoguePanel
from game.core.constants import *

# making each file seperate again cause i realise sometimes there will be different elements being rendered depending on the level, 
# so like this should be easier to make changes on individual levels
class Level1(GameEnv):
    def __init__(self):
        super().__init__(level_file="start")

    def create_ui(self):
        super().create_ui()
        # Pop up dialouge telling user what to do from the environment data loaded in __init__
        size = (300, 300)
        self.dialogue_panel = DialoguePanel(
            (SCREEN_WIDTH // 2- size[0]//2, SCREEN_HEIGHT //2- size[1]//2),
            size,
            self.env_data.story.intro_dialogue,
            self.ui_manager)
        

    def on_ui_event(self, event):
        super().on_ui_event(event)

    def update_frame(self, delta_time):
        pass
