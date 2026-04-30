from game.environments.base import GameEnv


class Level1(GameEnv):
    def __init__(self):
        super().__init__(level_file="level1")

        # Here we will make each level different to teach the user about each new thing individually (maybe?)
        