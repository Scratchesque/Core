
from pygame_gui.elements import UIWindow, UIImage
import pygame
import pygame_gui
from pygame.locals import *

class Player:
    def __init__(self, start_pos, court_size):
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

    def process_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_UP:
                self.move_up = True
            if event.key == K_DOWN:
                self.move_down = True
            if event.key == K_LEFT:
                self.move_left = True
            if event.key == K_RIGHT:
                self.move_right = True

        if event.type == KEYUP:
            if event.key == K_UP:
                self.move_up = False
            if event.key == K_DOWN:
                self.move_down = False
            if event.key == K_LEFT:
                self.move_left = False
            if event.key == K_RIGHT:
                self.move_right = False
        

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

    def render(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)