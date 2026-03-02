from game.environments.base import BaseEnvironment
from game.core.constants import *
from game.window.ui import UIFactory, TypingTextBox

class Level1(BaseEnvironment):
    def __init__(self, title):
        background_hex = 'ffffff'
        theme = 'level1'
        super().__init__(title, background_hex, theme)

    def setup(self, manager):
        self.title_label = UIFactory.label((20, 20), (660, 30), 'Title', manager, object_id='title')
        self.dialogue_box = TypingTextBox(
            (20, 60),
            (660, 160),
            "<b>Guide</b>: Welcome. This is a small dialogue box example.",
            manager,
            object_id='dialogue',
            typing_speed=30
        )
        self.quit_button = UIFactory.button(
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40),
            (100, 50),
            'Quit',
            manager,
            object_id='quit',
            anchor='midbottom'
        )
    
    def loop(self, event):
        pass
    
    def on_ui_event(self, event):
        quit_result = self.quit_button.button_pressed(event)
        if quit_result:
            print('Quit Game!')
            return False
            # pygame.quit() # try not to exit from inside the environment but if you have to there is an exception so it doesnt crash  

    def update(self, delta_time):
        self.dialogue_box.update_typing(delta_time)
        
