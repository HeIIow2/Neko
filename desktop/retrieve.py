import PIL
import requests
import threading
import queue
from PIL import Image, ImageTk
from io import BytesIO
import numpy as np

import files


class Result:
    def __init__(self, src: int):
        self.src = src

        self.id_ = None
        self.url = None
        self.image = None
        self.sfw = None
        self.translation = None
        self.tags = None

        self.base_color = None
        self.text_base_color = None
        self.elem_color = None
        self.text_elem_color = None

    def __str__(self):
        sfw_text = "NSFW" if not self.sfw else "SFW"
        translation_text = "" if self.translation is None else self.translation

        newline = "\n"

        return f"{self.id_} {sfw_text}\n" \
               f"{translation_text}\n" \
               f"tags:\n" \
               f"{newline.join(self.tags)}"

    def set_id(self, id_: int):
        self.id_ = id_

    def set_url(self, url: str):
        self.url = url

    def set_image(self, image: Image):
        self.image = image.convert("RGB")

        text_threshold = 140
        brighten_value = 20

        base_color_r = self.image.resize((1, 1)).getpixel((0, 0))
        self.base_color = self.rgb_to_hex(base_color_r)
        self.text_base_color = "#000" if np.average(base_color_r) > text_threshold else "#fff"
        elem_color_r = [255 if color + brighten_value > 255 else color + brighten_value for color in base_color_r]
        self.elem_color = self.rgb_to_hex(elem_color_r)
        self.text_elem_color = "#000" if np.average(elem_color_r) > text_threshold else "#fff"

    def set_sfw(self, sfw: bool):
        self.sfw = sfw

    def set_translation(self, translation: str):
        self.translation = translation

    def set_tags(self, tags: list):
        self.tags = tags

    def rgb_to_hex(self, rgb):
        return "#%02x%02x%02x" % tuple(rgb)

    def get_image_tk(self):
        return ImageTk.PhotoImage(self.image)

    image_tk = property(get_image_tk)


class Downloader(threading.Thread):
    def __init__(self, new_request_queue: queue.Queue, work_queue: queue.Queue, prev_work_queue: queue.Queue,
                 result_queue: queue.Queue, prev_result_queue: queue.Queue, hellow_neko_tags: dict):
        super().__init__()
        self.session = requests.Session()
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
        }
        self.session.body = {
            "program": "desktop"
        }

        self.new_request_queue = new_request_queue
        self.work_queue = work_queue
        self.prev_work_queue = prev_work_queue
        self.result_queue = result_queue
        self.prev_result_queue = prev_result_queue

        self.last_working_options = None
        self.last_working_endpoint = None

        self.prev_neko_id = 1592

        self.hellow_neko_tags = hellow_neko_tags

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

    def interpret_options(self, options: files.Options, prev=False):
        if options == self.last_working_options:
            return self.last_working_endpoint

        if options.source == 0:
            prev_next = "prev" if not prev else "next"

            from_ = None
            if options.query.isdigit():
                from_ = f"?image_id={options.query}"
            elif options.query in self.hellow_neko_tags:
                from_ = f"?tag_id={self.hellow_neko_tags[options.query][0]}"

            if from_ is None:
                print(f"Could not find tag {options.query}")
                return None

            sfw_str = "&sfw=1" if options.sfw else ""
            rand_str = "" if options.random else f"&{prev_next}={self.prev_neko_id}"

            return f"image.php/{from_}{sfw_str}{rand_str}"

    def get_from_hellow_neko(self, options: files.Options, prev=False):
        api = "https://ln.topdf.de/HellowNekoNew/api/"

        endpoint = self.interpret_options(options, prev)
        if endpoint is None:
            return None

        url = f"{api}{endpoint}"
        print(url)
        try:
            r = self.session.get(url)
            if r.status_code != 200 or r.text == "404":
                return None
        except requests.exceptions.RequestException:
            return None

        data = r.json()
        image = self.get_image_from_url(data["url"])
        if image is None:
            return None

        result = Result(options.source)
        result.image = image
        result.set_id(data["id"])
        result.set_url(data["url"])
        result.set_sfw(bool(data["sfw"]))
        result.set_translation(data["translation"])
        result.set_tags(data["tags"])

        return result, endpoint

    def get_from_src(self, options: files.Options, prev=False):
        if options.source == 0:
            return self.get_from_hellow_neko(options, prev)

    def run(self):
        while True:
            if not self.new_request_queue.empty():
                with self.result_queue.mutex:
                    self.result_queue.queue.clear()
                options = self.new_request_queue.get()

                if options == "terminate":
                    return

                result = self.get_from_src(options)
                if result is not None:
                    data, endpoint = result
                    with self.work_queue.mutex:
                        self.work_queue.queue.clear()
                    self.result_queue.put(data)

                    self.last_working_options = options
                    self.last_working_endpoint = endpoint
                else:
                    self.result_queue.put(self.last_working_options.query)

                continue

            if not self.prev_work_queue.empty():
                options = self.prev_work_queue.get()
                result, endpoint = self.get_from_src(options, prev=True)
                if result is not None:
                    self.prev_result_queue.put(result)

                continue

            if not self.work_queue.empty():
                options = self.work_queue.get()

                if options == "terminate":
                    return

                result = self.get_from_src(options)
                if result is not None:
                    data, endpoint = result
                    self.result_queue.put(data)

                    self.last_working_options = options
                    self.last_working_endpoint = endpoint

                continue


