import json
from typing import Dict

import config
from config.enums import Browser


def set_global_browser(name: str):
    if name.lower() == "edge":
        config.globals.global_browser = Browser.EDGE
    else:
        config.globals.global_browser = Browser.EDGE


def init_settings():
    try:
        with open("settings.json", "r", encoding="utf-8") as fin:
            settings: Dict = json.load(fin)
    except (json.JSONDecodeError, FileNotFoundError):
        settings = {}

    set_global_browser(settings.get("browser", "edge"))
