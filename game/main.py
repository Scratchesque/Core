from game.window.display import Display as main_window
from game.environments.level1 import Level1

def main_loop():
    level1 = Level1("Level1")
    level2 = Level1("Level2")

    main_window.start(level1)
    main_window.start(level2)

    
if __name__ == '__main__':
    main_loop()
   
    