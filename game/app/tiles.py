from pygame import image, Rect, math
from pygame_gui.elements import UIImage
from game.core.csv_support import cut_graphics 

# The main class that each tile is using so that they can be rendered on the board map
class Tile(UIImage):
    def __init__(self, start_pos, tiles_size, img_path, manager, container=None, tile=None):
        relative_pos= (start_pos[0] * tiles_size[0], start_pos[1] * tiles_size[1])
        relative_rect = Rect(relative_pos, tiles_size)
        
        self.vel = math.Vector2(0,0)

        root_path = f'game/assets/{img_path}'
        if tile == None:
            loaded_image = image.load(root_path).convert_alpha()
        else:
            loaded_image = cut_graphics(root_path, tile)

        super().__init__(relative_rect=relative_rect, image_surface=loaded_image, manager=manager, container=container)

        
class Player(Tile):
    def __init__(self, start_pos, tiles_size, img_path, manager, map_tiles, container=None, tile=None):
        self.map_tiles = map_tiles
        super().__init__(start_pos, tiles_size, img_path, manager, container, tile)

    def update_velocity(self, vel):    
        self.rect.x += vel.x
        self.rect.y += vel.y

    def update_pos_collision(self, collisions):
        for collision in collisions:
            for sprite in self.map_tiles[collision]:
                if self.rect.colliderect(sprite.rect):
                    overlap_x = min(self.rect.right, sprite.rect.right) - max(self.rect.left, sprite.rect.left)
                    overlap_y = min(self.rect.bottom, sprite.rect.bottom) - max(self.rect.top, sprite.rect.top)
                    if overlap_x < overlap_y:
                        if self.vel.x > 0:
                            self.rect.right = sprite.rect.left
                        elif self.vel.x < 0:
                            self.rect.left = sprite.rect.right
                        self.vel.x = 0
                    if overlap_y < overlap_x:
                        if self.vel.y > 0:
                            self.rect.bottom = sprite.rect.top
                        elif self.vel.y < 0:
                            self.rect.top = sprite.rect.bottom
                        self.vel.y = 0
                
    def update(self, delta_time):
        super().update(delta_time)
        self.update_velocity(self.vel)
        self.update_pos_collision(['water', 'tree'])
    #     self.update_sprite_sheet()
            
    # def update_sprite_sheet(self):
    #     sprite_index = (self.animationcount // self.animation_delay) % len(self.sprites)
    #     self.sprite = self.sprites[sprite_index]
    #     self.animationcount += 1
