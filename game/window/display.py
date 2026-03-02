import pygame
from game.environments.base import BaseEnvironment
from game.core.constants import *

class Display:
    # no self, manual init only when first created so we can call this class over and over
    def start(environment: BaseEnvironment):
        pygame.init()
        screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

        # Display.set_icon(r"Path/ICON.jpg")
        Display.set_caption(environment.title)
        
        clock = pygame.time.Clock()
        delta_time = 0

        environment.setup()
        game_state = True
        
        while game_state:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            
            pygame.display.update()
            # ?? pygame.display.flip()

            game_state = environment.loop(screen, delta_time)

            delta_time = clock.tick(60) / 1000

        # ends the pygame window so another level can be loaded
        pygame.display.quit()

        
      
    def set_caption(text):
        pygame.display.set_caption(text)

    def set_icon(path):
        icon = pygame.image.load(path)
        pygame.display.set_icon(icon)
    
    def get_screen():
        return pygame.display.get_surface()

    def update_screen(list=None):
        return pygame.display.update(list)
    
    def exit_screen():
        pygame.display.quit()
