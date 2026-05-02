from game.environments.base import GameEnv


class Level4(GameEnv):
    def __init__(self):
        super().__init__(level_file="level4")
