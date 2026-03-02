from game.environments.base import BaseEnvironment
from game.core.constants import *
from game.window.ui import *

class Level2(BaseEnvironment):
    def __init__(self, title):
        background_hex = '000000'
        theme = 'level2'
        super().__init__(title, background_hex, theme)

    def setup(self, manager):
        
        self.quit_button = Button((250, 175), (150, 50), 'Quit', manager)
    
    def loop(self, event):
        quit_result = self.quit_button.button_pressed(event)
        if quit_result:
            print('Quit Game!')
            return False
