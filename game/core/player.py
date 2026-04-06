import pygame
from pygame.locals import *
from game.core.constants import *
from pygame import image, transform
from pygame_gui.elements import UIImage

class Player:
    def __init__(self, start_pos, court_size, ui_manager):
        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False
        self.move_speed = 450.0

        self.court_size = court_size

        self.length = 30.0
        self.width = 5.0

        self.position = [float(start_pos[0]), float(start_pos[1])]
        
        self.rect = pygame.Rect((start_pos[0], start_pos[1]), (self.width, self.length))
        self.colour = pygame.Color("#000000")
        self.area_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        loaded_image = image.load('game/assets/background.jpg').convert()
        image_rect = loaded_image.get_rect()
        image_rect.height = 50
        image_rect.width = 50
        self.player_image = UIImage(relative_rect=image_rect, image_surface=loaded_image, manager=ui_manager)

    def update(self, dt):
        if self.move_up:
            self.position[1] -= dt * self.move_speed

            if self.position[1] < 10.0:
                self.position[1] = 10.0

            self.rect.y = self.position[1]
                
        if self.move_down:
            self.position[1] += dt * self.move_speed

            if self.position[1] > self.court_size[1] - self.length - 10:
                self.position[1] = self.court_size[1] - self.length - 10

            self.rect.y = self.position[1]

        if self.move_left:
            self.position[0] -= dt * self.move_speed

            if self.position[0] < 10.0:
                self.position[0] = 10.0

            self.rect.x = self.position[0]

        if self.move_right:
            self.position[0] += dt * self.move_speed

            if self.position[0] > self.court_size[0] - self.length - 10:
                self.position[0] = self.court_size[0] - self.length - 10

            self.rect.x = self.position[0]
        
        self.player_image.rect = self.rect
