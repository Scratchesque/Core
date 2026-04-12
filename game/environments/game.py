from game.app.board import Board
from game.app.panels import DialoguePanel, LevelText
from game.core.constants import *
from game.core.ui import UIFactory
from game.environments.base import BaseEnvironment
from game.app.code_blocks import CodeBlocks
from pygame_gui._constants import *

# This contains all of the  
class GameEnv(BaseEnvironment):
    # The BaseEnvironment in 'environments/base.py', init's the level file 'environments/data/start.json'
    def __init__(self, level_file="start"): # This file is where the env gets/loads inital data for the level
        super().__init__(level_file)

    def create_ui(self):
        # panel_pos and panel_size are temporary values but can be changed freely to fit to screen how we'd like

        # Takes data passed through and starts creating the tiles/player/goal and more in the future possibly
        self.board = Board(
            panel_pos=(50,50),
            panel_size=(1200,980),
            board_data=self.env_data.board, 
            manager=self.ui_manager)

        # A temporary placeholder of where our code blocks could be placed and initalised when finished programming
        self.test = CodeBlocks(
            panel_pos=(1250,50),
            panel_size=(620, 980),
            manager=self.ui_manager, 
            player=self.board.player)
        
        # This is temporarily in the test_panel container untill it finds a proper place on the screen or we replace it
        # As if its not in a container, it can get lost between the layers
        self.menu_button = UIFactory.button(
            pos=(500, 500),
            size=(100, 50), 
            text="Menu", 
            manager=self.ui_manager, 
            container=self.test.panel_container)

        # Setting level text from getting the env title
        # With the object id setting the image background for the label in 'environments/themes/game.json'
        
        LevelText(
            panel_pos=(0,0), 
            panel_size= (100, 50),
            text=self.title, 
            manager=self.ui_manager)

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
        
        # Code below is not the best as it only checks if a dialouge created from another file 'app/board.py' in process_event() has been clicked, and if so it tries to reset to the next level
        # But if theres any problems once inside the try loop, then all errors exit out silently to main menu which isnt that nice 
        if event.type == UI_CONFIRMATION_DIALOG_CONFIRMED:
            try:
                self.reset(self.env_data.env.next_level_data)
            except:
                self.game_manager.change_env("Main Menu")
                self.reset()

    def update_frame(self, delta_time):
        pass
