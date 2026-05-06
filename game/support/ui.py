# Rabbit Rush - ui.py
#
# Created By: VizzWizz, BoredHF, HJParker2802, KamranBasra, TafaraMangombe, Vladikusss
#
# Source: https://github.com/Scratchesque/Core

from pygame import Rect, transform
from pygame_gui.elements import UIButton, UIImage, UILabel, UITextBox
from pygame_gui._constants import UI_BUTTON_PRESSED

from game.core.images import load_image

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
    def image(pos, size, image_path, manager, object_id=None, container=None, anchor=None):
        # Image element for portraits/icons; scales to size if provided.
        loaded_image = load_image(image_path)
        if size is not None:
            loaded_image = transform.scale(loaded_image, size)
        rect = Rect((0, 0), loaded_image.get_size())
        if anchor is not None:
            setattr(rect, anchor, pos)
        else:
            rect.topleft = pos
        return UIImage(rect, loaded_image, manager, container=container, object_id=object_id)
    
    @staticmethod
    def button_img(pos, size, image_path, text, manager, object_id=None, center=False, anchor=None, container=None):
        # Image-backed button with smooth scaling and a transparent text/click layer.
        root_image = load_image(image_path)
        scaled_image = transform.scale(root_image, size)

        rect = Rect((0, 0), size)
        if anchor is not None:
            setattr(rect, anchor, pos)
        elif center:
            rect.center = pos
        else:
            rect.topleft = pos

        img = UIImage(rect, scaled_image, manager, container=container)
        button = Button(rect.topleft, size, text, manager, object_id=object_id, container=container)

        return ImageButton(img, button)

# A UITextBox that can scroll through the text 
class TypingTextBox(UITextBox):
    def __init__(self, pos, size, html_text, manager, object_id=None, container=None):
        super().__init__("", Rect(pos, size), manager, container=container, object_id=object_id)
        self.full_text = html_text
        self.visible_chars = 0
        self.elapsed = 0.0

    def set_full_text(self, html_text):
        self.full_text = html_text
        self.visible_chars = 0
        self.elapsed = 0.0
        self.set_text("")

    def update(self, delta_time): 
        if self.visible_chars >= len(self.full_text):
            return
        self.elapsed += 1
        new_count = self.elapsed * 0.5  # chars per frame
        if new_count != self.visible_chars:
            self.visible_chars = int(new_count)
            partial_html = self.full_text[:self.visible_chars]
            self.set_text(partial_html)

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

    def on_click(self, event):
        if event.type == UI_BUTTON_PRESSED:
            if event.ui_element == self:
                return True
        return False

class ImageButton:
    def __init__(self, image, button):
        self.image = image
        self.button = button

    def on_click(self, event):
        return self.button.on_click(event)

    def kill(self):
        self.image.kill()
        self.button.kill()

    def alive(self):
        return self.button.alive()
    
    def change_layer(self, num):
        self.image.change_layer(num)
        self.button.change_layer(num)

    def set_relative_position(self, pos):
        self.image.set_relative_position(pos)
        self.button.set_relative_position(pos)

    def set_text(self, string):
        self.button.set_text(string)
