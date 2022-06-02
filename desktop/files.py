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

    def get_window_title(self):
        return self.config["window-title"]

    def set_window_tile(self, title):
        self.config["window-title"] = title
        self.save_config()

    def get_window_state(self):
        if self.config["window-maximized"]:
            return "zoomed"
        return "normal"

    def set_window_state(self, state):
        if state == "zoomed":
            self.config["window-maximized"] = True
        else:
            self.config["window-maximized"] = False
        self.save_config()

    def get_window_geometry(self):
        return f"{self.config['window-dimensions'][0]}x{self.config['window-dimensions'][1]}"

    def set_window_geometry(self, geometry):
        self.config["window-dimensions"] = [int(i) for i in geometry.split("x")]
        self.save_config()

    def get_quarry(self):
        return self.config["quarry"]

    def set_quarry(self, quarry):
        self.config["quarry"] = quarry
        self.save_config()

    def get_sfw_filter(self):
        return self.config["sfw-filter"]

    def set_sfw_filter(self, sfw_filter):
        self.config["sfw-filter"] = sfw_filter
        self.save_config()

    def get_random_image(self):
        return self.config["random"]

    def set_random_image(self, random):
        self.config["random"] = random
        self.save_config()

    def save_config(self):
        with open(self.path, "w") as f:
            json.dump(self.config, f)

    window_title = property(fget=get_window_title, fset=set_window_tile)
    window_state = property(fget=get_window_state, fset=set_window_state)
    window_geometry = property(fget=get_window_geometry, fset=set_window_geometry)

    quarry = property(fget=get_quarry, fset=set_quarry)
    sfw_filter = property(fget=get_sfw_filter, fset=set_sfw_filter)
    random_image = property(fget=get_random_image, fset=set_random_image)
