import pygame
from pygame.locals import *
from game.core.constants import *
from pygame import image, transform
from pygame_gui.elements import UIImage

class Player:
    def __init__(self, start_pos, ui_manager):
        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False
        self.move_speed = 450.0

        self.position = [float(start_pos[0]), float(start_pos[1])]
        
        loaded_image = image.load('game/assets/background.jpg').convert()
        self.image_rect = loaded_image.get_rect()
        self.image_rect.height = 50
        self.image_rect.width = 50
        self.image_rect.x = self.position[0]
        self.image_rect.y = self.position[1]

        # calling this renders it to the screen via the ui_manager
        self.player_image = UIImage(relative_rect=self.image_rect, image_surface=loaded_image, manager=ui_manager)

    def update(self, dt):
        if self.move_up:
            self.position[1] -= dt * self.move_speed

            if self.position[1] < 10.0:
                self.position[1] = 10.0

            self.player_image.rect.y = self.position[1]
                
        if self.move_down:
            self.position[1] += dt * self.move_speed

            if self.position[1] > SCREEN_HEIGHT - self.image_rect.height - 10:
                self.position[1] = SCREEN_HEIGHT - self.image_rect.height - 10

            self.player_image.rect.y = self.position[1]

        if self.move_left:
            self.position[0] -= dt * self.move_speed

            if self.position[0] < 10.0:
                self.position[0] = 10.0

            self.player_image.rect.x = self.position[0]

        if self.move_right:
            self.position[0] += dt * self.move_speed

            if self.position[0] > SCREEN_WIDTH - self.image_rect.width - 10:
                self.position[0] = SCREEN_WIDTH - self.image_rect.width - 10

            self.player_image.rect.x = self.position[0]
