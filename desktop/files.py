import os
import os.path

FILE_PATH = "./external_files/"
TEMP_PATH = "./temp/"

CONFIG_FILE = "config.json"

if not os.path.exists(FILE_PATH):
    raise Exception("File path does not exist")

if not os.path.exists(TEMP_PATH):
    raise Exception("Temp path does not exist")

class Config:
    def __init__(self):
        self.path = os.path.join(FILE_PATH, CONFIG_FILE)
        if not os.path.exists(self.path):
            pass

    def download_config(self, url):
        pass
