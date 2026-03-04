import pygame
from game.environments.base import BaseEnvironment
from game.core.constants import *
import pygame_gui

class Display:
    # made it a self anyway cause techically it can be recreated as another var, cause its easier to reference from inside methods now
    def set_environments(self, environments: list[BaseEnvironment]):
        self.envs = environments

    def change_env(self, env_title):
        self.running = False
        self.load_level = True
        for env in self.envs:
            if env.title == env_title:
                self.env = env

    def init(self):
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

        print('a')
        try:
            self.run()
        except Exception as e:
            print(f'Error: {e}')
        finally:
            if not self.load_level:
                self.exit_screen()
            else:
                self.init()
                

    def run(self):

        self.env.create_ui(self.manager)
        
        clock = pygame.time.Clock()
        delta_time = 0

        while self.running:
            delta_time = clock.tick(60) / 1000

            # process events      
            for event in pygame.event.get():
                # if user press x on window then return 
                if event.type == pygame.QUIT:
                    self.running = False 
                
                # pygame_gui manager processing
                self.manager.process_events(event)

                # if events from the environment function gets false then return
                result = self.env.on_ui_event(event)
                if result == False: 
                    self.running = False
            
            # things to update each frame in the environment
            self.env.update_frame(delta_time)
            # pygame_gui manager updating
            self.manager.update(delta_time)
            # reseting the screen each frame and drawing it back
            self.screen.blit(self.background, (0, 0))
            self.manager.draw_ui(self.screen)

            pygame.display.update()

        
    def set_icon(self, path):
        icon = pygame.image.load(path)
        pygame.display.set_icon(icon)

    def get_screen(self):
        return pygame.display.get_surface()

    def update_screen(self,list=None):
        return pygame.display.update(list)

    def exit_screen(self):
        pygame.display.quit()
