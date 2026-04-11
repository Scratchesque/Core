from pygame import Rect
from pygame_gui.elements import UIPanel, UIButton
from pygame_gui import *
from game.core.constants import *

class Panel(UIPanel):
    def __init__(self, board_pos, board_size, env_data, manager, player):
        super().__init__(Rect(board_pos, board_size), manager=manager, object_id="#code_background", starting_height=2)

        self.env_data = env_data
        self.manager = manager

        self.board_size = board_size
        self.player = player

        UIButton(
            Rect((50,0), (100, 50)),
            "Up",
            manager=manager,
            container=self,
            parent_element=self,
            object_id="#up",
        )

        UIButton(
            Rect((50,100), (100, 50)),
            "Down",
            manager=manager,
            container=self,
            parent_element=self,
            object_id="#down",
        )

        UIButton(
            Rect((0,50), (100, 50)),
            "Left",
            manager=manager,
            container=self,
            parent_element=self,
            object_id="#left",
        )

        UIButton(
            Rect((100,50), (100, 50)),
            "Right",
            manager=manager,
            container=self,
            parent_element=self,
            object_id="#right",
        )

    def process_event(self, event):
        super().process_event(event)
        # here ive just used another way like object ids, to not save each button indivudually to their own self.xxxx
        if event.type == UI_BUTTON_PRESSED:
            if event.ui_object_id == '#code_background.#up':
                self.player.move('U')
            if event.ui_object_id == '#code_background.#down':
                self.player.move('D')
            if event.ui_object_id == '#code_background.#left':
                self.player.move('L')
            if event.ui_object_id == '#code_background.#right':
                self.player.move('R')

