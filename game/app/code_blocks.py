from pygame import Rect
from pygame_gui.elements import UIPanel, UIButton
from pygame_gui._constants import *

# This file should contain information about how we put in the code blocks
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
        
        UIButton(relative_rect=Rect((50,150), (100, 50)),
            text="Jump",
            manager=self.ui_manager,
            container=self,
            object_id="#jump")

    def process_event(self, event):
        super().process_event(event)
        if event.type == UI_BUTTON_PRESSED:
            if event.ui_object_id == '#code_panel.#up':
                self.player.do_action('up')
            if event.ui_object_id == '#code_panel.#down':
                self.player.do_action('down')
            if event.ui_object_id == '#code_panel.#left':
                self.player.do_action('left')
            if event.ui_object_id == '#code_panel.#right':
                self.player.do_action('right')
            if event.ui_object_id == '#code_panel.#jump':
                self.player.do_action('jump')
            
            