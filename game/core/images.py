from pygame import SRCALPHA, error, image

from game.core.paths import resolve_project_path


# Get absolute path of image and return alpha surface
def load_image(path: str):
    loaded = image.load(resolve_project_path(path))
    try:
        if loaded.get_flags() & SRCALPHA or loaded.get_alpha() is not None:
            return loaded.convert_alpha()
        return loaded.convert()
    except error:
        return loaded
