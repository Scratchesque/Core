from game.environments.base import BaseEnvironment
from game.core.constants import *
from game.window.ui import UIFactory

class Level2(BaseEnvironment):
    def __init__(self, title):
        background_hex = '000000'
        theme = 'level2'
        super().__init__(title, background_hex, theme)

    def create_ui(self, manager):
        
        self.quit_button = UIFactory.button((250, 175), (150, 50), 'Quit', manager, object_id='quit')
        self.back_button = UIFactory.button((100, 175), (100, 50), 'Back', manager)

    def on_ui_event(self, event):
        quit_result = self.quit_button.on_click(event)
        back_result = self.back_button.on_click(event)
        if quit_result:
            print('Quit Game!')
            return False
        if back_result:
            self.window.change_env('Main Menu')
    
    def update_frame(self, delta_time):
        # Per-frame updates (e.g., typing effects, animations).
        pass
