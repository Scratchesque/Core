from game.core.constants import *
from game.environments.base import BaseEnvironment
from game.core.ui import UIFactory
from game.app.panels import DialoguePanel

 
class LevelSelect(BaseEnvironment):
    # The BaseEnvironment in 'environments/base.py', init's the level file 'environments/data/menu.json'
    def __init__(self, level_file="menu"): # This file is where the env gets/loads inital data for the level
        super().__init__(level_file)

    # This is called in 'base.py' at reset() 
    def create_ui(self):
        # we can change how all the elements look like
        size = (500,500)
        DialoguePanel(
            panel_pos=(SCREEN_WIDTH // 2- size[0]//2, SCREEN_HEIGHT //2- size[1]//2),
            panel_size=size,
            text="Welcome to Rabbit Rush, your introduction to computer science.\nKevin the Bunny has lost his Carrots/Apples and abilities.\nIt's your goal to gain them back.\nLearn how to read and implement code to help Kevin reach his goal.",
            manager=self.ui_manager)

        self.quit_button = UIFactory.button((SCREEN_WIDTH // 2, SCREEN_HEIGHT-150), (300, 100), "Quit", self.ui_manager, object_id="quit", anchor='midbottom')

    def on_ui_event(self, event):
        # When a button is pressed for the environments, change to that title environemt
        if event.type == DIALOGUE_SELECTED:
            self.game_manager.change_env("Start")

        # if quiting call quit in game manager
        quit_result = self.quit_button.on_click(event)
        if quit_result:
            self.game_manager.change_env("QUIT")

    def update_frame(self, delta_time):
        pass
