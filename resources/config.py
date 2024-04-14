from pathlib import Path
from typing import Any, Dict
import os
import yaml

path = os.getcwd() + "/config.yml"

def read_yaml() -> Dict[str, Any]:
    with open(path, "r") as file:
        return yaml.safe_load(file)

def telegram() -> Dict[str, Any]:
    return read_yaml()["Telegram"]


def database() -> Dict[str, Any]:
    return read_yaml()["database"]

def sqlite() -> Dict[str, Any]:
    return read_yaml()["sqlite"]


def postgresql() -> Dict[str, Any]:
    return read_yaml()["postgresql"]


def console() -> Dict[str, Any]:
    return read_yaml()["console"]