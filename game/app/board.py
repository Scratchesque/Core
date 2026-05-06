from pygame import Rect
from pygame_gui.elements import UIPanel

from game.app.tiles import Tile, Player, NPC
from game.core.constants import IMG_TILE_SIZE
from game.support.files import import_map_layout


# Render map layers and entity tiles (player/NPC/goal).
class Board(UIPanel):
    def __init__(self, panel_pos, panel_size, env_data, manager):
        # `starting_height` controls panel render order.
        # Place map elements in this panel container so they update/render together.
        super().__init__(
            Rect(panel_pos, panel_size),
            manager=manager,
            object_id="#game_panel",
            starting_height=1,
        )

        # Cached state used while building and rendering map tiles.
        self.env_data = env_data
        self.completed_level = False
        self.tiles_size = None
        self.board_offset = (0, 0)
        self.map_tiles = {}

        # Build tiles and entities from map data.
        self.create_ui()

    # Scale tiles to fit the panel while preserving map proportions.
    def _scale_tiles(self, width, height):
        if self.tiles_size is None:
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
        for element_type, element_data in self.env_data.map.__dict__.items():
            csv_map = element_data[0]
            if element_type == "start_pos":
                csv_map = element_data
            tile_img = element_data[1]
            self.map_tiles[element_type] = []
            csv_layout = import_map_layout(csv_map)
            height = len(csv_layout)
            for row_index, row in enumerate(csv_layout):
                width = len(row)
                self._scale_tiles(width, height)
                for col_index, tile_value in enumerate(row):
                    if tile_value != "-1":
                        tile = self.make_tile(col_index, row_index, tile_value, tile_img)
                        if element_type != "start_pos":
                            self.map_tiles[element_type].append(tile)

    def make_tile(self, x, y, tile_value, tile_img):
        match tile_value:
            case "g":  # Goal
                self.goal = Tile(
                    start_pos=(x, y),
                    tiles_size=self.tiles_size,
                    img_path="levels/carrot.webp",
                    manager=self.ui_manager,
                    container=self,
                    board_offset=self.board_offset,
                )
            case "p":  # Player
                self.player = Player(
                    start_pos=(x, y),
                    tiles_size=self.tiles_size,
                    map_tiles=self.map_tiles,
                    player_data=self.env_data.player,
                    manager=self.ui_manager,
                    container=self,
                    board_offset=self.board_offset,
                )
                self.player.change_layer(3)
            case "n":  # NPC
                self.npc = NPC(
                    start_pos=(x, y),
                    tiles_size=self.tiles_size,
                    npc_data=self.env_data.npc,
                    manager=self.ui_manager,
                    container=self,
                    board_offset=self.board_offset,
                )
                self.map_tiles["npc"] = [self.npc]
            case _:
                return Tile(
                    start_pos=(x, y),
                    tiles_size=self.tiles_size,
                    img_path=tile_img + ".png",
                    manager=self.ui_manager,
                    container=self,
                    tile=int(tile_value),
                    board_offset=self.board_offset,
                )
