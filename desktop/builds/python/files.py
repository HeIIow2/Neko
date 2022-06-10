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
    def __init__(self, neko: bool, hentai: bool, sfw: bool, random: bool, neko_tag: int = None,
                 neko_id: int = None, hentai_id: int = None):
        self.neko = neko
        self.hentai = hentai
        self.sfw = sfw
        self.random = random

        self.neko_tag = neko_tag
        self.neko_id = neko_id

        self.hentai_id = hentai_id

    def __eq__(self, other):
        if not isinstance(other, Options):
            return False

        return self.neko == other.neko and self.hentai == other.hentai and self.sfw == other.sfw and \
               self.random == other.random and self.neko_tag == other.neko_tag and self.neko_id == other.neko_id and \
                self.hentai_id == other.hentai_id


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

    def get_neko_quarry(self):
        return self.config["neko-quarry"]

    def set_neko_quarry(self, quarry):
        self.config["neko-quarry"] = quarry

    def get_hentai_quarry(self):
        return self.config["hentai-quarry"]

    def set_hentai_quarry(self, quarry):
        self.config["hentai-quarry"] = quarry

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

    def get_neko_focus(self):
        return self.config["focus"] == "neko"

    def set_neko_focus(self, focus: bool):
        print(f"set neko focus to {focus}")
        self.config["focus"] = "neko" if focus else "hentai"

    def get_hentai_focus(self):
        return self.config["focus"] == "hentai"

    def set_hentai_focus(self, focus: bool):
        print(f"set hentai focus to {focus}")
        self.config["focus"] = "hentai" if focus else "neko"

    def get_raw_button_properties(self, button: str):
        if button not in self.config["button-properties"]:
            return {"hentai": {}, "neko": {}, "keybindings": []}
        return self.config["button-properties"][button]

    def get_focus(self):
        return self.config["focus"]

    def get_button_properties(self, button: str):
        return self.get_raw_button_properties(button)[self.get_focus()]

    def get_button_keybindings(self, button: str):
        return self.get_raw_button_properties(button)[f"keybindings"]

    def get_api_url(self):
        return self.config["api-url"]

    def get_padding(self):
        return self.config["padding"]

    def get_caching_count(self):
        return self.config["caching-count"]

    def get_history_count(self):
        return self.config["history-count"]

    def save_config(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4)

    def get_options(self, neko_tags: dict):
        neko = self.get_neko_focus()
        hentai = self.get_hentai_focus()

        neko_id = None
        neko_tag = None

        hentai_id = None

        if neko:
            if self.neko_quarry.isdigit():
                neko_id = int(self.neko_quarry)
            else:
                if self.neko_quarry in neko_tags:
                    neko_tag = neko_tags[self.neko_quarry][0]
                else:
                    return None

        return Options(neko, hentai, self.sfw_filter, self.random_image, neko_tag, neko_id, hentai_id)

    window_title = property(fget=get_window_title, fset=set_window_tile)
    window_state = property(fget=get_window_state, fset=set_window_state)
    window_geometry = property(fget=get_window_geometry, fset=set_window_geometry)

    neko_quarry = property(fget=get_neko_quarry, fset=set_neko_quarry)
    hentai_quarry = property(fget=get_hentai_quarry, fset=set_hentai_quarry)
    sfw_filter = property(fget=get_sfw_filter, fset=set_sfw_filter)
    random_image = property(fget=get_random_image, fset=set_random_image)
    neko_focus = property(fget=get_neko_focus, fset=set_neko_focus)
    hentai_focus = property(fget=get_hentai_focus, fset=set_hentai_focus)
    padding = property(fget=get_padding)

    api_url = property(fget=get_api_url)
    caching_count = property(fget=get_caching_count)
    history_count = property(fget=get_history_count)
