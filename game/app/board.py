from pygame import image, Rect
from pygame_gui.elements import UIImage
from pygame_gui.windows import UIConfirmationDialog

from game.core.constants import *
from game.core.ui import UIFactory
from game.app.elements import TiledElement
from game.window.ui_windows import MovementWindow

class Board:
    def __init__(self, board_pos, board_size, level_data, manager):
        self.data = level_data
        self.board_pos = board_pos
        self.tiles_len = board_size/self.data.row_tiles_amm
        self.row_tiles_amm = self.data.row_tiles_amm
        self.manager = manager

        self.complete = False
        self.movement_window = None

        self.create_frame() 
        self.init_level()

    def create_frame(self):
        # just creating a grid , nothing extra yet like platforms or other things in the level
        tile_img = image.load('game/assets/menu/button.png').convert_alpha()
        tile_rect = tile_img.get_rect()
        tile_rect.width = self.tiles_len
        tile_rect.height = self.tiles_len

        for height in range(self.row_tiles_amm):
            for length in range(self.row_tiles_amm):
                tile_rect.x = self.board_pos[0] + self.tiles_len * length
                tile_rect.y = self.board_pos[1] + self.tiles_len * height
                UIImage(tile_rect, tile_img, self.manager)

    def init_level(self):
        # creating the elements to be on the screen from 'elements.py'       
        self.carrot = TiledElement(self.data.start_pos.carrot, self.tiles_len, self.board_pos, self.row_tiles_amm, 'levels/carrot.png', self.manager)
        self.player = TiledElement(self.data.start_pos.player, self.tiles_len, self.board_pos, self.row_tiles_amm, 'levels/bunny.png', self.manager)

        self.test_button = UIFactory.button(
            (SCREEN_WIDTH -200, SCREEN_HEIGHT - 100),
            (100, 50),
            "Movement",
            self.manager,
            object_id="move",
        )

    def on_ui_event(self, event):
        if self.test_button.on_click(event):
            if self.movement_window is None or not self.movement_window.alive():
                self.movement_window = MovementWindow(
                Rect((SCREEN_WIDTH-500, 150), (250, 250)),
                self.manager,
                self.player
            )

        if self.carrot.collision_check(self.player):
            if self.complete == False:
                self.complete = True
                rect = Rect((SCREEN_WIDTH // 2, SCREEN_HEIGHT //2), (300, 300)) 
                UIConfirmationDialog(rect, "You Win!", self.manager)

            
