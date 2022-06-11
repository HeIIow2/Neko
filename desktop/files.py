import os
import os.path
import requests
import json

FILE_PATH = "./external_files/"
TEMP_PATH = "./temp/"

CONFIG_FILE = "config.json"
CONFIG_URL = "https://raw.githubusercontent.com/HeIIow2/Neko/master/desktop/external_files/config.json"

if not os.path.exists(FILE_PATH):
    raise Exception("File path does not exist")

if not os.path.exists(TEMP_PATH):
    raise Exception("Temp path does not exist")

def save_temporary(img, name):
    img.save(os.path.join(TEMP_PATH, name))
    return os.path.join(TEMP_PATH, name)

class Options:
    def __init__(self, source: int, sfw: bool, random: bool, query: str):
        self.source = source
        self.sfw = sfw
        self.random = random

        self.query = query

    def __eq__(self, other):
        if not isinstance(other, Options):
            return False

        return self.source == other.source and self.sfw == other.sfw and self.random == other.random and self.query == other.query


class Config:
    def __init__(self):
        self.path = os.path.join(FILE_PATH, CONFIG_FILE)
        if not os.path.exists(self.path):
            print("Downloading config file...")
            self.download_config()

        with open(self.path, "r") as f:
            self.config = json.load(f)

    def __str__(self):
        for key, value in self.config.items():
            print(f"{key}: {value}")

    def download_config(self):
        r = requests.get(CONFIG_URL)
        if r.status_code != 200:
            raise Exception("Config file could not be downloaded")

        with open(self.path, "w") as f:
            f.write(r.text)

    def get_show_messagebox(self):
        return self.config["show-messagebox"]

    def set_show_messagebox(self, show: bool):
        self.config["show-messagebox"] = bool(show)

    def get_window_title(self):
        return self.config["window-title"]

    def set_window_tile(self, title):
        self.config["window-title"] = title

    def get_window_state(self):
        if self.config["window-maximized"]:
            return "zoomed"
        return "normal"

    def set_window_state(self, state):
        if state == "zoomed":
            self.config["window-maximized"] = True
        else:
            self.config["window-maximized"] = False

    def get_window_geometry(self):
        return f"{self.config['window-dimensions'][0]}x{self.config['window-dimensions'][1]}"

    def set_window_geometry(self, geometry):
        self.config["window-dimensions"] = [int(i) for i in geometry.split("x")]

    def get_quarry(self):
        return self.config["quarry"]

    def set_quarry(self, quarry):
        self.config["quarry"] = quarry

    def get_sfw_filter(self):
        return self.config["sfw"]

    def set_sfw_filter(self, sfw_filter: bool):
        print(f"set sfw filter to {sfw_filter}")
        self.config["sfw"] = bool(sfw_filter)

    def get_random_image(self):
        return self.config["random"]

    def set_random_image(self, random: bool):
        print(f"set random image to {random}")
        self.config["random"] = bool(random)

    def get_source(self):
        return self.config["source"]

    def set_source(self, source: int):
        self.config["source"] = source

    def get_button_properties(self, button: str):
        if button not in self.config["button-properties"]:
            return {}
        return self.config["button-properties"][button][str(self.source)]

    def get_button_keybindings(self, button: str):
        if button not in self.config["button-properties"]:
            return []
        return self.config["button-properties"][button]["keybindings"]

    def get_padding(self):
        return self.config["padding"]

    def get_caching_count(self):
        return self.config["caching-count"]

    def get_history_count(self):
        return self.config["history-count"]

    def save_config(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4)

    def get_options(self):
        return Options(self.get_source(), self.get_sfw_filter(), self.get_random_image(), self.get_quarry())

    show_messagebox = property(get_show_messagebox, set_show_messagebox)
    window_title = property(fget=get_window_title, fset=set_window_tile)
    window_state = property(fget=get_window_state, fset=set_window_state)
    window_geometry = property(fget=get_window_geometry, fset=set_window_geometry)

    quarry = property(fget=get_quarry, fset=set_quarry)
    sfw_filter = property(fget=get_sfw_filter, fset=set_sfw_filter)
    random_image = property(fget=get_random_image, fset=set_random_image)
    source = property(fget=get_source, fset=set_source)
    padding = property(fget=get_padding)

    caching_count = property(fget=get_caching_count)
    history_count = property(fget=get_history_count)
