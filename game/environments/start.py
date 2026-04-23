from game.environments.base import GameEnv


class StartLevel(GameEnv):
    def __init__(self):
        super().__init__(level_file="start")
