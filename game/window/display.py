# Rabbit Rush - display.py
#
# Created By: VizzWizz, BoredHF, HJParker2802, KamranBasra, TafaraMangombe, Vladikusss
#
# Source: https://github.com/Scratchesque/Core

import pygame
import pygame_gui

from game.core.images import load_image
from game.core.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from game.core.paths import resolve_project_path
from game.environments.base import BaseEnvironment


# The main window rendered on the screen
class Display:
    FPS = 60
    CURSOR_SIZE = 25

    # Starts rendering the environment selected
    def __init__(self):
        pygame.init()
        self.resolution = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen = pygame.display.set_mode(self.resolution, pygame.FULLSCREEN)
        self.surface = pygame.Surface(self.resolution)
        self.set_icon("game/assets/levels/carrot.webp")
        self.cursor_img = load_image('game/assets/SproutLands/UI/Mouse/Triangle Mouse icon 1.png')

    def run(self, env: BaseEnvironment):
        pygame.display.set_caption(env.title)

        self.env = env
        self.running = True
        env.ui_manager = pygame_gui.UIManager(self.resolution, theme_path=env.theme_path)

        self.surface.fill(env.background_colour)
        env.reset()

        pygame.mouse.set_visible(False)
        
        self.main_loop()

    # The main window loop for rendering the environment
    def main_loop(self):
        clock = pygame.time.Clock()
        delta_time = 0

        while self.running:
            delta_time = clock.tick(self.FPS) / 1000

            # Set position of image cursor where mouse is
            self.update_cursor()

            # Process user input / events
            self.process_events()

            # Things to be processed each frame
            self.update_frame(delta_time)

    # Rendering objects on the window
    def update_frame(self, delta_time):
        # Things to update each frame in the environment
        self.env.update_frame(delta_time)
        # pygame_gui manager updating elements
        self.env.ui_manager.update(delta_time)
        # pygame drawing elements
        self.screen.blit(self.surface, (0, 0))
        self.env.ui_manager.draw_ui(self.screen)

        pygame.display.update()

    # pygame events
    def process_events(self):
        for event in pygame.event.get():
            # If user press x on window then return
            if event.type == pygame.QUIT:
                self.stop_game_loop()

            # pygame_gui manager processing
            self.env.ui_manager.process_events(event)

            # If events from the environment function gets false then return
            self.env.on_ui_event(event)

    def create_cursor(self):
        self.cursor = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect(
                (0,0),
                (self.CURSOR_SIZE,self.CURSOR_SIZE)
            ),
            image_surface=self.cursor_img,
            manager=self.env.ui_manager
        )
        self.cursor.change_layer(50)
 
    def update_cursor(self):
        pos = pygame.mouse.get_pos()
        self.cursor.set_position((pos[0]+1,pos[1]+1))

    # Sets icon for window, at least 32x32
    def set_icon(self, path):
        icon = pygame.image.load(resolve_project_path(path))
        pygame.display.set_icon(icon)

    def stop_game_loop(self):
        self.running = False

    # Exits the current window and checks to see if it should run again
    def exit_screen(self):
        pygame.display.quit()
