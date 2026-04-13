from game.environments.base import GameEnv
from game.app.panels import DialoguePanel
from pygame_gui._constants import *
from game.core.ui import UIFactory
from game.core.constants import *

# making each file seperate again cause i realise sometimes there will be different elements being rendered depending on the level, 
# so like this should be easier to make changes on individual levels
class Level1(GameEnv):
    def __init__(self):
        super().__init__(level_file="start")

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
        if self.menu_button.on_click(event):
            self.game_manager.change_env("Main Menu")

        # maybe put below the code in a super thing in GameEnv class, cause then it consistenly completes the level the same and goes next
        
        # Code below is not the best as it only checks if a dialouge created from another file 'app/board.py' in process_event() has been clicked, and if so it tries to reset to the next level
        # But if theres any problems once inside the try loop, then all errors exit out silently to main menu which isnt that nice 
        # if event.type == UI_CONFIRMATION_DIALOG_CONFIRMED:
        #     try:
        #         self.reset(self.env_data.env.next_level_data)
        #     except:
        #         self.game_manager.change_env("Main Menu")
        #         self.reset()

    def update_frame(self, delta_time):
        pass
