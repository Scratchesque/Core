import pygame
from game.environments.base import BaseEnvironment
from game.core.constants import *
import pygame_gui

# The main window rendered on the screen
class Display:
    # From main.py sets all available levels/environments that can be rendered
    def set_environments(self, environments: list[BaseEnvironment]):
        self.envs = environments

    # Stops the current loop and loop and starts loading the next environmnet
    def change_env(self, env_title: str):
        self.running = False
        self.load_level = True
        for env in self.envs:
            if env.title == env_title:
                self.env = env

    # Starts loading the window and setting up environment loop
    def run(self):
        pygame.init()
        pygame.display.set_caption(self.env.title)
        # self.set_icon(r"Path/ICON.jpg")

        self.running = True
        self.load_level = False

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), theme_path=self.env.theme_path)

        self.background.fill(self.env.background_colour)
        self.manager.preload_fonts([{'name': 'fira_code', 'point_size': 14, 'style': 'bold'}])

        self.env.set_window(self)

        try:
            self.main_loop()
        except Exception as e:
            print(f'Error: {e}')
        finally:
            self.exit_screen()
            
                
    # The main window loop for rendering the environment
    def main_loop(self):

        self.env.create_ui(self.manager)
        
        clock = pygame.time.Clock()
        delta_time = 0

        while self.running:
            delta_time = clock.tick(60) / 1000

            # Process user input / events  
            self.process_events()
                
            # Things to be processed each frame
            self.update_frame(delta_time)

    # Rendering objects on the window
    def update_frame(self,delta_time):
        # Things to update each frame in the environment
        self.env.update_frame(delta_time)
        # pygame_gui manager updating
        self.manager.update(delta_time)
        # Reseting the screen each frame and drawing it back
        self.screen.blit(self.background, (0, 0))
        self.manager.draw_ui(self.screen)

        pygame.display.update()

    # pygame events
    def process_events(self):
        for event in pygame.event.get():
            # If user press x on window then return 
            if event.type == pygame.QUIT:
                self.running = False 
            
            # pygame_gui manager processing
            self.manager.process_events(event)

            # If events from the environment function gets false then return
            result = self.env.on_ui_event(event)
            if result == False: 
                self.running = False

    # Sets icon for window, at least 32x32
    def set_icon(self, path):
        icon = pygame.image.load(path)
        pygame.display.set_icon(icon)

    # Exits the current window and checks to see if it should run again
    def exit_screen(self):
        pygame.display.quit()
        if self.load_level:
            self.run()
        
