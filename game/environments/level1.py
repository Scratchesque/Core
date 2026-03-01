from game.environments.base import BaseEnvironment
from game.elements.player import TestPlayer
from game.core.constants import *
import pygame

class Level1(BaseEnvironment):
    def __init__(self, title):
        super().__init__(title)

    def setup(self):
        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()

        TestPlayer.containers = (self.updatable, self.drawable)
        self.player = TestPlayer(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    
    def loop(self, screen, dt):
        # fills the screen black after every frame cause then you would have frames on top of one another
        screen.fill((0, 0, 0))

        for obj in self.updatable:
            obj.update(dt)
        
        for obj in self.drawable:
            obj.draw(screen)

        # this is to simulate going to another level, if the main loop is fulfiled then
        keys = pygame.key.get_pressed()
        if keys[pygame.K_x]:
            return False
        
        # if instead here it is to change to another level instead of carrying on with the main loop because of like an info button or something
        # firstly kill the window with 'pygame.display.quit()' to remove the sprite groups cause i think pygame doesnt like having multiple windows
        # then return false because you cant carry on with this game loop any more because you killed it to go back, maybe respawn it somehow? or im thinking too deep
        #
        # eg
        #
        # if button press
        #      level2 = MainMenu("Level2")
        #      main_window.start(level1)
        #      return False


        return True