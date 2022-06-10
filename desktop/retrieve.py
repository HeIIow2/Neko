from copy import copy

import PIL
import requests
import threading
import queue
from PIL import Image, ImageTk
from io import BytesIO
import numpy as np

import files


class Result:
    def __init__(self, id_, url, image: Image, sfw, translation, tags):
        self.id = id_
        self.url = url
        self.image = image.convert("RGB")
        self.sfw = sfw
        self.translation = translation
        self.tags = tags

        text_threshold = 140
        brighten_value = 20

        base_color_r = self.image.resize((1, 1)).getpixel((0, 0))
        self.base_color = self.rgb_to_hex(base_color_r)
        self.text_base_color = "#000" if np.average(base_color_r) > text_threshold else "#fff"
        elem_color_r = [255 if color+brighten_value > 255 else color+brighten_value for color in base_color_r]
        self.elem_color = self.rgb_to_hex(elem_color_r)
        self.text_elem_color = "#000" if np.average(elem_color_r) > text_threshold else "#fff"

    def rgb_to_hex(self, rgb):
        return "#%02x%02x%02x" % tuple(rgb)

    def get_description(self):
        sfw_text = "NSFW" if not self.sfw else "SFW"
        translation_text = "" if self.translation is None else self.translation

        newline = "\n"

        return f"{self.id} {sfw_text}\n" \
               f"{translation_text}\n" \
               f"tags:\n" \
               f"{newline.join(self.tags)}"

    def get_image_tk(self):
        return ImageTk.PhotoImage(self.image)

    description = property(get_description)
    image_tk = property(get_image_tk)


class Downloader(threading.Thread):
    def __init__(self, neko_api_url: str, work_queue: queue.Queue, result_queue: queue.Queue, prev_neko_id: int = None):
        super().__init__()
        self.session = requests.Session()
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
        }
        self.session.body = {
            "program": "desktop"
        }

        self.work_queue = work_queue
        self.result_queue = result_queue

        self.neko_api_url = neko_api_url
        self.previous_neko_id = prev_neko_id

    def get_image_from_url(self, url):
        print(f"Downloading image from {url}")
        try:
            r = self.session.get(url)
            if r.status_code != 200:
                return None
        except requests.exceptions.RequestException:
            return None

        try:
            image = Image.open(BytesIO(r.content))
        except PIL.UnidentifiedImageError:
            return None

        return image

    def get_neko_data_by_tag(self, tag: int, sfw: bool, random: bool):
        sfw_str = "&sfw=1" if sfw else ""
        prev = "" if random else f"&prev={self.previous_neko_id}"
        r = self.session.get(f"{self.neko_api_url}image.php/?tag_id={tag}{sfw_str}{prev}")
        return r.json()

    def get_neko_data_by_id(self, neko_id: int):
        r = self.session.get(f"{self.neko_api_url}image.php?image_id={neko_id}")
        return r.json()

    def cache_neko(self, options: files.Options):
        neko_data = None
        if options.neko_tag is not None:
            neko_data = self.get_neko_data_by_tag(options.neko_tag, options.sfw, options.random)
        elif options.neko_id is not None:
            neko_data = self.get_neko_data_by_id(options.neko_id)

        if neko_data is None:
            return

        self.previous_neko_id = neko_data["id"]
        image = self.get_image_from_url(neko_data["url"])
        if image is None:
            print(f"Failed to download image{neko_data['url']}")
            return self.cache_neko(options)
        result = Result(neko_data["id"], neko_data["url"], image, int(neko_data["sfw"]),
                        neko_data["translation"], neko_data["tags"])
        return result

    def run(self):
        while True:
            if not self.work_queue.qsize():
                continue

            options = self.work_queue.get()
            if options == "terminate":
                return

            data = None
            if options.neko:
                data = self.cache_neko(options)

            if data is not None:
                self.result_queue.put(data)


class Api:
    def __init__(self, config: files.Config):
        self.config = config
        self.work_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.thread = Downloader(copy(self.config.api_url), self.work_queue, self.result_queue)
        self.thread.start()
        self.history = []
        self.prev_index = -1

        self.session = requests.Session()
        self.session.body = {
            "program": "desktop"
        }

        self.all_tag_endpoint = "all_tag.php"
        self.tags = {

        }

        r = self.session.get(self.config.api_url + self.all_tag_endpoint)
        if r.status_code != 200:
            raise Exception(ConnectionError, "Could not get tags")

        for tag in r.json():
            self.tags[tag["name"]] = (tag["id"], tag["frequency"])

        self.option = self.get_option()
        self.gui = None

        self.requested = False
        self.request()

    def set_gui(self, gui):
        self.gui = gui

    def get_option(self):
        return self.config.get_options(self.tags)

    def get_all_tags(self):
        return "\n".join([f"{key} ({tag[1]})" for key, tag in self.tags.items()])

    def fill_work_queue(self):
        while self.result_queue.qsize() + self.work_queue.qsize() < self.config.caching_count:
            self.work_queue.put(self.get_option())

    def get_previous(self):
        if len(self.history) <= abs(self.prev_index):
            return None

        self.prev_index -= 1
        return self.history[self.prev_index]

    def request(self):
        # if the input quarry changed,
        # the work queue gets cleared
        temp_option = self.get_option()
        if temp_option != self.option:
            self.work_queue.queue.clear()
            self.result_queue.queue.clear()
            self.option = temp_option

        # fill up the work queue
        while self.result_queue.qsize() + self.work_queue.qsize() < self.config.caching_count:
            self.work_queue.put(self.get_option())

        self.requested = True

    def get_request(self):
        if not self.requested:
            return None

        if self.prev_index < -1:
            self.prev_index += 1
            self.requested = False
            return self.history[self.prev_index]

        if self.result_queue.empty():
            return None

        self.requested = False
        result = self.result_queue.get()
        # append to history
        self.history.append(result)
        if len(self.history) > self.config.history_count:
            self.history.pop(0)
        self.fill_work_queue()
        return result

    def terminate(self):
        self.work_queue.queue.clear()
        self.work_queue.put("terminate")

    all_tags = property(get_all_tags)
