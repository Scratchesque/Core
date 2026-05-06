# Rabbit Rush - player_data.py
#
# Created By: VizzWizz, BoredHF, HJParker2802, KamranBasra, TafaraMangombe, Vladikusss
#
# Source: https://github.com/Scratchesque/Core

import json

from game.core.paths import resolve_project_path


# This class contains logic for saving player progress 
class PlayerData:
    DEFAULT_UNLOCKED_LEVELS = ["Start"]

    def __init__(self, relative_path="game/player_data.json"):
        self.path = resolve_project_path(relative_path)
        self.completed_levels = set()
        self.unlocked_levels = set(self.DEFAULT_UNLOCKED_LEVELS)
        self.load()

    def load(self):
        if not self.path.exists():
            self.save()
            return

        with self.path.open("r", encoding="utf-8") as save_file:
            data = json.load(save_file)

        self.completed_levels = set(data.get("completed_levels", []))
        self.unlocked_levels = set(data.get("unlocked_levels", self.DEFAULT_UNLOCKED_LEVELS))
        if not self.unlocked_levels:
            self.unlocked_levels = set(self.DEFAULT_UNLOCKED_LEVELS)

    def save(self):
        data = {
            "completed_levels": sorted(self.completed_levels),
            "unlocked_levels": sorted(self.unlocked_levels),
        }
        with self.path.open("w", encoding="utf-8") as save_file:
            json.dump(data, save_file, indent=2)

    def is_unlocked(self, level_name):
        return level_name in self.unlocked_levels

    def is_completed(self, level_name):
        return level_name in self.completed_levels

    def complete_level(self, level_name, next_level_name=None):
        self.completed_levels.add(level_name)
        if next_level_name and next_level_name != "QUIT":
            self.unlocked_levels.add(next_level_name)
        self.save()
