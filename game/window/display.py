import pygame
import pygame_gui

from game.core.constants import *
from game.environments.base import BaseEnvironment


# The main window rendered on the screen
class Display:
    # Starts rendering the environment selected
    def __init__(self):
        pygame.init()
        self.resolution = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen = pygame.display.set_mode(self.resolution, pygame.FULLSCREEN)
        self.surface = pygame.Surface(self.resolution)

    def run(self, env: BaseEnvironment):
        pygame.display.set_caption(env.title)

        self.env = env
        self.running = True
        env.ui_manager = pygame_gui.UIManager(self.resolution, theme_path=env.theme_path)

        env.reset()
        
        self.main_loop()

    # The main window loop for rendering the environment
    def main_loop(self):
        clock = pygame.time.Clock()
        delta_time = 0

        while self.running:
            delta_time = clock.tick(FPS) / 1000

            # Process user input / events
            self.process_events()

            # Things to be processed each frame
            self.update_frame(delta_time)

    # Rendering objects on the window
    def update_frame(self, delta_time):
        # Things to update each frame in the environment
        self.env.update_frame(delta_time)
        # pygame_gui manager updating/drawing
        self.env.ui_manager.update(delta_time)
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
            
    # Sets icon for window, at least 32x32
    def set_icon(self, path):
        icon = pygame.image.load(path)
        pygame.display.set_icon(icon)

    def stop_game_loop(self):
        self.running = False

    # Exits the current window and checks to see if it should run again
    def exit_screen(self):
        pygame.display.quit()
