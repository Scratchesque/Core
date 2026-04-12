from pygame import Rect
from pygame_gui.elements import UIPanel
from game.core.csv_support import *
from game.core.constants import *
from game.app.elements import *
from pygame_gui.windows import UIConfirmationDialog 

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

        # Render the tiles
        self.create_ui()
        self.init_level()

    # Gets the size of this panel container, and divdes it by the ammount of tiles in the level to get the size of the tile 
    def _scale_tiles(self):
        if self.tiles_size == None:
            x = self.get_relative_rect().size[0] // self.tiles_amm[0]
            y = self.get_relative_rect().size[1] // self.tiles_amm[1]
            self.tiles_size = [x,y]

    def create_ui(self):
        # also i realise by having tiles created like this makes it harder to program collisions
        # need to change this somehow so objects can tell where they are on the map maybe somehow
        # maybe use collisions like in code blocks, where it uses the 'object_id'

        # Gets the relevant information about each map file in the board data at the loaded json, then scales and renders each tile in each file
        for csv_map, asset_img in self.board_data.map.__dict__.items():
            csv_layout = import_map_layout(csv_map)
            height = len(csv_layout)
            for row_index, row in enumerate(csv_layout):
                width = len(row)
                self.tiles_amm = (width,height)
                self._scale_tiles()
                for col_index, val in enumerate(row):
                    if val != '-1':
                        Tile(start_pos=(col_index,row_index), 
                            tiles_size=self.tiles_size, 
                            tiles_amm=self.tiles_amm, 
                            img_path=asset_img+".png", 
                            manager=self.ui_manager, 
                            container=self, 
                            tile=val)

    def init_level(self):
        # Uses random sprites I found in the assets folder and sets their position based on the json loaded
        self.goal = Tile(start_pos=(self.board_data.start_pos.goal), 
            tiles_size=self.tiles_size, 
            tiles_amm=self.tiles_amm, 
            img_path='SproutLands/Objects/Basic Grass Biom things 1.png', 
            manager=self.ui_manager, 
            container=self, 
            tile=20)
        self.player = Tile(start_pos=(self.board_data.start_pos.player), 
            tiles_size=self.tiles_size, 
            tiles_amm=self.tiles_amm, 
            img_path='SproutLands/Characters/Free Chicken Sprites.png', 
            manager=self.ui_manager, 
            container=self, 
            tile=0)

    # Having super().process_event(event) or super().update(delta_time) inside the panel eliminates the need to call these functions outside of this class
    # With pygame_gui Since we passthrough the ui manager, it inherites UIPanel (or any element in pygame_gui.elements) and does its own initalisation which allows us to process events in each class
    def process_event(self, event):
        super().process_event(event)
        if self.goal.collision_check(self.player):
            if self.completed_level == False:
                self.completed_level = True
                rect = Rect((SCREEN_WIDTH // 2, SCREEN_HEIGHT //2), (300, 300)) 
                UIConfirmationDialog(rect=rect, 
                    action_long_desc="You Win!", 
                    manager=self.ui_manager)
    
    def update(self, delta_time):
        super().update(delta_time)
