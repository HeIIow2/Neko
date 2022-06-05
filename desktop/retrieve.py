from copy import copy
import requests
import threading
import queue
from PIL import Image, ImageTk
from io import BytesIO
import random

import files

class Result:
    def __init__(self, id_, url, image: Image, sfw, translation, tags):
        self.id = id_
        self.url = url
        self.image = image
        self.sfw = sfw
        self.translation = translation
        self.tags = tags

    def get_description(self):
        sfw_text = "NSFW" if not self.sfw else "SFW"
        translation_text = "No translation" if self.translation is None else self.translation

        newline = "\n"

        return f"{self.id} {sfw_text}\n" \
               f"{self.translation}\n" \
               f"tags:\n" \
               f"{newline.join(self.tags)}"

    def get_image_tk(self):
        return ImageTk.PhotoImage(self.image)

    description = property(get_description)
    image_tk = property(get_image_tk)


class Options:
    def __init__(self, get_neko: bool, get_hentai: bool, get_sfw: bool, get_random: bool, tag: int = None,
                 id_: int = None):
        self.get_neko = get_neko
        self.get_hentai = get_hentai
        self.get_sfw = get_sfw
        self.get_random = get_random
        self.tag = tag
        self.id = id_
        self.filename = str(random.randint(0, 1000000)) + ".png"

    def __eq__(self, other):
        if not isinstance(other, Options):
            return False

        return self.get_neko == other.get_neko and \
               self.get_hentai == other.get_hentai and \
               self.get_sfw == other.get_sfw and \
               self.get_random == other.get_random and \
               self.tag == other.tag and \
               self.id == other.id


class Downloader(threading.Thread):
    def __init__(self,neko_api_url: str, work_queue: queue.Queue, result_queue: queue.Queue, prev_neko_id: int = None):
        super().__init__()
        self.session = requests.Session()
        self.session.body = {
            "program": "desktop"
        }

        self.work_queue = work_queue
        self.result_queue = result_queue

        self.neko_api_url = neko_api_url
        self.previous_neko_id = prev_neko_id

    def get_image_from_url(self, url):
        r = self.session.get(url)
        if r.status_code != 200:
            return None

        return Image.open(BytesIO(r.content))

    def get_neko_data_by_tag(self, tag: int, sfw: bool, random: bool):
        sfw_str = "sfw=1" if sfw else ""
        prev = "" if random else f"?prev={self.previous_neko_id}"
        r = self.session.get(f"{self.neko_api_url}image.php/?tag_id={tag}&{sfw_str}")
        return r.json()

    def cache_neko(self, options: Options):
        neko_data = None
        if options.tag is not None:
            neko_data = self.get_neko_data_by_tag(options.tag, options.get_sfw, options.get_random)

        if neko_data is None:
            return

        self.previous_neko_id = neko_data["id"]
        result = Result(neko_data["id"], neko_data["url"], self.get_image_from_url(neko_data["url"]), int(neko_data["sfw"]),
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
            if options.get_neko:
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

        self.session = requests.Session()
        self.session.body = {
            "program": "desktop"
        }

        self.all_tag_endpoint = "all_tag.php"
        self.tags = {

        }

        r = self.session.get(self.config.api_url + self.all_tag_endpoint)
        if r.status_code != 200:
            raise Exception(ConnectionError ,"Could not get tags")

        for tag in r.json():
            self.tags[tag["name"]] = (tag["id"], tag["frequency"])

        self.option = self.get_option()
        self.cache_neko()

        self.gui = None

    def set_gui(self, gui):
        self.gui = gui

    def get_option(self):
        if len(self.config.neko_quarry) <= 0:
            return

        id_ = None
        tag = None

        if self.config.neko_quarry.isdigit():
            id_ = int(self.config.neko_quarry)
        else:
            if self.config.neko_quarry in self.tags:
                tag = self.tags[self.config.neko_quarry][0]
            else:
                raise Exception("Tag not found")

        return Options(self.config.neko_focus, self.config.hentai_focus, self.config.sfw_filter, self.config.random_image, id_=id_, tag=tag)

    def get_all_tags(self):
        return "\n".join([f"{key} ({tag[1]})" for key, tag in self.tags.items()])

    def cache_neko(self):
        while self.result_queue.qsize() + self.work_queue.qsize() < self.config.caching_count:
            self.work_queue.put(self.get_option())

    def next(self, no_update: bool = False):
        temp_option = self.get_option()
        if temp_option != self.option:
            self.work_queue.queue.clear()
            self.result_queue.queue.clear()
            self.cache_neko()
            self.option = temp_option

        if self.result_queue.qsize() > 0:
            data = self.result_queue.get()
            self.cache_neko()

            return data

        while self.result_queue.empty():
            self.cache_neko()
            self.gui.window_update()

        data = self.result_queue.get()
        self.cache_neko()
        return data

    def terminate(self):
        self.work_queue.queue.clear()
        self.work_queue.put("terminate")

    all_tags = property(get_all_tags)
