from pygame import Rect
from pygame_gui.elements import UIPanel, UIButton
from pygame_gui import *
from game.core.constants import *

class CodeBlocks(UIPanel):
    def __init__(self, panel_pos, panel_size, manager, player):
        # Setting the start height to 2 as it can be placed above the board tiles
        super().__init__(Rect(panel_pos, panel_size), manager=manager, object_id="#code_panel", starting_height=2)

        self.player = player

        self.create_ui()

    def create_ui(self):
        UIButton(relative_rect=Rect((50,0), (100, 50)),
            text="Up",
            manager=self.ui_manager,
            container=self,
            object_id="#up")

        UIButton(relative_rect=Rect((50,100), (100, 50)),
            text="Down",
            manager=self.ui_manager,
            container=self,
            object_id="#down")

        UIButton(relative_rect=Rect((0,50), (100, 50)),
            text="Left",
            manager=self.ui_manager,
            container=self,
            object_id="#left")

        UIButton(relative_rect=Rect((100,50), (100, 50)),
            text="Right",
            manager=self.ui_manager,
            container=self,
            object_id="#right")

    def process_event(self, event):
        super().process_event(event)
        # here ive just used another way like object ids, to not save each button indivudually to their own self.xxxx
        if event.type == UI_BUTTON_PRESSED:
            if event.ui_object_id == '#code_panel.#up':
                self.player.move('U')
            if event.ui_object_id == '#code_panel.#down':
                self.player.move('D')
            if event.ui_object_id == '#code_panel.#left':
                self.player.move('L')
            if event.ui_object_id == '#code_panel.#right':
                self.player.move('R')

