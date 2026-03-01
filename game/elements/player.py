from game.elements.sprite import BaseSprite
import pygame

# I copied the code below for how the player moves around cause idk pygame from https://github.com/kevinctofel/Asteroids
# look into that if curious about other things aswell cause ive not put in the asteroirds and shooting like them
class TestPlayer(BaseSprite):
    def __init__(self, x, y):
        super().__init__()
        
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.rotation = 0

    def draw(self, screen):
        pygame.draw.polygon(screen, (255,255,255), self.triangle(), 2)

    def rotate(self, dt):
        self.rotation += 300 * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rotate((-1 * dt))
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-1 * dt)

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * 200 * dt

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * 20 / 1.5
        a = self.position + forward * 20
        b = self.position - forward * 20 - right
        c = self.position - forward * 20 + right
        return [a, b, c]
