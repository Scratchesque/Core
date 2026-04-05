import importlib
import inspect
import pkgutil

import game.environments as environments_pkg
from game.environments.base import BaseEnvironment
from game.window.display import Display


class GameManager:
    def __init__(self):
        self.envs_list = self._load_environments()
        self.display = Display()
        self.change_env("Main Menu")

    def start(self):
        try:
            self.load_level = False
            self.env.set_manager(self)
            self.display.run(self.env)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.quit_load_level()

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
                
                environments.append(cls())

        if not environments:
            raise RuntimeError("No environments found in game/environments.")

        return environments

    def quit_load_level(self):
        if self.load_level:
            self.start()
        else:
            self.display.exit_screen()