class Api:
    def __init__(self, config: files.Config):
        self.config = config

        self.history = []
        self.index = -1

        self.session = requests.Session()
        self.session.body = {"program": "desktop"}

        self.all_tag_endpoint = "all_tag.php"
        self.hellow_neko_tags = {}
        self.autocomplete_tags = []

        r = self.session.get("https://ln.topdf.de/HellowNekoNew/api/all_tag.php")
        if r.status_code != 200:
            raise Exception(ConnectionError, "Could not get tags")
        for tag in r.json():
            self.hellow_neko_tags[tag["name"]] = (int(tag["id"]), int(tag["frequency"]))
            self.autocomplete_tags.append(tag["name"])

        self.new_request_queue = queue.Queue()
        self.work_queue = queue.Queue()
        self.prev_work_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.prev_result_queue = queue.Queue()
        self.thread = Downloader(self.new_request_queue, self.work_queue, self.prev_work_queue, self.result_queue,
                                 self.prev_result_queue, hellow_neko_tags=self.hellow_neko_tags)
        self.thread.start()

        self.gui = None

        self.requested_next = False
        self.requested_prev = False
        self.from_index = False
        self.request_next()

    def get_all_tags(self):
        return "\n".join([f"{key} ({tag[1]})" for key, tag in self.hellow_neko_tags.items()])

    def fill_work_queue(self):
        while self.result_queue.qsize() + self.work_queue.qsize() < self.config.caching_count:
            self.work_queue.put(self.config.get_options())

    def get_previous(self):
        return self.history[self.index]

    def request_next(self, browse=False):
        if browse:
            self.history = self.history[:self.index + 1]
            self.new_request_queue.put(self.config.get_options())
            self.requested_next = True
            self.from_index = False
            return

        if self.index < len(self.history) - 1:
            self.from_index = True
            self.index += 1

        # fill up the work queue
        self.fill_work_queue()
        self.requested_next = True

    def request_prev(self):
        if self.index > 0:
            self.index -= 1
            self.from_index = True
        else:
            self.prev_work_queue.put(self.config.get_options())

        self.requested_prev = True

    def get_request(self):
        self.fill_work_queue()
        if not self.requested_next and not self.requested_prev:
            return None

        if self.requested_next:
            if self.result_queue.empty() and not self.from_index:
                return None

            self.requested_next = False

            if self.from_index:
                self.from_index = False
                self.requested_next = False
                return self.history[self.index]

            result = self.result_queue.get()
            if not isinstance(result, str):
                self.history.append(result)
                self.index += 1

                while len(self.history) > self.config.history_count:
                    self.index -= 1
                    self.history.pop(0)

                self.fill_work_queue()

            return result

        if self.requested_prev:
            if self.prev_result_queue.empty() and not self.from_index:
                return None

            self.requested_prev = False

            if self.from_index:
                self.from_index = False
                return self.history[self.index]

            result = self.prev_result_queue.get()
            self.history.insert(0, result)
            self.index = 0

            return result

    def terminate(self):
        self.work_queue.queue.clear()
        self.work_queue.put("terminate")

    all_tags = property(get_all_tags)
