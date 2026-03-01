import pygame


class BaseSprite(pygame.sprite.Sprite):
    def __init__(self):
        # this is so we dont have to add each sprite individually to update
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

    def draw(self, screen):
        pass

    def update(self, dt):
        pass

