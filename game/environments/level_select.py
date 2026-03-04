from game.core.constants import *
from game.environments.base import BaseEnvironment
from game.environments.level1 import Level1
from game.environments.level2 import Level2
from game.window.ui import TypingTextBox, UIFactory


class LevelSelect(BaseEnvironment):
    def __init__(self, title):
        background_hex = "ffffff"
        theme = "level1"
        super().__init__(title, background_hex, theme)

        self.reset()
        
    def reset(self):
        self.levels = ['Level 1', 'Level 2'] 
        self.buttons = [] # this need to be reset unless every time the ui is created it adds more buttons to the list
        
    def create_ui(self, manager):
        self.reset()
        
        x = 50
        for level in self.levels:
            self.buttons.append(
                UIFactory.button(
                    (x, SCREEN_HEIGHT // 2), (100, 50), level, manager
                )
            )
            x += 150

        self.quit_button = UIFactory.button((250, 175), (150, 50), 'Quit', manager, object_id='quit')

    def on_ui_event(self, event):
        for x in range(len(self.buttons)):
            if self.buttons[x].on_click(event):
                title = self.levels[x]
                self.window.change_env(title)
                print(f"Pressed {title}!")
            
        quit_result = self.quit_button.on_click(event)
        if quit_result:
            print('Quit Game!')
            return False

        # quit_result = self.quit_button.on_click(event)
        # url_clicked = self.dialogue_box.url_click(event)
        # if url_clicked:
        #     print("Pressed url box!")
        # if quit_result:
        #     print("Quit Game!")
        #     return False
        # pygame.quit() # try not to exit from inside the environment but if you have to there is an exception so it doesnt crash

    def update_frame(self, delta_time):
        pass
        # self.dialogue_box.update_typing(delta_time)
