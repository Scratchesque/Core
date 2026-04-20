from game.environments.base import GameEnv
from game.app.panels import DialoguePanel
from game.core.constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Level1(GameEnv):
    def __init__(self):
        super().__init__(level_file="start")

        # Here we will make each level different to teach the user about each new thing individually (maybe?)
        