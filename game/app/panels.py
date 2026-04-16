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
        
