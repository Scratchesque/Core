from pygame import Rect
from pygame_gui.elements import UIPanel
from pygame_gui.windows import UIConfirmationDialog 
from game.core.csv_support import import_map_layout
from game.core.constants import *
from game.app.tiles import Tile, Player

# This file renders the map from the board data in the json
class Board(UIPanel):
    def __init__(self, panel_pos, panel_size, board_data, manager):
        # Starting_height is the panel's layer height
        # For UIPanels you should either put all object that are supposed updated inside of the panels container
        # or for example, use a UIPanel as a gui hud element like player health without a container 
        super().__init__(Rect(panel_pos, panel_size), manager=manager, object_id="#transparent_panel", starting_height=1)
        
        # Load vars to be used accross the class
        self.board_data = board_data
        self.completed_level = False
        self.tiles_size = None
        self.map_tiles = {}

        # Render the tiles
        self.create_ui()
        self.init_level()

    # Gets the size of this panel container, and divdes it by the ammount of tiles in the level to get the size of the tile 
    def _scale_tiles(self, width, height):
        if self.tiles_size == None:
            x = self.get_relative_rect().size[0] // width
            y = self.get_relative_rect().size[1] // height
            self.tiles_size = [x,y]

    def create_ui(self):
        # Gets the relevant information about each map file in the board data at the loaded json, then scales and renders each tile in each file
        for element_type, element_data in self.board_data.map.__dict__.items():
            csv_map = element_data[0]
            tile_img = element_data[1]
            self.map_tiles[element_type] = []
            csv_layout = import_map_layout(csv_map)
            height = len(csv_layout)
            for row_index, row in enumerate(csv_layout):
                width = len(row)
                self._scale_tiles(width,height)
                for col_index, val in enumerate(row):
                    if val != '-1':
                        tile = Tile(start_pos=(col_index, row_index), 
                            tiles_size=self.tiles_size,
                            img_path=tile_img+".png", 
                            manager=self.ui_manager, 
                            container=self, 
                            tile=int(val))
                        self.map_tiles[element_type].append(tile)

    def init_level(self):
        # Uses random sprites I found in the assets folder and sets their position based on the json loaded
        
        self.goal = Tile(start_pos=self.board_data.start_pos.goal, 
            tiles_size=self.tiles_size,
            img_path='SproutLands/Objects/Basic Grass Biom things 1.png', 
            manager=self.ui_manager, 
            container=self, 
            tile=20)
        self.player = Player(start_pos=self.board_data.start_pos.player, 
            tiles_size=self.tiles_size,
            map_tiles=self.map_tiles,
            manager=self.ui_manager, 
            container=self, 
            tile=0)
        
    # Having super().process_event(event) or super().update(delta_time) inside the panel eliminates the need to call these functions outside of this class
    # With pygame_gui Since we passthrough the ui manager, it inherites UIPanel (or any element in pygame_gui.elements) and does its own initalisation which allows us to process events in each class
    def process_event(self, event):
        super().process_event(event)
        if self.player.rect.colliderect(self.goal.rect):
            if self.completed_level == False:
                self.completed_level = True
                rect = Rect((SCREEN_WIDTH // 2, SCREEN_HEIGHT //2), (300, 300)) 
                UIConfirmationDialog(rect=rect, 
                    action_long_desc="You Win!", 
                    manager=self.ui_manager)
    
    def update(self, delta_time):
        super().update(delta_time)
        
