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
    def __init__(self, source: int, sfw: bool, random: bool, quarry: str):
        self.source = source
        self.sfw = sfw
        self.random = random

        self.quarry = quarry

    def __eq__(self, other):
        if not isinstance(other, Options):
            return False

        return self.source == other.source and self.sfw == other.sfw and self.random == other.random and self.quarry == other.quarry


class Config:
    def __init__(self):
        self.path = os.path.join(FILE_PATH, CONFIG_FILE)
        self.sources_map_name = {}
        self.sources_map_id = {}

        if not os.path.exists(self.path):
            print("Downloading config file...")
            self.download_config()

        with open(self.path, "r") as f:
            self.config = json.load(f)

        for source in self.config["sources"]:
            self.sources_map_name[source["name"]] = source
            self.sources_map_id[source["id"]] = source

    def __str__(self):
        string = ""
        for key, value in self.config.items():
            string += f"{key}: {value}\n"
        return string

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
        return self.get_current_source_data()["quarry"]

    def set_quarry(self, quarry):
        self.set_current_source_data("quarry", quarry)

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
        return self.config["button-properties"][button][str(self.current_source)]

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

    def get_options(self):
        return Options(self.get_source(), self.get_sfw_filter(), self.get_random_image(), self.get_quarry())

    def get_sources(self):
        return self.config["sources"]

    def get_source_data(self, source_id: int):
        return self.sources_map_id[source_id]

    def get_current_source_data(self):
        return self.get_source_data(self.current_source)

    def set_current_source_data(self, key, value):
        self.sources_map_id[self.current_source][key] = value

    def get_source_dropdown_options(self):
        return [source["name"] for source in self.get_sources()]

    def set_current_source(self, source_name: str):
        self.current_source = self.sources_map_name[source_name]["id"]

    def save_config(self):
        for i, source in enumerate(self.config["sources"]):
            self.config["sources"][i] = self.sources_map_id[self.config["sources"][i]["id"]]

        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4)


    show_messagebox = property(get_show_messagebox, set_show_messagebox)
    window_title = property(fget=get_window_title, fset=set_window_tile)
    window_state = property(fget=get_window_state, fset=set_window_state)
    window_geometry = property(fget=get_window_geometry, fset=set_window_geometry)

    quarry = property(fget=get_quarry, fset=set_quarry)
    sfw_filter = property(fget=get_sfw_filter, fset=set_sfw_filter)
    random_image = property(fget=get_random_image, fset=set_random_image)
    current_source = property(fget=get_source, fset=set_source)
    padding = property(fget=get_padding)

    caching_count = property(fget=get_caching_count)
    history_count = property(fget=get_history_count)
    sources = property(fget=get_sources)
