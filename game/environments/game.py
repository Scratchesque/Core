from game.app.board import Board
from game.app.elements import *
from game.core.constants import *
from game.core.ui import UIFactory
from game.environments.base import BaseEnvironment
from game.app.code_blocks import Panel

from pygame import Rect
from pygame_gui.elements import UILabel

class GameEnv(BaseEnvironment):
    def __init__(self, level_file="start"): # this is the starting file 
        super().__init__(level_file)

    def create_ui(self):
        # Board: (50,50) - (1200, 980)
        self.board = Board(
            env_data=self.env_data.board, 
            manager=self.ui_manager)

        # Code Blocks: (1200,50) - (1920,1080)
        # here implement the blocks that will be generated to interact with the board somehow?
        self.test = Panel(
            board_pos=(1245,50),
            board_size=(SCREEN_WIDTH-1200-50*2, SCREEN_HEIGHT-50*2),
            env_data=self.env_data.board, 
            manager=self.ui_manager, player=self.board.player)
        
        # FOR SOME REASON PYGAME NOT ACCTUALY MAKE SIZE 100, 100, ITS 95, 95

        # other misc stuff
        self.menu_button = UIFactory.button(
            (500, 500),
            (100, 50), 
            "Menu", 
            self.ui_manager, container=self.test.panel_container)

        # Level Text
        rect = Rect((0,0), (100, 50)) 
        UILabel(rect, self.title, self.ui_manager)

        # Pop up telling user what to do
        size = (300, 300)
        
        self.dialogue_panel = DialoguePanel(
            (SCREEN_WIDTH // 2- size[0]//2, SCREEN_HEIGHT //2- size[1]//2),
            size,
            self.env_data.story.intro_dialogue,
            self.ui_manager,
        )
        

    def on_ui_event(self, event):   
        # code below is not the best it only checks if a dialouge created from another file has been clicked, and if so it tries to reset to the next level
        # but if theres any problems once in this try loop, then all errors exit out silently to main menu which isnt that nice  
        if event.type == UI_CONFIRMATION_DIALOG_CONFIRMED:
            try:
                self.reset(self.env_data.env.next_level_data)
            except:
                self.game_manager.change_env("Main Menu")
                self.reset()

    def update_frame(self, delta_time):
        pass
