from pygame import image, Rect
from pygame_gui.elements import UIImage, UIPanel

from game.core.constants import *
from game.app.elements import TiledElement

class Board(UIPanel):
    def __init__(self, board_pos, board_size, env_data, manager):
        super().__init__(Rect(board_pos, board_size), manager=manager, object_id="#board_background")

        self.env_data = env_data
        self.manager = manager

        self.board_size = board_size
        self.tiles_amm = env_data.tiles_amm
        self.complete = False

        self.tiles_size = self._scale_tiles()

        self.create_frame() 
        self.init_level()

    def _scale_tiles(self):
        x = self.board_size[0] / self.tiles_amm[0]
        y = self.board_size[1] / self.tiles_amm[1]
        return [x,y]  

    def create_frame(self):
        # just creating a grid , nothing extra yet like platforms or other things in the level
        tile_img = image.load('game/assets/menu/button.png').convert_alpha()
        tile_rect = tile_img.get_rect()
        tile_rect.width = self.tiles_size[0]
        tile_rect.height = self.tiles_size[1]

        for height in range(self.tiles_amm[1]):
            for length in range(self.tiles_amm[0]):
                tile_rect.x = self.tiles_size[0] * length
                tile_rect.y = self.tiles_size[1] * height
                UIImage(tile_rect, tile_img, self.manager, container=self.panel_container)

    def init_level(self):
        # creating the elements to be on the screen from 'elements.py'       
        self.carrot = TiledElement((self.env_data.start_pos.carrot), self.tiles_size, self.tiles_amm, 'levels/carrot.png', self.manager, self.panel_container)
        self.player = TiledElement(self.env_data.start_pos.player, self.tiles_size, self.tiles_amm, 'levels/bunny.png', self.manager, self.panel_container)


            
