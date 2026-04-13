from game.core.constants import *

from csv import reader
from pygame import image, Surface, Rect

# Loads level csv in 'environments/map/{map_path}.CSV' to be used  
def import_map_layout(path):
    terrain_map = []
    with open(f"game/environments/map/{path}.csv") as map:
        level = reader(map,delimiter = ',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map
    
# Gets a image and crops it at a tile to return to use for rendering
def cut_graphics(surface):

    # IMG_TILE_SIZE is the size of each SproutLand asset, eg 16x16
    # So if we use another graphics that dont match 16x16 for the tiles, this needs to be changed
    tile_num_x = int(surface.get_size()[0] / IMG_TILE_SIZE)
    tile_num_y = int(surface.get_size()[1]/ IMG_TILE_SIZE)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * IMG_TILE_SIZE
            y = row * IMG_TILE_SIZE
            new_surf = Surface((IMG_TILE_SIZE,IMG_TILE_SIZE)).convert_alpha()
            new_surf.blit(surface,(0,0),Rect(x,y,IMG_TILE_SIZE,IMG_TILE_SIZE))
            new_surf.set_colorkey('black')
            cut_tiles.append(new_surf)
    
    return cut_tiles
