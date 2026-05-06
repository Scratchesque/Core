# Rabbit Rush - graphics.py
#
# Created By: VizzWizz, BoredHF, HJParker2802, KamranBasra, TafaraMangombe, Vladikusss
#
# Source: https://github.com/Scratchesque/Core

from pygame import Surface, Rect

from game.core.constants import IMG_TILE_SIZE


# Gets a image and returns a list of available image surfaces to use
def tile_graphics(surface):
    # IMG_TILE_SIZE is the size of each SproutLand asset, eg 16x16
    tile_num_x = int(surface.get_size()[0] / IMG_TILE_SIZE)
    tile_num_y = int(surface.get_size()[1] / IMG_TILE_SIZE)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * IMG_TILE_SIZE
            y = row * IMG_TILE_SIZE
            new_surf = Surface((IMG_TILE_SIZE, IMG_TILE_SIZE)).convert_alpha()
            new_surf.blit(surface, (0, 0), Rect(x, y, IMG_TILE_SIZE, IMG_TILE_SIZE))
            new_surf.set_colorkey("black")
            cut_tiles.append(new_surf)

    return cut_tiles

# Gets a surface and returns a list of surfaces with the tiles cut out without blank gaps in the list, to make use for in animating the player
def cut_graphics(img_surface, sprite_col_start, sprite_row_start, sprite_gap):
    total_tiles_per_row = img_surface.get_height() // IMG_TILE_SIZE
    total_tiles_per_col = img_surface.get_width() // IMG_TILE_SIZE

    frames = []
    for start_col in range(sprite_row_start, total_tiles_per_row, 1 + sprite_gap):
        col = total_tiles_per_row * start_col
        for start_row in range(sprite_col_start, total_tiles_per_col, 1 + sprite_gap):
            frame_index = col + start_row
            frames.append(frame_index)

    return frames
