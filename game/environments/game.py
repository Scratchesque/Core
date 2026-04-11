from game.app.board import Board
from game.app.elements import *
from game.core.constants import *
from game.core.ui import UIFactory
from game.environments.base import BaseEnvironment
from game.app.code_blocks import Panel

from pygame import Rect
from pygame_gui.windows import UIConfirmationDialog, UIMessageWindow
from pygame_gui.elements import UILabel

class GameEnv(BaseEnvironment):
    def __init__(self, level_file="start"): # this is the starting file 
        super().__init__(level_file)

    def create_ui(self):
        # Board: (50,50) - (1200, 980)
        self.board = Board(
            board_pos=(50,50),
            board_size=(1200, SCREEN_HEIGHT-50*2),
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
            "To complete this level, be built different!",
            self.ui_manager,
        )
        

    def on_ui_event(self, event):   
        if self.board.carrot.collision_check(self.board.player):
            if self.board.complete == False:
                self.board.complete = True
                rect = Rect((SCREEN_WIDTH // 2, SCREEN_HEIGHT //2), (300, 300)) 
                UIConfirmationDialog(rect, "You Win!", self.ui_manager)

        if self.menu_button.on_click(event):
            self.game_manager.change_env("Main Menu")

        if event.type == UI_CONFIRMATION_DIALOG_CONFIRMED: # here you check if it goes to the next level by rerendering, or using something else, also sets it back to the start
            try:
                self.reset(self.env_data.env.next_level_data)
            except:
                self.game_manager.change_env("Main Menu")
                self.reset()

    def update_frame(self, delta_time):
        pass
