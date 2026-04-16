from pygame import Rect, transform
from pygame_gui.elements import UIButton, UIImage, UILabel, UITextBox
from pygame_gui._constants import *
from game.core.html_typing import truncate_html, visible_text_length
from game.core.images import load_image

# Making a button that can make it easy to check if itself has been pressed 
class Button(UIButton):
    def __init__(self, pos, size, text, manager, object_id=None, center=False, anchor=None, container=None):
        rect = Rect((0, 0), size)
        if anchor is not None:
            # Use Rect anchor names, e.g. "center", "midtop", "midbottom".
            setattr(rect, anchor, pos)
        elif center:
            rect.center = pos
        else:
            rect.topleft = pos
        super().__init__(rect, text, manager, container=container, object_id=object_id)

    # Example custom method
    def on_click(self, event):
        if event.type == UI_BUTTON_PRESSED:
            if event.ui_element == self:
                return True
        return False

# An easy way of accessing different ui elements that can do different things in one place
class UIFactory:
    @staticmethod
    def button(pos, size, text, manager, object_id=None, center=False, anchor=None, container=None):
        # Centralize button creation so styling and ids are consistent across levels.
        return Button(pos, size, text, manager, object_id=object_id, center=center, anchor=anchor, container=container)

    @staticmethod
    def label(pos, size, text, manager, object_id=None, container=None, anchor=None):
        # Simple text label for titles, HUD, or static UI text.
        if anchor is not None:
            rect = Rect((0, 0), size)
            setattr(rect, anchor, pos)
        else:
            rect = Rect(pos, size)
        return UILabel(rect, text, manager, container=container, object_id=object_id)

    @staticmethod
    def text_box(pos, size, html_text, manager, object_id=None, container=None):
        # Multi-line narrative or dialogue text. Supports basic HTML-style tags.
        rect = Rect(pos, size)
        return UITextBox(
            html_text, rect, manager, container=container, object_id=object_id
        )

    @staticmethod
    def image(pos, size, image_path, manager, object_id=None, container=None):
        # Image element for portraits/icons; scales to size if provided.
        loaded_image = load_image(image_path)
        if size is not None:
            loaded_image = transform.smoothscale(loaded_image, size)
        rect = Rect(pos, loaded_image.get_size())
        return UIImage(rect, loaded_image, manager, container=container, object_id=object_id)
    
    @staticmethod
    def button_img(pos,size,image_path,text,manager,object_id=None,container=None):
        # i tried just using buttons and adding a image to the theme.json, but auto scaling was having problems so this is the other fix i found
        root_path = load_image(image_path)
        img = UIImage(Rect(pos, size), root_path, manager, container=container)
        button = Button(pos, size, text, manager, object_id, container=container)

        # maybe temp, maybe not, untill/if theres a need to fix 
        class ButtonImg:
            def __init__(self, image, button):
                self.image = image
                self.button = button

        return ButtonImg(img, button)


class TypingTextBox(UITextBox):
    def __init__(self, pos, size, html_text, manager, object_id=None, typing_speed=30, container=None):
        super().__init__("", Rect(pos, size), manager, container=container, object_id=object_id)
        self.full_text = html_text
        self.visible_chars = 0
        self.typing_speed = typing_speed  # chars per second
        self.elapsed = 0.0

    def set_full_text(self, html_text):
        self.full_text = html_text
        self.visible_chars = 0
        self.elapsed = 0.0
        self.set_text("")

    def update_typing(self, delta_time):
        if self.visible_chars >= visible_text_length(self.full_text):
            return
        self.elapsed += delta_time
        new_count = min(visible_text_length(self.full_text), int(self.elapsed * self.typing_speed))
        if new_count != self.visible_chars:
            self.visible_chars = new_count
            partial_html = truncate_html(self.full_text, self.visible_chars)
            self.set_text(partial_html)

    def url_click(self, event):
        if event.type == UI_TEXT_BOX_LINK_CLICKED:
            if event.ui_element == self:
                return True
        return False
