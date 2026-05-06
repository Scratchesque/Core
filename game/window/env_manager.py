# Rabbit Rush - env_manager.py
#
# Created By: VizzWizz, BoredHF, HJParker2802, KamranBasra, TafaraMangombe, Vladikusss
#
# Source: https://github.com/Scratchesque/Core

import importlib
import inspect
import pkgutil

import game.environments as environments_pkg
from game.core.paths import resolve_project_path
from game.environments.base import (
    BlockEnv,
    BaseEnvironment,
    CodeEnv,
    GameEnv,
    InterpreterEnv,
)
from game.support.files import load_json
from game.support.player_data import PlayerData
from game.window.display import Display


# This process is explained on trello under (Completed) 'Start getting the core of the program'
class EnvManager:
    def __init__(self, debug=False):
        self.debug = debug
        self.player_data = PlayerData()
        self.display = Display()
        self.envs_list = self._load_environments()
        self.change_env("Main Menu")

    def start(self):
        while True:
            try:
                self.load_level = False
                self.display.run(self.env)
            except Exception:
                import traceback

                traceback.print_exc()

            if not self.load_level:
                self.display.exit_screen()
                return

    def change_env(self, env_title: str):
        if env_title == "QUIT":
            self.display.stop_game_loop()
        elif env_title == "RESET":
            self.display.stop_game_loop()
            self.load_level = True
        else:
            matched = False
            for env in self.envs_list:
                if env.title == env_title:
                    matched = True
                    print(f"Found match: {env.title}")
                    self.display.stop_game_loop()
                    self.env = env
                    self.load_level = True
            if not matched:
                print(f"NO MATCH FOUND. Available: {[e.title for e in self.envs_list]}")

    def mark_level_completed(self, level_name, next_level_name=None):
        self.player_data.complete_level(level_name, next_level_name)

    def _load_environments(self):
        environments = []
        for module_info in sorted(
            pkgutil.iter_modules(environments_pkg.__path__), key=lambda m: m.name
        ):
            module_name = module_info.name

            if module_name in {"base", "__init__"} or module_name.startswith("_"):
                continue

            module = importlib.import_module(
                f"{environments_pkg.__name__}.{module_name}"
            )
            for _, cls in inspect.getmembers(module, inspect.isclass):
                if (
                    cls is BaseEnvironment
                    or cls is GameEnv
                    or not issubclass(cls, BaseEnvironment)
                ):
                    continue

                # Only load environment classes declared in this module/file.
                if cls.__module__ != module.__name__:
                    continue

                env = cls()
                env.game_manager = self
                environments.append(env)

        data_dir = resolve_project_path("game/environments/data")

        for f in sorted(data_dir.glob("*.json")):
            env = self._create_level_from_file(f.stem)
            if env is None:
                continue
            env.game_manager = self
            environments.append(env)

        if not environments:
            raise RuntimeError("No environments found in game/environments.")

        return environments

    def _create_level_from_file(self, level_file):
        env_data = load_json(f"game/environments/data/{level_file}.json")

        if not hasattr(env_data, "env"):
            raise ValueError(
                f"Environment data for '{level_file}' is missing an 'env' section."
            )

        if "level" in level_file:
            if env_data.env.type == "Block":
                return BlockEnv(level_file)
            elif env_data.env.type == "Interpreter":
                return InterpreterEnv(level_file)
            elif env_data.env.type == "Code":
                return CodeEnv(level_file)
        return None
