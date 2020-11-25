import os
import json
from contextlib import contextmanager
from typing import Dict, Any, Iterator, List
from discord.ext import commands
import inspect

class ResNotFoundError(Exception):
    pass

def create_ine(path: str) -> None:
    file_name = path.split("/")[-1]
    folders = path.split("/")[:-1]

    path_accumulator = "./"

    for folder in folders:
        if not os.path.exists(path_accumulator + folder):
            os.makedirs(path_accumulator + folder)
        path_accumulator += folder + "/"

    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write("{}")


def update_res(fname: str, res: Dict[str, Any]) -> None:
    with open(f"./res/{fname}.json", "w") as f:
        json.dump(res, f)

def fetch_res(fname: str) -> Dict[str, Any]:
    with open(f"./res/{fname}.json", "r") as f:
        return json.load(f)

@contextmanager
def get_res(fname: str, update: bool=True) -> Iterator[Dict[str, Any]]:
    with open(f"./res/{fname}.json", "r") as f:
        res = json.load(f)

    try:
        yield res
    finally:
        if update:
            update_res(fname, res)

def get_string(sname: str, lang: str="en") -> str:
    strings = fetch_res("strings")

    try:
        if lang in strings[sname]:
            return strings[sname][lang]
        else:
            return strings[sname]["en"]
    except KeyError:
        raise ResNotFoundError(f"The string resource {sname} could not be found")

def get_config() -> Dict[str, Any]:
    with open("config.json", "r") as cfg:
        return json.load(cfg)

def feature_users(feature: str) -> List[int]:
    return    [ int(guild)
                for guild, config in fetch_res("local/guild_configurations").items()
                if feature in config["features"] ]

def update_config(updated_cfg: Dict[str, Any]) -> None:
    with open("config.json", "w") as cfg:
        json.dump(updated_cfg, cfg, indent=4)
