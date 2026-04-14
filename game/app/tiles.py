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
    def __init__(self, start_pos, tiles_size, manager, map_tiles, container=None, tile=None):
        # Ive put the img_path in here cause its not something that 'should' be changed on the fly as animations can break if changed as of now
        img_path='SproutLands/Characters/Basic Charakter Spritesheet.png'
        super().__init__(start_pos, tiles_size, img_path, manager, container, tile)

        self.vel = math.Vector2(0,0)
        self.pos = math.Vector2(start_pos)
        self.tiles_size = math.Vector2(tiles_size)

        self.map_tiles = map_tiles

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
        # or else they can just clip through to get to the goal check by jumping
        if not self.is_jumping:
            if self.rect.colliderect(obj.rect):
                return True

    def do_action(self, action = ""):
        if self.is_moving:
            return

        self.og_pos = self.pos.copy()
        self.move_timer = MOVEMENT_DURATION
        self.is_moving = True

        match action:
            case "up" | "down" | "left" | "right":
                if action == "up":
                    self.vel.y = -PLAYER_VEL
                elif action == "down":
                    self.vel.y = PLAYER_VEL
                elif action == "left":
                    self.vel.x = -PLAYER_VEL
                elif action == "right":
                    self.vel.x = PLAYER_VEL
                self.state = action

            case "jump":
                self.state = "jump"
                self.is_jumping = True
                self.vel.y = -PLAYER_VEL

            case "idle":
                self.state = "idle"
                self.is_moving = False

    def update_movement(self):
        if not self.is_moving:
            return

        self.move_timer -= 1
        progress = 1 - (self.move_timer / MOVEMENT_DURATION)

        move_x = self.vel.x * progress
        move_y = self.vel.y * progress

        if self.is_jumping and self.move_timer < MOVEMENT_DURATION // 2:
            move_y = self.vel.y - (move_y)

        self.pos.x = self.og_pos.x + move_x
        self.pos.y = self.og_pos.y + move_y

        if self.move_timer <= 0:
            self.is_moving = False
            self.is_jumping = False
            self.state = 'idle'
            self.vel = math.Vector2(0, 0)

    def update_wall_collisions(self, vel, collisions):
        if self.is_jumping:
            return

        if vel.x == 0 and vel.y == 0:
            return

        for collision in collisions:
            for sprite in self.map_tiles.get(collision, []):
                if self.rect.colliderect(sprite.rect):
                    self.pos = self.og_pos.copy()
                    self.vel = math.Vector2(0, 0)
       
    def update_sprite_sheet(self):
        time_lag = 10
        current_strip = self.animations[self.state]

        frame_index = (self.animationcount // time_lag) % len(current_strip)
        tile_number = current_strip[frame_index]
        self.set_image(self.sprite_list[tile_number])
        self.animationcount += 1

    def update(self, delta_time):
        super().update(delta_time)
        self.update_sprite_sheet()
        self.update_movement()
        self.update_wall_collisions(self.vel, ['water', 'tree'])

        # Setting the new self.pos onto the screen
        self.set_relative_position((int(self.pos.x * self.tiles_size.x), int(self.pos.y * self.tiles_size.y)))
         