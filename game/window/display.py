import pygame
import pygame_gui

from game.core.constants import *
from game.environments.base import BaseEnvironment


# The main window rendered on the screen
class Display:
    # Starts rendering the environment selected
    def run(self, env: BaseEnvironment):
        self.env = env

        pygame.init()
        pygame.display.set_caption(self.env.title)
        # self.set_icon(r"Path/ICON.jpg")

        self.running = True

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.ui_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), theme_path=self.env.theme_path)

        self.surface.fill(self.env.background_colour)
        self.ui_manager.preload_fonts([{
                    "name": "fira_code",
                    "point_size": 14,
                    "style": "regular",
                    "antialiased": "1",
                }])

        self.main_loop()

    # The main window loop for rendering the environment
    def main_loop(self):

        self.env.create_ui(self.ui_manager)

        clock = pygame.time.Clock()
        delta_time = 0

        while self.running:
            delta_time = clock.tick(60) / 1000

            # Process user input / events
            self.process_events()

            # Things to be processed each frame
            self.update_frame(delta_time)

    # Rendering objects on the window
    def update_frame(self, delta_time):
        # Things to update each frame in the environment
        self.env.update_frame(delta_time)
        # pygame_gui manager updating
        self.ui_manager.update(delta_time)
        # Reseting the screen each frame and drawing it back
        self.screen.blit(self.surface, (0, 0))
        self.ui_manager.draw_ui(self.screen)

        pygame.display.update()

    # pygame events
    def process_events(self):
        for event in pygame.event.get():
            # If user press x on window then return
            if event.type == pygame.QUIT:
                self.stop_game_loop()

            # pygame_gui manager processing
            self.ui_manager.process_events(event)

            # If events from the environment function gets false then return
            result = self.env.on_ui_event(event)
            if result == False:
                self.stop_game_loop()

    # Sets icon for window, at least 32x32
    def set_icon(self, path):
        icon = pygame.image.load(path)
        pygame.display.set_icon(icon)

    def stop_game_loop(self):
        self.running = False

    # Exits the current window and checks to see if it should run again
    def exit_screen(self):
        pygame.display.quit()
