from game.core.constants import *

from csv import reader
import pygame

def import_map_layout(path):
    terrain_map = []
    with open("game/environments/map/"+path+".csv") as map:
        level = reader(map,delimiter = ',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map
    
def cut_graphics(path, tile):
    surface = pygame.image.load(path).convert_alpha()

    tile_num_x = int(surface.get_size()[0] / IMG_TILE_SIZE)
    tile_num_y = int(surface.get_size()[1]/ IMG_TILE_SIZE)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * IMG_TILE_SIZE
            y = row * IMG_TILE_SIZE
            new_surf = pygame.Surface((IMG_TILE_SIZE,IMG_TILE_SIZE)).convert_alpha()
            new_surf.blit(surface,(0,0),pygame.Rect(x,y,IMG_TILE_SIZE,IMG_TILE_SIZE))
            new_surf.set_colorkey('black')
            cut_tiles.append(new_surf)
    
    return cut_tiles[int(tile)]
