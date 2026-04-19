from pygame import Rect
from pygame_gui.elements import UIPanel

from game.app.panels import MessagePanel
from game.app.tiles import Tile, Player, NPC
from game.core.constants import *
from game.core.events import *
from game.support.files import import_map_layout


# This file renders the map from the board data in the json
class Board(UIPanel):
    def __init__(self, panel_pos, panel_size, env_data, manager):
        # Starting_height is the panel's layer height
        # For UIPanels you should either put all object that are supposed updated inside of the panels container
        # or for example, use a UIPanel as a gui hud element like player health without a container 
        super().__init__(Rect(panel_pos, panel_size), manager=manager, object_id="#game_panel", starting_height=1)
        
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
        # Gets the relevant information about each map file in the board data at the loaded json, then scales and renders each tile in each file
        for element_type, element_data in self.env_data.map.__dict__.items():
            csv_map = element_data[0]
            if element_type == 'start_pos':
                csv_map = element_data
            tile_img = element_data[1]
            self.map_tiles[element_type] = []
            csv_layout = import_map_layout(csv_map)
            height = len(csv_layout)
            for row_index, row in enumerate(csv_layout):
                width = len(row)
                self._scale_tiles(width,height)
                for col_index, val in enumerate(row):
                    if val != '-1':
                        tile = self.make_tile(col_index, row_index, val, tile_img)
                        # only apply tiles that are part of the map
                        if element_type != 'start_pos':
                            self.map_tiles[element_type].append(tile)

    def make_tile(self, x, y, val, tile_img):
        match val:
            case 'g': #Goal
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
                # if the goal tile is made before the player, the player is placed underneath it
                # so that the player is always above the goal/npc tiles, chaange the layer
                self.player.change_layer(3)
            case 'n': #NPC (future implementation of its own class and dialouge etc.)
                # need a better tileset tho for the npc
                self.npc = NPC(start_pos=(x, y), 
                    tiles_size=self.tiles_size,
                    npc_data=self.env_data.npc,
                    manager=self.ui_manager, 
                    container=self,
                    board_offset=self.board_offset)
                # for collision for player to not go over npc 
                self.map_tiles['npc'] = [self.npc]
            case _:
                return Tile(start_pos=(x, y), 
                    tiles_size=self.tiles_size,
                    img_path=tile_img+".png", 
                    manager=self.ui_manager, 
                    container=self, 
                    tile=int(val),
                    board_offset=self.board_offset)
        
    # Having super().process_event(event) or super().update(delta_time) inside the panel eliminates the need to call these functions outside of this class
    # With pygame_gui Since we passthrough the ui manager, it inherites UIPanel (or any element in pygame_gui.elements) and does its own initalisation which allows us to process events in each class
    def process_event(self, event):
        super().process_event(event)
        if self.completed_level == False:
            if self.player.goal_check(self.goal):
                self.completed_level = True
                info_size = (275,160)
                info_pos = ((SCREEN_WIDTH-info_size[0])//2), ((SCREEN_HEIGHT-info_size[1])//2)
                MessagePanel(panel_pos=info_pos,
                    panel_size=info_size,
                    title="You Win!",
                    message="Loading next level...",
                    manager=self.ui_manager)
                level_complete_event = pygame.event.Event(LEVEL_COMPLETED)
                pygame.event.post(level_complete_event)
    
    def update(self, delta_time):
        super().update(delta_time)
        
