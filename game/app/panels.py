import pygame
from pygame import Rect
from pygame_gui.elements import UIImage, UIPanel, UILabel

from game.core.images import load_image
from game.support.ui import TypingTextBox, UIFactory


class DialoguePanel(UIPanel):
    def __init__(self, panel_pos, panel_size, title, message, manager):
        super().__init__(Rect(panel_pos, panel_size), manager=manager, object_id="#confirm_panel", starting_height=5)
        
        self.create_ui(title, message, panel_size)

    def create_ui(self, title, message, panel_size):
        padding = 24
        button_size = (160, 54)

        UILabel(
            relative_rect=Rect((padding, 22), (panel_size[0] - (padding * 2), 36)),
            text=title,
            manager=self.ui_manager,
            container=self,
            object_id="#confirm_title",
        )

        self.text_box = TypingTextBox(
            pos=(padding, 78),
            size=((panel_size[0] - padding * 2), (panel_size[1] -  padding * 2 - 125)),
            html_text=message,
            manager=self.ui_manager,
            container=self,
            object_id="#confirm_body")
        
        self.confirm_button = UIFactory.button_img(
            pos=((panel_size[0] - button_size[0]) // 2, panel_size[1] - 78),
            size=button_size,
            image_path="game/assets/menu/button.png",
            text="Confirm",
            manager=self.ui_manager,
            container=self,
            object_id="#confirm_accept_button",
        )

    def process_event(self, event):
        super().process_event(event)
        if self.confirm_button.on_click(event):
            self.kill()

    def update(self, delta_time):
        super().update(delta_time)
        self.text_box.update_typing(delta_time)

class MessagePanel(UIPanel):
    def __init__(self, panel_pos, panel_size, title, message, manager):
        super().__init__(
            Rect(panel_pos, panel_size),
            manager=manager,
            object_id="#confirm_panel",
            starting_height=6,
        )
        self.create_ui(title, message, panel_size)

    def create_ui(self, title, message, panel_size):
        padding = 24

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


class SpeechPanel(UIPanel):
    def __init__(self, panel_pos, panel_size, message_list, manager):
        super().__init__(
            Rect(panel_pos, panel_size),
            manager=manager,
            object_id="#transparent_panel",
            starting_height=4,
        )
        self.message_list = message_list
        self.message_index = 0
        self.create_ui(panel_size)

    def create_ui(self, panel_size):
        padding = 13
        button_diff = 65

        UIFactory.image(
            pos=(0,0),
            size=panel_size,
            image_path="game/assets/levels/speech.png",
            manager=self.ui_manager,
            container=self
        )

        self.text_box = TypingTextBox(
            pos=(padding, padding+5),
            size=(panel_size[0] - padding * 2, panel_size[1]- padding- 5 - button_diff),
            html_text=self.message_list[0],
            manager=self.ui_manager,
            container=self,
            object_id="#speech_body")

        self.next_button = UIFactory.button(
            pos=(panel_size[0]-button_diff,panel_size[1]-button_diff),
            size=(35,25),
            text="OK",
            manager=self.ui_manager,
            container=self,
            object_id="#speech_button",
        )

    def process_event(self, event):
        super().process_event(event)
        if self.next_button.on_click(event):
            self.message_index += 1
            if self.message_index >= len(self.message_list):
                self.message_index = 0
            self.text_box.set_full_text(self.message_list[self.message_index])
            # pass

    def update(self, delta_time):
        super().update(delta_time)
        self.text_box.update_typing(delta_time)


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
        
