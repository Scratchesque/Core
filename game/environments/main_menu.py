from game.core.constants import *
from game.environments.base import BaseEnvironment
from game.core.ui import UIFactory


class LevelSelect(BaseEnvironment):
    def __init__(self):
        super().__init__(level_file="menu")

    def create_ui(self, ui_manager):
        # i can make a proper version of the main menu loading in some time, not a priority but it does need fixing
        self.buttons = []  # this need to be reset unless every time the ui is created it adds more buttons to the list
        self.levels = [env.title for env in self.game_manager.envs_list if env.title != self.title]

        x = 500
        for level in self.levels:
            self.buttons.append(UIFactory.button_img((x, SCREEN_HEIGHT // 2), (300, 100), 'game/assets/menu/button.png', level, ui_manager, object_id='#trasparent'))
            x += (350)

        self.quit_button = UIFactory.button((850, 800), (300, 100), "Quit", ui_manager, object_id="quit")

    def on_ui_event(self, event):
        for x in range(len(self.buttons)):
            if self.buttons[x].button.on_click(event):
                title = self.levels[x]
                self.game_manager.change_env(title)
                print(f"Pressed {title}!")

        quit_result = self.quit_button.on_click(event)
        if quit_result:
            self.game_manager.change_env("QUIT")

    def update_frame(self, delta_time):
        pass
