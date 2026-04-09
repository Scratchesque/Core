from game.app.board import Board
from game.app.elements import *
from game.core.constants import *
from game.core.ui import UIFactory
from game.environments.base import BaseEnvironment

from pygame import Rect
from pygame_gui.windows import UIConfirmationDialog, UIMessageWindow
from pygame_gui.elements import UILabel

class TestingEnv(BaseEnvironment):
    def __init__(self, level_file="start"): # this is the starting file 
        super().__init__(level_file)

    def create_ui(self):
        # Board: (50,50) - (1200, 980)
        self.board = Board(
            board_pos=(50,50),
            board_size=(1200, SCREEN_HEIGHT-50*2),
            env_data=self.env_data.board, 
            manager=self.ui_manager)

        # Code Blocks: (1200,0) - (1920,1080)
        # here implement the blocks that will be generated to interact with the board somehow?
        self.test_button = UIFactory.button(
            (SCREEN_WIDTH -200, SCREEN_HEIGHT - 100),
            (100, 50),
            "Movement",
            self.ui_manager,
            object_id="move",
        )

        # other misc stuff
        self.menu_button = UIFactory.button(
            (SCREEN_WIDTH - 350, SCREEN_HEIGHT - 100),
            (100, 50), 
            "Menu", 
            self.ui_manager)

        # Level Text
        rect = Rect((0,0), (100, 50)) 
        UILabel(rect, self.title, self.ui_manager)

        # Pop up telling user what to do
        rect = Rect((SCREEN_WIDTH // 2, SCREEN_HEIGHT //2), (300, 300)) 
        UIMessageWindow(rect, "To complete this level, be built different!", self.ui_manager)

    def on_ui_event(self, event):
        if self.test_button.on_click(event):
            # bugs cause if you press this more than once, spawns more windows, so it thinks its been pressed more times than it has, probably best to just get rid of these ui windows
            # only temp for now untill we got the coding block implemented 
            MovementWindow(Rect((SCREEN_WIDTH-500, 150), (250, 250)), self.ui_manager, self.board.player)
            
        if self.board.carrot.collision_check(self.board.player):
            if self.board.complete == False:
                self.board.complete = True
                rect = Rect((SCREEN_WIDTH // 2, SCREEN_HEIGHT //2), (300, 300)) 
                UIConfirmationDialog(rect, "You Win!", self.ui_manager)

        if self.menu_button.on_click(event):
            self.game_manager.change_env("Main Menu")

        if event.type == UI_CONFIRMATION_DIALOG_CONFIRMED: # here you check if it goes to the next level by rerendering, or using something else, also sets it back to the start
            try:
                next_level_data = self.env_data.env.next_level_data
                self.__init__(next_level_data)
                self.reset()
            except:
                self.__init__('start')
                self.game_manager.change_env("Main Menu")


    def update_frame(self, delta_time):
        pass
