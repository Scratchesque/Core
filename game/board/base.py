from pygame import image, Rect
from pygame_gui.elements import UIImage
from pygame_gui.windows import UIConfirmationDialog

from game.core.constants import *
from game.core.ui import UIFactory
from game.board.elements import TiledElement
from game.window.ui_windows import MovementWindow


class GameBoard:
    def __init__(self, game_pos, game_size, row_tiles_amm, manager):
        self.game_pos = game_pos
        self.tiles_len = game_size/row_tiles_amm
        self.row_tiles_amm = row_tiles_amm
        self.manager = manager

        self.complete = False

        self.create_frame() 
        self.init_level((0,0),(1,2))

    def create_frame(self):
        # just creating a grid , nothing extra yet like platforms or other things in the level
        tile_img = image.load('game/assets/menu/button.png').convert_alpha()
        tile_rect = tile_img.get_rect()
        tile_rect.width = self.tiles_len
        tile_rect.height = self.tiles_len

        for height in range(self.row_tiles_amm):
            for length in range(self.row_tiles_amm):
                tile_rect.x = self.game_pos[0] + self.tiles_len * length
                tile_rect.y = self.game_pos[1] + self.tiles_len * height
                UIImage(tile_rect, tile_img, self.manager)

    def init_level(self, player_tile_pos, carrot_tile_pos):
        # creating the elements to be on the screen from 'elements.py'       
        self.carrot = TiledElement(carrot_tile_pos, self.tiles_len, self.game_pos, self.row_tiles_amm, 'levels/carrot.png', self.manager)
        self.player = TiledElement(player_tile_pos, self.tiles_len, self.game_pos, self.row_tiles_amm, 'levels/bunny.png', self.manager)

        self.test_button = UIFactory.button(
            (SCREEN_WIDTH -200, SCREEN_HEIGHT - 100),
            (100, 50),
            "Movement",
            self.manager,
            object_id="move",
        )

    def on_ui_event(self, event):
        if self.test_button.on_click(event):
            # bugs cause if you press this more than once, spawns more windows, so it thinks its been pressed more times than it has, probably best to just get rid of these ui windows
            # only temp for now untill we got the coding block implemented 
            MovementWindow(Rect((SCREEN_WIDTH-500, 150), (250, 250)), self.manager, self.player)

        if self.carrot.collision_check(self.player):
            if self.complete == False:
                self.complete = True
                rect = Rect((SCREEN_WIDTH // 2, SCREEN_HEIGHT //2), (300, 300)) 
                UIConfirmationDialog(rect, "You Win!", self.manager)

            
