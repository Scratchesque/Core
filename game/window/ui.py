# here make it easy to place buttons and other elements on the screen?
# idk how pygame elements work
import pygame_gui
import pygame

class Button(pygame_gui.elements.UIButton):
    def __init__(self, pos, size, text, manager):
        rect =  pygame.Rect(pos, size)
        super().__init__(rect, text, manager)

    # Example custom method
    def button_pressed(self,event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self:
                return True
        return False