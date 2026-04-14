from game.core.constants import *
from game.environments.base import BaseEnvironment
from game.core.ui import UIFactory

 
class LevelSelect(BaseEnvironment):
    # The BaseEnvironment in 'environments/base.py', init's the level file 'environments/data/menu.json'
    def __init__(self, level_file="menu"): # This file is where the env gets/loads inital data for the level
        super().__init__(level_file)

    # This is called in 'base.py' at reset() 
    def create_ui(self):
        # i can make a proper version of the main menu loading in some time, not a priority but it does need fixing
        self.buttons = []  # this need to be reset unless every time the ui is created it adds more buttons to the list
        # Temp for now but gets list of all envs   
        self.levels = [env.title for env in self.game_manager.envs_list if env.title != self.title]

        # Then lists them on the screen
        x = 500
        for level in self.levels:
            self.buttons.append(UIFactory.button_img(
                pos=(x, SCREEN_HEIGHT // 2),
                size=(300, 100),
                image_path='game/assets/menu/button.png',
                text=level,
                manager=self.ui_manager,
                object_id='#transparent_button'))
            x += (350)

        self.quit_button = UIFactory.button((850, 800), (300, 100), "Quit", self.ui_manager, object_id="quit")

    def on_ui_event(self, event):
        # When a button is pressed for the environments, change to that title environemt
        for x in range(len(self.buttons)):
            if self.buttons[x].button.on_click(event):
                title = self.levels[x]
                self.game_manager.change_env(title)
                print(f"Pressed {title}!")

        # if quiting call quit in game manager
        quit_result = self.quit_button.on_click(event)
        if quit_result:
            self.game_manager.change_env("QUIT")

    def update_frame(self, delta_time):
        pass
