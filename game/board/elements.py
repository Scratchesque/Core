import math
from pygame_gui.elements import UIImage
from pygame import image


class TiledElement():
    def __init__(self, tile_pos, tile_size, frame_pos, row_tiles_amm, img_path, ui_manager):
        # the element needs to know the constraints of itself so it cant go out, here it sets that up
        self.frame_pos = frame_pos
        self.tile_size = tile_size
        self.row_tiles_amm = row_tiles_amm

        # then this takes a normal (0,1) (2,6) or any position within the board and translates it to where it should be on the screen
        self.x = tile_pos[0]
        self.y = tile_pos[1]
        self.set_coord()

        loaded_image = image.load(f'game/assets/{img_path}').convert_alpha()
        self.image_rect = loaded_image.get_rect()
        self.image_rect.height = self.tile_size
        self.image_rect.width = self.tile_size
        self.image_rect.x = self.position[0]
        self.image_rect.y = self.position[1]

        # calling this renders it to the screen via the ui_manager
        self.element_img = UIImage(relative_rect=self.image_rect, image_surface=loaded_image, manager=ui_manager)

    # sets the position it should be on the screen based on x,y values set earlier
    def set_coord(self):
        x = self.x * self.tile_size + self.frame_pos[0]
        y = self.y * self.tile_size + self.frame_pos[1]
        self.position = [x, y]

    # adds directions to the existing position
    def translate_coord(self, x,y):
        self.x += x
        self.y += y
    
    def move(self, direction):
        if direction == 'U':
            self.translate_coord(0,-1)
            if self.y < 0:
                self.y = 0
        if direction == 'D':
            self.translate_coord(0,1)
            if self.y > self.row_tiles_amm - 1:
                self.y = self.row_tiles_amm -1
        if direction == 'L':
            self.translate_coord(-1,0)
            if self.x < 0:
                self.x = 0
        if direction == 'R':
            self.translate_coord(1,0)
            if self.x > self.row_tiles_amm - 1:
                self.x = self.row_tiles_amm -1
        
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