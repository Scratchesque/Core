from pygame import Rect
from pygame_gui.elements import UIPanel
from game.core.csv_support import *
from game.core.constants import *
from game.app.elements import TiledElement
from pygame_gui.windows import UIConfirmationDialog 

class Board(UIPanel):
    def __init__(self, env_data, manager):
        super().__init__(Rect(env_data.board_pos, env_data.board_size), manager=manager, object_id="#board_background", starting_height=1)
        # beceause its in a panel now, any elements place outside the container arent rendered, so the level can be very but zoomed in on some tiles 
        self.env_data = env_data
        self.manager = manager

        self.completed_level = False

        self.tiles_size = None
        self.create_frame()
        
        self.init_level()

    def _scale_tiles(self):
        if self.tiles_size == None:
            x = self.env_data.board_size[0] // self.tiles_amm[0]
            y = self.env_data.board_size[1] // self.tiles_amm[1]
            self.tiles_size = [x,y]

    def create_frame(self):
        # also i realise by having tiles created like this makes it harder to program collisions
        # need to change this somehow so objects can tell where they are on the map maybe somehow
        for csv_map, asset_img in self.env_data.map.__dict__.items():
            csv_layout = import_map_layout(csv_map)
            height = len(csv_layout)
            for row_index, row in enumerate(csv_layout):
                width = len(row)
                self.tiles_amm = (width,height)
                self._scale_tiles()
                for col_index, val in enumerate(row):
                    if val != '-1':
                        TiledElement((col_index,row_index), self.tiles_size, self.tiles_amm, asset_img+".png", self.ui_manager, self.panel_container, tile=val)

    def init_level(self):    
        self.carrot = TiledElement((self.env_data.start_pos.carrot), self.tiles_size, self.tiles_amm, 'levels/carrot.png', self.manager, self.panel_container)
        self.player = TiledElement(self.env_data.start_pos.player, self.tiles_size, self.tiles_amm, 'SproutLands/Characters/Free Chicken Sprites.png', self.manager, self.panel_container, tile=0)


    def process_event(self, event):
        if self.carrot.collision_check(self.player):
            if self.completed_level == False:
                self.completed_level = True
                rect = Rect((SCREEN_WIDTH // 2, SCREEN_HEIGHT //2), (300, 300)) 
                UIConfirmationDialog(rect, "You Win!", self.ui_manager)
        return super().process_event(event)
