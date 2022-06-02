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

        self.window_title = self.config["window-title"]
        if self.config["window-maximized"]:
            self.window_state = "zoomed"
        else:
            self.window_state = "normal"
        self.window_geometry = f"{self.config['window-dimensions'][0]}x{self.config['window-dimensions'][1]}"

    def download_config(self):
        r = requests.get(CONFIG_URL)
        if r.status_code != 200:
            raise Exception("Config file could not be downloaded")

        with open(self.path, "w") as f:
            f.write(r.text)
