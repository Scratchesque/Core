# here make it easy to place buttons and other elements on the screen?
# idk how pygame elements work
import pygame
import pygame_gui
from game.core.html_typing import truncate_html, visible_text_length


class Button(pygame_gui.elements.UIButton):
    def __init__(
        self,
        pos,
        size,
        text,
        manager,
        object_id=None,
        center=False,
        anchor=None,
        container=None,
    ):
        rect = pygame.Rect((0, 0), size)
        if anchor is not None:
            # Use pygame.Rect anchor names, e.g. "center", "midtop", "midbottom".
            setattr(rect, anchor, pos)
        elif center:
            rect.center = pos
        else:
            rect.topleft = pos
        super().__init__(rect, text, manager, container=container, object_id=object_id)

    # Example custom method
    def on_click(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self:
                return True
        return False

class ButtonImg():
            def __init__(self, image, button):
                self.image = image
                self.button = button

class UIFactory:
    @staticmethod
    def button(pos, size, text, manager, object_id=None, center=False, anchor=None, container=None):
        # Centralize button creation so styling and ids are consistent across levels.
        return Button(pos, size, text, manager, object_id=object_id, center=center, anchor=anchor, container=container)

    @staticmethod
    def label(pos, size, text, manager, object_id=None, container=None, anchor=None):
        # Simple text label for titles, HUD, or static UI text.
        if anchor is not None:
            rect = pygame.Rect((0, 0), size)
            setattr(rect, anchor, pos)
        else:
            rect = pygame.Rect(pos, size)
        return pygame_gui.elements.UILabel(rect, text, manager, container=container, object_id=object_id)

    @staticmethod
    def text_box(pos, size, html_text, manager, object_id=None, container=None):
        # Multi-line narrative or dialogue text. Supports basic HTML-style tags.
        rect = pygame.Rect(pos, size)
        return pygame_gui.elements.UITextBox(
            html_text, rect, manager, container=container, object_id=object_id
        )

    @staticmethod
    def image(pos, size, image_path, manager, object_id=None, container=None):
        # Image element for portraits/icons; scales to size if provided.
        image = pygame.image.load(image_path).convert_alpha()
        if size is not None:
            image = pygame.transform.smoothscale(image, size)
        rect = pygame.Rect(pos, image.get_size())
        return pygame_gui.elements.UIImage(rect, image, manager, container=container, object_id=object_id)
    
    @staticmethod
    def button_img(pos,size,image_path,text,manager,object_id=None,container=None):
        # i tried just using buttons and adding a image to the theme.json, but auto scaling was having problems so this is the other fix i found
        image = pygame.image.load(image_path).convert_alpha()
        image = pygame_gui.elements.UIImage(pygame.Rect(pos, size), image, manager)
        button = Button(pos, size, text, manager, object_id, container=container)
        return ButtonImg(image, button)


class TypingTextBox(pygame_gui.elements.UITextBox):
    def __init__(self, pos, size, html_text, manager, object_id=None, typing_speed=30, container=None):
        super().__init__("", pygame.Rect(pos, size), manager, container=container, object_id=object_id)
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
        if event.type == pygame_gui.UI_TEXT_BOX_LINK_CLICKED:
            if event.ui_element == self:
                return True
        return False
