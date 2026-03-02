import pygame
from game.environments.base import BaseEnvironment
from game.core.constants import *
import pygame_gui

class Display:
    # no self, manual init only when first created so we can call this class over and over
    def start(environment: BaseEnvironment):
        try:
            pygame.init()
            pygame.display.set_caption(environment.title)
            # Display.set_icon(r"Path/ICON.jpg")

            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            background.fill(environment.background)

            manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

            environment.setup(manager)
            
            clock = pygame.time.Clock()
            delta_time = 0

            is_running = True
            
            while is_running:
                delta_time = clock.tick(60) / 1000
            
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        is_running = False

                    environment.loop(event)
                    manager.process_events(event)
                
                manager.update(delta_time)
                screen.blit(background, (0, 0))
                manager.draw_ui(screen)

                pygame.display.update()
                # ?? pygame.display.flip()


            # ends the pygame window so another level can be loaded
            pygame.quit()
        except Exception as e:
            print(f'Error: {e}')
            

        
    def set_icon(path):
        icon = pygame.image.load(path)
        pygame.display.set_icon(icon)

    def get_screen():
        return pygame.display.get_surface()

    def update_screen(list=None):
        return pygame.display.update(list)
    
    def exit_screen():
        pygame.display.quit()
