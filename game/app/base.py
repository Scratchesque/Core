from game.app.board import Board
from game.core.constants import *

class MainApp:
    def __init__(self, level_data, manager):
        self.board = Board((50,50), SCREEN_HEIGHT-100, level_data.board, manager)

