from pygame import Color

class BaseEnvironment():
    def __init__(self, title, hex):
        self.title = title
        self.background = Color(f'#{hex}')
    
    def setup(self):
        pass
    
    def loop(self):
        pass