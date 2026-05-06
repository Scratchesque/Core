# Rabbit Rush - board.py
#
# Created By: VizzWizz, BoredHF, HJParker2802, KamranBasra, TafaraMangombe, Vladikusss
#
# Source: https://github.com/Scratchesque/Core

from pygame import Rect
from pygame_gui.elements import UIPanel

from game.app.tiles import Tile, Player, NPC
from game.core.constants import IMG_TILE_SIZE
from game.support.files import import_map_layout


# This file renders the map along with player/npc/goal tiles
class Board(UIPanel):
    def __init__(self, panel_pos, panel_size, env_data, manager):
        # Starting_height is the panel's layer height
        # For UIPanels you should either put all object that are supposed updated inside of the panels container
        # or for example, use a UIPanel as a gui hud element like player health without a container 
        super().__init__(
            Rect(panel_pos, panel_size), 
            manager=manager, 
            object_id="#game_panel", 
            starting_height=1
        )
        
        # Load vars to be used accross the class
        self.env_data = env_data
        self.completed_level = False
        self.tiles_size = None
        self.board_offset = (0, 0)
        self.map_tiles = {}

        # Render the tiles
        self.create_ui()

    # Gets the size of this panel container, and divdes it by the ammount of tiles in the level to get the size of the tile 
    def _scale_tiles(self, width, height):
        if self.tiles_size == None:
            panel_width, panel_height = self.get_relative_rect().size
            max_scale_x = panel_width // (width * IMG_TILE_SIZE)
            max_scale_y = panel_height // (height * IMG_TILE_SIZE)
            scale = max(1, min(max_scale_x, max_scale_y))
            tile_size = IMG_TILE_SIZE * scale

            board_width = width * tile_size
            board_height = height * tile_size

            offset_x = (panel_width - board_width) // 2
            offset_y = (panel_height - board_height) // 2

            self.tiles_size = [tile_size, tile_size]
            self.board_offset = (offset_x, offset_y)

    def create_ui(self):
        csv_title = self.env_data.env.title.replace(' ', '_')

        self.env_data.map.__dict__["start_pos"] = ""

        for element_type, tile_img in self.env_data.map.__dict__.items():
            self.map_tiles[element_type] = []
            csv_layout = import_map_layout(f'{csv_title}/{element_type}')
            height = len(csv_layout)
            for row_index, row in enumerate(csv_layout):
                width = len(row)
                self._scale_tiles(width,height)
                for col_index, val in enumerate(row):
                    if val != '-1':
                        tile = self.make_tile(col_index, row_index, val, 'SproutLands/'+tile_img)
                        if element_type != 'start_pos':
                            self.map_tiles[element_type].append(tile)

    def make_tile(self, x, y, val, tile_img):
        match val:
            case 'g': # Goal
                self.goal = Tile(start_pos=(x, y), 
                    tiles_size=self.tiles_size,
                    img_path='levels/carrot.webp', 
                    manager=self.ui_manager, 
                    container=self,
                    board_offset=self.board_offset)
            case 'p': # Player
                self.player = Player(start_pos=(x, y), 
                    tiles_size=self.tiles_size,
                    map_tiles=self.map_tiles,
                    player_data=self.env_data.player,
                    manager=self.ui_manager,
                    container=self,
                    board_offset=self.board_offset)
                self.player.change_layer(3)
            case 'n': # NPC
                self.npc = NPC(start_pos=(x, y), 
                    tiles_size=self.tiles_size,
                    npc_data=self.env_data.npc,
                    manager=self.ui_manager, 
                    container=self,
                    board_offset=self.board_offset)
                self.map_tiles['npc'] = [self.npc]
            case _:
                return Tile(start_pos=(x, y), 
                    tiles_size=self.tiles_size,
                    img_path=tile_img+".png", 
                    manager=self.ui_manager, 
                    container=self, 
                    tile=int(val),
                    board_offset=self.board_offset)
        
