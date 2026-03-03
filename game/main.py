from game.environments.level1 import Level1
from game.environments.level2 import Level2
from game.window.display import Display


def main_loop():
    level1 = Level1("Level1")
    level2 = Level2("Level2")

    main_window = Display() 
    main_window.init(level1)
    main_window.init(level2)


if __name__ == "__main__":
    main_loop()
