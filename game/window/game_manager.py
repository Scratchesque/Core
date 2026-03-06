import importlib
import inspect
import pkgutil
import re

import game.environments as environments_pkg
from game.environments.base import BaseEnvironment
from game.window.display import Display


class GameManager:
    def __init__(self):
        self.envs_list = self._load_environments()
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
                return

    def _load_environments(self):
        environments = []
        for module_info in sorted(pkgutil.iter_modules(environments_pkg.__path__), key=lambda m: m.name):
            module_name = module_info.name

            if module_name in {"base", "__init__"} or module_name.startswith("_"):
                continue

            module = importlib.import_module(f"{environments_pkg.__name__}.{module_name}")
            for _, cls in inspect.getmembers(module, inspect.isclass):
                if cls is BaseEnvironment or not issubclass(cls, BaseEnvironment):
                    continue

                # Only load environment classes declared in this module/file.
                if cls.__module__ != module.__name__:
                    continue
                
                print("loading environment", cls.title)
                environments.append(cls())

        if not environments:
            raise RuntimeError("No environments found in game/environments.")

        return environments

    # what if someone wanted to change the start an environment, either it would have to be first in the sorted list, or they would have look through all the environments if they didnt know to see which is true to set it to false so they can set theirs to run
    # better just set in here the main game manager init where to start off the program because main calls this class no?
    def _get_start_environment(self):
        for env in self.envs_list:
            if getattr(env, "START_ENV", False):
                return env

        # Fallback when no environment explicitly marks itself as start.
        return self.envs_list[0]

    # when scaling the project with more levels/environments, if someone were to delete/not use the env title, it falls back to the class name?
    # is it not better to set it inside the class init instead because it also for now sets the title name of the window and the names for levels in the main menu. if it were the class name things can get confusing so we should keep it consistent
    # cool regex tho
    def _title_from_class_name(self, class_name):
        with_spaces = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", class_name)
        with_spaces = re.sub(r"(?<=[A-Za-z])(?=[0-9])", " ", with_spaces)
        return with_spaces

    def exit_game(self):
        self.display.exit_screen()
        if self.load_level:
            self.start()
