from pygame import image, Rect, math
from pygame_gui.elements import UIImage
from game.core.csv_support import cut_graphics, tile_graphics
from game.core.constants import *

# The main class that each tile is using so that they can be rendered on the board map
class Tile(UIImage):
    def __init__(self, start_pos, tiles_size, img_path, manager, container=None, tile=None):
        relative_pos= (start_pos[0] * tiles_size[0], start_pos[1] * tiles_size[1])
        relative_rect = Rect(relative_pos, tiles_size)
        
        self.img = image.load(f'game/assets/{img_path}').convert_alpha()
        if tile == None:
            loaded_image = self.img
        else:
            self.sprite_list = cut_graphics(self.img)
            loaded_image = self.sprite_list[tile]

        super().__init__(relative_rect=relative_rect, image_surface=loaded_image, manager=manager, container=container)

class Player(Tile):
    def __init__(self, start_pos, tiles_size, manager, map_tiles, container=None):
        self.shadow = Tile(start_pos=start_pos,
                           tiles_size=tiles_size,
                           img_path='levels/shadow.png',
                           manager=manager,
                           container=container)
        
        # Ive put the img_path in here cause its not something that 'should' be changed on the fly as animations can break if changed as of now
        img_path='SproutLands/Characters/Basic Charakter Spritesheet.png'
        super().__init__(start_pos, tiles_size, img_path, manager, container, 0)

        self.vel = math.Vector2(0,0)
        self.pos = math.Vector2(start_pos)
        self.tiles_size = math.Vector2(tiles_size)

        self.map_tiles = map_tiles
        self.jumpable_tiles = ['vegetation']
        self.boundary_tiles = ['water', 'tree'] + self.jumpable_tiles

        self.animationcount = 0
        self.animations = {}
        self.state = 'idle'

        self.move_timer = MOVEMENT_DURATION
        self.is_moving = False
        self.is_jumping = False

        self._set_animations()

    def _set_animations(self):
        animation_frames = {
            "down":  [0, 1, 2, 3],
            "up":    [4, 5, 6, 7],
            "left":  [8, 9, 10, 11],
            "right": [12, 13, 14, 15],
            "idle": [0, 1],
            "jump": [0]
        }

        animation_list = tile_graphics(img_surface=self.img, 
                              sprite_col_start=1,
                              sprite_row_start=1,
                              sprite_gap=2)
        
        for name, frames in animation_frames.items():
            self.animations[name] = []
            for frame in frames:
                self.animations[name].append(animation_list[frame])
    
    def collision_check(self, obj):
        # or else they can just clip through tiles
        if not self.is_jumping:
            if self.rect.colliderect(obj.rect):
                return True

    def do_action(self, action, x=0, y=0):
        if self.is_moving:
            return

        self.og_pos = self.pos.copy()
        self.move_timer = MOVEMENT_DURATION
        self.is_moving = True

        match action:
            case "up" | "down" | "left" | "right":
                self.vel.y = y
                self.vel.x = x
                self.state = action

            case "jump": # the 'y' makes the jump look higher and higher, 'x' is for distance accross
                self.vel.x = x
                self.vel.y = -2 # jump height should be consistent
                self.state = action
                self.is_jumping = True
    
    def set_idle(self):
        self.is_moving = False
        self.is_jumping = False
        self.state = 'idle'
        self.vel = math.Vector2(0, 0)

    def update_movement(self):
        if not self.is_moving:
            return

        # incremental timer when the player is moving
        self.move_timer -= 1
        progress = 1 - (self.move_timer / MOVEMENT_DURATION)

        move_x = self.vel.x * progress
        move_y = self.vel.y * progress

        # without this if statement the player wouldnt come back down when jumping
        if self.is_jumping and self.move_timer < MOVEMENT_DURATION // 2:
            move_y = self.vel.y - (move_y)

        self.pos.x = self.og_pos.x + move_x
        self.pos.y = self.og_pos.y + move_y

        if self.move_timer <= 0:
            self.set_idle()

        # this took me forever to realise but unless the position is updated on the screen before, the collisions dont work correctly
        # in the future i will change collisions to use tile coordinates instead of checking if it is touching another sprite rect 
        # cause that fixes the problem of using update position twice, if not when colliding on a jump it tps back, 
        # this is a must have or else they get stuck ontop of the tile that they can jump over
        self.update_position()
        # no point of checking for wall collisions if the player wont be moving so only update when player is moving
        self.update_tile_collisions()
        # updating the new calculated position for if they touch a collision with a tile from the func called before
        self.update_position()

    def update_tile_collisions(self):
        if self.vel.x == 0 and self.vel.y == 0:
            # this code is for that if they are ontop of a tile that they shouldnt be, then tp them back
            if not self.is_jumping:
                for collision_name in self.jumpable_tiles:
                    for sprite in self.map_tiles[collision_name]:
                        if self.rect.colliderect(sprite.rect):
                            self.pos = self.og_pos.copy()
                            self.set_idle()
            return

        # theres still problems if the player is in a corner where they arent able to jump through
        # like on the start level, go up one and try to jump to the right 
        # not working cause the tile above is a boundary_tiles, but i dont think thats a big issue
        for collision in self.boundary_tiles:
            # this is so that if they are jumping, they can go through tiles and skip those collisons
            if self.is_jumping and collision in self.jumpable_tiles:
                continue
            for sprite in self.map_tiles[collision]:
                if self.rect.colliderect(sprite.rect):
                    # this is for jumping in place
                    if self.is_jumping and self.vel.x == 0:
                        continue
                    self.pos = self.og_pos.copy()
                    self.set_idle()
       
    def update_sprite_sheet(self):
        time_lag = 10
        current_strip = self.animations[self.state]

        frame_index = (self.animationcount // time_lag) % len(current_strip)
        tile_number = current_strip[frame_index]
        self.set_image(self.sprite_list[tile_number])
        self.animationcount += 1

    def update_position(self):
        # this updates the position of the player tile and the created shadow tile, then depending if the player is jumping or not it changes the position
        screen_x = int(self.pos.x * self.tiles_size.x)
        screen_y = int(self.pos.y * self.tiles_size.y)

        shadow_y = screen_y
        if self.is_jumping:
            shadow_y = int((self.og_pos.y)*self.tiles_size.y)

        self.set_relative_position((screen_x, screen_y))
        self.shadow.set_relative_position((screen_x, shadow_y))

    def update(self, delta_time):
        super().update(delta_time)
        self.update_sprite_sheet()
        self.update_movement()
