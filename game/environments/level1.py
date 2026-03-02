from game.environments.base import BaseEnvironment
from game.elements.player import TestPlayer
from game.core.constants import *
import pygame
import pygame_gui

class Level1(BaseEnvironment):
    def __init__(self, title):
        background_hex = 'ffffff'
        super().__init__(title, background_hex)

    def setup(self, manager):
        
        self.hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                             text='Say Hello',
                                             manager=manager)
    
    def loop(self, event):

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
              if event.ui_element == self.hello_button:
                  print('Hello World!')
