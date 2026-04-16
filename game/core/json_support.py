import json
from types import SimpleNamespace

from game.core.paths import resolve_project_path

# chatgpt made this for me cause i didnt have a clue, but it goes through each {} in the json and returns result to get added to the env_data
def dict_to_namespace(dictionary):
    if isinstance(dictionary, dict):
        return SimpleNamespace(**{k: dict_to_namespace(v) for k, v in dictionary.items()})
    elif isinstance(dictionary, list):
        return [dict_to_namespace(item) for item in dictionary]
    else:
        return dictionary

# This turns a json into a.b.c variables that we can use to get values
def load_json(file_path):
    try:
        path = resolve_project_path(file_path)
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        data_list = dict_to_namespace(data)
        data_list.env.init # checks if init data exists inside jsons at 'environments/data/xxx.json' 
        return data_list
    except:
        return False
       
