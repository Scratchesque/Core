from pygame import Color

class BaseEnvironment():
    def __init__(self, title:str, hex:int, theme:str=None):
        self.title = title
        self.background = Color(f'#{hex}')
        self.theme_path = f'game/themes/{theme}.json'
    
    def setup(self):
        pass
    
    def loop(self):
        pass