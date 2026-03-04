from game.environments.level1 import Level1
from game.environments.level2 import Level2
from game.environments.level_select import LevelSelect
from game.window.display import Display


def main_loop():

    main_window = Display()

    main_window.set_environments([
            LevelSelect("Main Menu"),
            Level1("Level 1"),
            Level2("Level 2"),
        ]
    )
    main_window.change_env("Main Menu")
    main_window.run()


if __name__ == "__main__":
    main_loop()
