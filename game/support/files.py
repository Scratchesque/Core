# Rabbit Rush - files.py
#
# Created By: VizzWizz, BoredHF, HJParker2802, KamranBasra, TafaraMangombe, Vladikusss
#
# Source: https://github.com/Scratchesque/Core

import json
from types import SimpleNamespace
from csv import reader

from game.core.paths import resolve_project_path


# Load level CSV map data from `game/environments/map/`.
def import_map_layout(path):
    terrain_map = []
    with open(
        resolve_project_path(f"game/environments/map/{path}.csv"), encoding="utf-8"
    ) as map:
        level = reader(map, delimiter=",")
        for row in level:
            terrain_map.append(list(row))
        return terrain_map


# Recursively convert dict/list JSON data into namespaces.
def _dict_to_namespace(dictionary):
    if isinstance(dictionary, dict):
        return SimpleNamespace(
            **{k: _dict_to_namespace(v) for k, v in dictionary.items()}
        )
    elif isinstance(dictionary, list):
        return [_dict_to_namespace(item) for item in dictionary]
    else:
        return dictionary


# Load JSON file and expose nested values via dot-access namespaces.
def load_json(file_path):
    path = resolve_project_path(file_path)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return _dict_to_namespace(data)
