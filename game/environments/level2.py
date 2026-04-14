from game.environments.base import GameEnv
from game.app.panels import DialoguePanel
from game.core.ui import UIFactory
from game.core.constants import *

# making each file seperate again cause i realise sometimes there will be different elements being rendered depending on the level, 
# so like this should be easier to make changes on individual levels
class Level2(GameEnv):
    def __init__(self):
        super().__init__(level_file="level1")

    def create_ui(self):
        super().create_ui()
        # This is temporarily in the test_panel container untill it finds a proper place on the screen or we replace it
        # As if its not in a container, it can get lost between the layers
        self.menu_button = UIFactory.button(
            pos=(500, 500),
            size=(100, 50), 
            text="Menu", 
            manager=self.ui_manager, 
            container=self.blocks.panel_container)


        # Pop up dialouge telling user what to do from the environment data loaded in __init__
        size = (300, 300)
        self.dialogue_panel = DialoguePanel(
            (SCREEN_WIDTH // 2- size[0]//2, SCREEN_HEIGHT //2- size[1]//2),
            size,
            self.env_data.story.intro_dialogue,
            self.ui_manager)
        

    def on_ui_event(self, event):
        super().on_ui_event(event)
        if self.menu_button.on_click(event):
            self.game_manager.change_env("Main Menu")

    def update_frame(self, delta_time):
        pass
