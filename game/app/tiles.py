from pygame import Rect, math, transform, MOUSEBUTTONUP
from pygame_gui.elements import UIImage, UIScreenSpaceHealthBar

from game.app.panels import MessagePanel, SpeechPanel
from game.core.constants import *
from game.core.events import *
from game.core.images import load_image
from game.support.graphics import cut_graphics, tile_graphics

# The main class that each tile is using so that they can be rendered on the board map
class Tile(UIImage):
    MOVEMENT_DURATION = 10

    def __init__(self, start_pos, tiles_size, img_path, manager, container=None, tile=None, board_offset=(0, 0)):
        #Setup pos/size of tile
        self.tiles_size = (int(tiles_size[0]), int(tiles_size[1]))
        self.board_offset = (int(board_offset[0]), int(board_offset[1]))

        relative_pos = (
            self.board_offset[0] + start_pos[0] * self.tiles_size[0],
            self.board_offset[1] + start_pos[1] * self.tiles_size[1],
        )
        relative_rect = Rect(relative_pos, tiles_size)

        # Setup image graphics
        self.full_img = load_image(f'game/assets/{img_path}')
        if tile == None:
            self.base_image = self.full_img
        else:
            self.sprite_list = tile_graphics(self.full_img)
            self.base_image = self.sprite_list[tile]

        super().__init__(relative_rect=relative_rect, image_surface=self.base_image, manager=manager, container=container)
        self.set_image(self.base_image)

        self.pos = math.Vector2(start_pos)
        self.animation_count = 0

    # Fix blurry images with scaling
    def set_image(self, image_surface, image_is_alpha_premultiplied=False):
        self.base_image = image_surface
        scaled_image = transform.scale(image_surface, self.tiles_size)
        super().set_image(scaled_image, image_is_alpha_premultiplied)
    
    # Setup animations with cutting parameters of image 
    def _setup_animations(self, animation_frames, sprite_col_start=0, sprite_row_start=0, sprite_gap=0):
        self.animation_count = 1
        self.animations = {}
        self.state = 'idle'

        animation_list = cut_graphics(
            img_surface=self.full_img, 
            sprite_col_start=sprite_col_start,
            sprite_row_start=sprite_row_start,
            sprite_gap=sprite_gap
        )
        
        for name, frames in animation_frames.items():
            self.animations[name] = []
            for frame in frames:
                self.animations[name].append(animation_list[frame])
    
    # Update animation image state 
    def update(self, delta_time):
        if self.animation_count == 0:
            return

        current_strip = self.animations[self.state]
        frame_index = (self.animation_count // self.MOVEMENT_DURATION) % len(current_strip)
        tile_number = current_strip[frame_index]

        self.set_image(self.sprite_list[tile_number])
        self.animation_count += 1
    
    # Check that absolute distance between 2 objects is less than 0.9 tiles away 
    @staticmethod
    def collision_check(pos1, pos2):
        x = abs(pos1.x - pos2.x) <= 0.9
        y = abs(pos1.y - pos2.y) <= 0.9
        if x and y:
            return True

class NPC(Tile):
    def __init__(self, start_pos, tiles_size, npc_data, manager, container=None, board_offset=(0, 0)):
        img_path = 'SproutLands/Characters/Free Chicken Sprites.png'
        super().__init__(start_pos, tiles_size, img_path, manager, container, 0, board_offset)
        
        self.bubble_x = self.rect.x + tiles_size[0]
        self.bubble_y = self.rect.y - tiles_size[1]

        self.message_list = npc_data
        self.create_speech()

        self._setup_animations(
            animation_frames=({
                "idle": [0,1]
            })
        )
        
    def create_speech(self):
        self.speech_bubble = SpeechPanel(
            panel_pos=(self.bubble_x,self.bubble_y),
            panel_size=(250,80),
            message_list=self.message_list,
            manager=self.ui_manager
        )
        
    def process_event(self, event):
        if event.type == MOUSEBUTTONUP and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.speech_bubble.kill() if self.speech_bubble.alive() else self.create_speech()

class Player(Tile):
    def __init__(self, start_pos, tiles_size, map_tiles, player_data, manager, container=None, board_offset=(0, 0)):
        self.shadow = Tile(start_pos=start_pos,
                           tiles_size=tiles_size,
                           img_path='levels/shadow.png',
                           manager=manager,
                           container=container,
                           board_offset=board_offset)
        
        # Ive put the img_path in here cause its not something that 'should' be changed on the fly as animations can break if changed as of now
        img_path='SproutLands/Characters/Basic Charakter Spritesheet.png'
        super().__init__(start_pos, tiles_size, img_path, manager, container, 0, board_offset)

        self.vel = math.Vector2(0,0)
        self.tiles_size = math.Vector2(tiles_size)
        self.board_offset = math.Vector2(board_offset)

        self.map_tiles = map_tiles

        self.jumpable_tiles = []
        self.boundary_tiles = ['npc']

        self.current_health = 1
        self.move_cost = 0

        self._load_player_data(player_data)

        self._setup_animations(
            animation_frames=({
                "down":  [2, 3],
                "up":    [6, 7],
                "left":  [10, 11],
                "right": [14, 15],
                "idle": [0, 1],
                "jump": [0]
            }),
            sprite_col_start=1,
            sprite_row_start=1,
            sprite_gap=2
        )

        self.move_timer = 0
        self.is_moving = False
        self.is_jumping = False


    def _load_player_data(self, player_data):
        map_bounds = player_data.bounds

        if hasattr(map_bounds, "jumpable"):
            self.jumpable_tiles = map_bounds.jumpable
        self.boundary_tiles += map_bounds.blocked + self.jumpable_tiles
        
        # set up the energy bar if it is present in the env data json
        if hasattr(player_data, "energy"):
            player_energy = player_data.energy
            self.health_capacity = player_energy.health
            self.current_health = player_energy.health
            self.move_cost = 1

            UIScreenSpaceHealthBar(relative_rect=Rect((50,50),(75,25)),
                        sprite_to_monitor=self,
                        manager=self.ui_manager,
                        object_id='#energy_bar',
                        container=self.ui_container)
    
    # right now the only way to get the health lower is through this function that is called in code blocks
    # so that you can change the energy per level, you can set values from the env data json 
    def deplete_energy(self):
        self.current_health -= self.move_cost
    
    def goal_check(self, obj):
        if not self.is_jumping:
            return self.collision_check(self.pos, obj.pos)

    def do_action(self, action, x=0, y=0):
        if self.is_moving:
            return

        match action:
            case "up" | "down" | "left" | "right" | "jump":
                self.og_pos = self.pos.copy()
                self.move_timer = self.MOVEMENT_DURATION
                self.is_moving = True
                self.state = action

                self.vel.y = y
                self.vel.x = x
                if action == "jump":
                    self.is_jumping = True
    
    def set_idle(self):
        self.is_moving = False
        self.is_jumping = False
        self.state = 'idle'
        self.vel = math.Vector2(0, 0)

    def _apply_jump(self):
        
        if self.is_jumping:
            jump_height = min(-2, -2 + self.vel.y)
            artificial_y = jump_height * self.progress
            if self.move_timer >= self.MOVEMENT_DURATION // 2:
                return artificial_y
            else:
                return jump_height - artificial_y
            
        # if not jumping, then no change    
        return 0

    def update_movement(self):
        if not self.is_moving:
            return

        self.move_timer -= 1
        self.progress = 1 - (self.move_timer / self.MOVEMENT_DURATION)

        move_x = self.vel.x * self.progress
        move_y = self.vel.y * self.progress
        
        move_y += self._apply_jump()

        self.pos.x = self.og_pos.x + move_x
        self.pos.y = self.og_pos.y + move_y

        if self.move_timer <= 0:
            self.set_idle()

        self.update_tile_collisions()
        self.update_position()

    def update_tile_collisions(self):
        if self.vel.x == 0 and self.vel.y == 0:
            # this code is for that if they are ontop of a tile that they shouldnt be, then tp them back
            if not self.is_jumping:
                for collision_name in self.jumpable_tiles:
                    for sprite in self.map_tiles[collision_name]:
                        if self.collision_check(self.pos, sprite.pos):
                            self.pos = self.og_pos.copy()
                            self.set_idle()
            return

        for collision in self.boundary_tiles:
            # this is so that if they are jumping, they can go through tiles and skip those collisons
            if self.is_jumping and collision in self.jumpable_tiles:
                continue
            for sprite in self.map_tiles[collision]:
                # so that collision works while jumping, remove the artifical jump height added when checking for collisions
                collision_pos = self.pos.copy()
                collision_pos.y -= self._apply_jump()
                if self.collision_check(collision_pos, sprite.pos):
                    self.pos = self.og_pos.copy()
                    self.set_idle()
       
    def update_position(self):
        # this updates the position of the player tile and the created shadow tile
        player_x = int(self.board_offset.x + self.pos.x * self.tiles_size.x)
        player_y = int(self.board_offset.y + self.pos.y * self.tiles_size.y)

        shadow_pos = self.pos.y - self._apply_jump()
        shadow_y = int(self.board_offset.y + shadow_pos * self.tiles_size.y)

        self.set_relative_position((player_x, player_y))
        self.shadow.set_relative_position((player_x, shadow_y))

    def update(self, delta_time):
        super().update(delta_time)
        self.update_movement()
