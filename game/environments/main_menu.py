from game.core.constants import *
from game.environments.base import BaseEnvironment
from game.core.ui import UIFactory
from game.app.panels import DialoguePanel

 
class LevelSelect(BaseEnvironment):
    # The BaseEnvironment in 'environments/base.py', init's the level file 'environments/data/menu.json'
    def __init__(self, level_file="menu"): # This file is where the env gets/loads inital data for the level
        super().__init__(level_file)
        self.panel_texts = [
            "Welcome to Rabbit Rush, your introduction to computer science.\nKevin the Bunny has lost his Carrots/Apples and abilities.\nIt's your goal to gain them back.\nLearn how to read and implement code to help Kevin reach his goal.",
            "How to play:\nDrag and drop the function you want Kevin to execute, your goal is to get Kevin to reach his lost carrot/apple.",
            "Level types:\nThere are two types of levels:\n1. Introduction Levels: introduce “abilities” act as where users learn fundamentals of coding\n2. Practical Levels: users put what they have learned in practice."
        ]

    # This is called in 'base.py' at reset() 
    def create_ui(self):
        # we can change how all the elements look like
        self.dialouge_pos = 0
        self.generate_dialouge()
        
        self.quit_button = UIFactory.button((SCREEN_WIDTH // 2, SCREEN_HEIGHT-100), (300, 100), "Quit", self.ui_manager, object_id="quit", anchor='midbottom')

    def on_ui_event(self, event):
        # When a button is pressed for the environments, change to that title environemt
        if event.type == DIALOGUE_SELECTED:
            if self.dialouge_pos < len(self.panel_texts):
                self.generate_dialouge()
            else:
                self.game_manager.change_env("Start")

        quit_result = self.quit_button.on_click(event)
        if quit_result:
            self.game_manager.change_env("QUIT")

    def generate_dialouge(self):
        size = (500,600)
        DialoguePanel(
            panel_pos=(SCREEN_WIDTH // 2- size[0]//2, SCREEN_HEIGHT //2- size[1]//2),
            panel_size=size,
            text=self.panel_texts[self.dialouge_pos],
            manager=self.ui_manager)

        self.dialouge_pos += 1

    def update_frame(self, delta_time):
        pass
