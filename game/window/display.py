import pygame
from game.environments.base import BaseEnvironment
from game.core.constants import *
import pygame_gui

class Display:
    # no self, manual init only when first created so we can call this class over and over
    def init(environment: BaseEnvironment):
        try:
            Display.start(environment)
        except Exception as e:
            print(f'Error: {e}')
        finally:
            Display.exit_screen()

    def start(environment: BaseEnvironment):
        pygame.init()
        pygame.display.set_caption(environment.title)
        # Display.set_icon(r"Path/ICON.jpg")

        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        background.fill(environment.background)

        manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), theme_path=environment.theme_path)

        environment.setup(manager)
        
        clock = pygame.time.Clock()
        delta_time = 0

        while True:
            delta_time = clock.tick(60) / 1000
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 
                
                result = environment.loop(event)
                if result == False: 
                    return
                manager.process_events(event)
            
            manager.update(delta_time)
            screen.blit(background, (0, 0))
            manager.draw_ui(screen)

            pygame.display.update()

        
    def set_icon(path):
        icon = pygame.image.load(path)
        pygame.display.set_icon(icon)

    def get_screen():
        return pygame.display.get_surface()

    def update_screen(list=None):
        return pygame.display.update(list)
    
    def exit_screen():
        pygame.display.quit()
