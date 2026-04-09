from pygame import image, Rect
from pygame_gui.elements import UIImage, UIWindow, UIButton
from pygame_gui import *
from game.core.constants import *

class MovementWindow(UIWindow):
    def __init__(self, rect, ui_manager, player):
        super().__init__(rect, ui_manager,
                         window_display_title='Movement',
                         object_id='#player_movement_window',
                         resizable=False)
        
        self.player = player

        UIButton(
            Rect((50,0), (100, 50)),
            "Up",
            manager=ui_manager,
            container=self,
            parent_element=self,
            object_id="#up",
        )

        UIButton(
            Rect((50,100), (100, 50)),
            "Down",
            manager=ui_manager,
            container=self,
            parent_element=self,
            object_id="#down",
        )

        UIButton(
            Rect((0,50), (100, 50)),
            "Left",
            manager=ui_manager,
            container=self,
            parent_element=self,
            object_id="#left",
        )

        UIButton(
            Rect((100,50), (100, 50)),
            "Right",
            manager=ui_manager,
            container=self,
            parent_element=self,
            object_id="#right",
        )

    def process_event(self, event):
        super().process_event(event)
        # here ive just used another way like object ids, to not save each button indivudually to their own self.xxxx
        if event.type == UI_BUTTON_PRESSED:
            if event.ui_object_id == '#player_movement_window.#up':
                self.player.move('U')
            if event.ui_object_id == '#player_movement_window.#down':
                self.player.move('D')
            if event.ui_object_id == '#player_movement_window.#left':
                self.player.move('L')
            if event.ui_object_id == '#player_movement_window.#right':
                self.player.move('R')

class TiledElement():
    def __init__(self, tile_pos, tiles_size, frame_pos, tiles_amm, img_path, ui_manager):
        # the element needs to know the constraints of itself so it cant go out, here it sets that up
        self.frame_pos = frame_pos
        self.tiles_size = tiles_size
        self.tiles_amm = tiles_amm

        # then this takes a normal (0,1) (2,6) or any position within the board and translates it to where it should be on the screen
        self.x = tile_pos[0]
        self.y = tile_pos[1]
        self.set_coord()

        loaded_image = image.load(f'game/assets/{img_path}').convert_alpha()
        self.image_rect = loaded_image.get_rect()
        self.image_rect.width = self.tiles_size[0]
        self.image_rect.height = self.tiles_size[1]
        self.image_rect.x = self.position[0]
        self.image_rect.y = self.position[1]

        # calling this renders it to the screen via the ui_manager
        self.element_img = UIImage(relative_rect=self.image_rect, image_surface=loaded_image, manager=ui_manager)

    # sets the position it should be on the screen based on x,y values set earlier
    def set_coord(self):
        if self.x < 0:
            self.x = 0
        elif self.x > self.tiles_amm[0] - 1:
                self.x = self.tiles_amm[0] -1
        if self.y < 0:
            self.y = 0
        elif self.y > self.tiles_amm[1] - 1:
            self.y = self.tiles_amm[1] -1

        x = self.x * self.tiles_size[0] + self.frame_pos[0]
        y = self.y * self.tiles_size[1] + self.frame_pos[1]
        self.position = [x, y]

    def move(self, direction):
        if direction == 'U':
            self.y -= 1
        if direction == 'D':
            self.y += 1           
        if direction == 'L':
            self.x -= 1
        if direction == 'R':
            self.x += 1

        self.set_coord()
        self.element_img.rect.x = self.position[0]
        self.element_img.rect.y = self.position[1]
    
    # check if element is ontop of another
    def collision_check(self, obj):
        x = self.x == obj.x
        y = self.y == obj.y
        if x and y: 
            return True
        return False