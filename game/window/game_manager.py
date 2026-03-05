from game.environments.level1 import Level1
from game.environments.level2 import Level2
from game.environments.level_select import LevelSelect
from game.window.display import Display


class GameManager:
    def __init__(self):
        self.envs_list = [
            LevelSelect("Main Menu"),
            Level1("Level 1"),
            Level2("Level 2"),
        ]
        self.display = Display()
        self.change_env("Main Menu")
        self.start()

    def start(self):
        try:
            self.load_level = False
            self.env.set_manager(self)
            self.display.run(self.env)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.exit_game()

    def change_env(self, env_title: str):
        self.display.stop_game_loop()
        self.load_level = True
        for env in self.envs_list:
            if env.title == env_title:
                self.env = env

    def exit_game(self):
        self.display.exit_screen()
        if self.load_level:
            self.start()
