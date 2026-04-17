import pygame
from pygame import Rect
from pygame_gui.elements import UIImage, UIPanel, UILabel
from game.core.images import load_image
from game.core.ui import TypingTextBox, UIFactory
from game.core.constants import DIALOGUE_SELECTED

# The popup that comes up at the start of every game in 'environments/game.py'
class DialoguePanel(UIPanel):
    def __init__(self, panel_pos, panel_size, text, manager):
        # Setting the starting height to 5 here since it should be above any other ui panels to be rendered
        super().__init__(Rect(panel_pos, panel_size), manager=manager, object_id="#dialouge_panel", starting_height=5)
        
        self.create_ui(text, panel_size)

    def create_ui(self, text, panel_size):
        # this is prlly not the best for now of setting pos/size but its only as a temp measure untill we decide how we want to talk to the user to look like
        padding = 10
        ui_size = (panel_size[0]-padding*2, panel_size[1]//3-padding*2) 

        # Renders the typing text box that updates the typing every frame
        text_pos = (padding,padding)
        self.text_box = TypingTextBox(
            pos=text_pos,
            size=ui_size,
            html_text=text,
            manager=self.ui_manager,
            container=self,
            object_id="#dialogue",
            typing_speed=30,)

        # Confirmation button to exit the panel
        conf_pos = (padding, panel_size[1] - ui_size[1] - padding)
        self.confirm = UIFactory.button_img(
            pos=conf_pos, 
            size=ui_size, 
            image_path="game/assets/menu/button.png", 
            text="Confirm", 
            manager=self.ui_manager,
            container=self,
            object_id="#transparent_button")

    def process_event(self, event):
        super().process_event(event)
        if self.confirm.button.on_click(event):
            # Deletes this panel
            self.kill()
            window_selected_event = pygame.event.Event(DIALOGUE_SELECTED)
            pygame.event.post(window_selected_event)

    def update(self, delta_time):
        super().update(delta_time)
        # Moving the scrolling text 
        self.text_box.update_typing(delta_time)
        pass


class ConfirmationPanel(UIPanel):
    def __init__(self, panel_pos, panel_size, title, message, confirm_event_type, manager):
        super().__init__(
            Rect(panel_pos, panel_size),
            manager=manager,
            object_id="#confirm_panel",
            starting_height=6,
        )
        self.confirm_event_type = confirm_event_type
        self.create_ui(title, message, panel_size)

    def create_ui(self, title, message, panel_size):
        padding = 24
        button_gap = 18
        button_size = (160, 54)
        button_y = panel_size[1] - 78
        total_button_width = (button_size[0] * 2) + button_gap
        buttons_x = (panel_size[0] - total_button_width) // 2

        UILabel(
            relative_rect=Rect((padding, 22), (panel_size[0] - (padding * 2), 36)),
            text=title,
            manager=self.ui_manager,
            container=self,
            object_id="#confirm_title",
        )

        UILabel(
            relative_rect=Rect((padding, 78), (panel_size[0] - (padding * 2), 52)),
            text=message,
            manager=self.ui_manager,
            container=self,
            object_id="#confirm_body",
        )

        self.cancel_button = UIFactory.button_img(
            pos=(buttons_x, button_y),
            size=button_size,
            image_path="game/assets/menu/button.png",
            text="Cancel",
            manager=self.ui_manager,
            container=self,
            object_id="#confirm_cancel_button",
        )
        self.confirm_button = UIFactory.button_img(
            pos=(buttons_x + button_size[0] + button_gap, button_y),
            size=button_size,
            image_path="game/assets/menu/button.png",
            text="Confirm",
            manager=self.ui_manager,
            container=self,
            object_id="#confirm_accept_button",
        )

    def process_event(self, event):
        super().process_event(event)
        if self.cancel_button.on_click(event):
            self.kill()
            return
        if self.confirm_button.on_click(event):
            self.kill()
            confirm_event = pygame.event.Event(self.confirm_event_type)
            pygame.event.post(confirm_event)

    def update(self, delta_time):
        super().update(delta_time)

# Making the level text a ui panel so that it can change heights and not be lost in the rendering order
class LevelText(UIPanel):
    def __init__(self, panel_pos, panel_size, text, manager):
        # Setting the starting height to 4 here since it should be above any other ui panels to be rendered, but below the dialouge text
        super().__init__(Rect(panel_pos, panel_size), manager=manager, object_id="#transparent_panel", starting_height=4)

        # for some reason im having trouble using the theme.json aswell for this panel to set the image so ive just put the image as an element
        img = load_image('game/assets/menu/button.png')
        UIImage(relative_rect=Rect((0,0), panel_size), 
            image_surface=img, 
            manager=self.ui_manager, 
            container=self)
        
        UILabel(relative_rect=Rect((0,0),panel_size),
            text=text,
            manager=self.ui_manager,
            container=self)
        
