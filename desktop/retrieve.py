import queue
import threading
import numpy as np

from io import BytesIO
import PIL
from PIL import Image, ImageTk

import requests
from urllib.parse import urljoin

import files


def get_request_session():
    session = requests.Session()
    session.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
    session.body = {"program": "desktop"}
    return session

def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % tuple(rgb)

class AllTags:
    def __init__(self, current_src: int):
        self.current_src = current_src

        self.result_queue = queue.Queue()
        self.tags_dict = {}

    def __str__(self):
        return "\n".join([str(tag) for tag in self.get_tags(self.current_src)])

    def get_tags_r(self, src: int):
        if src in self.tags_dict:
            return self.tags_dict[src]

        while not self.result_queue.empty():
            src, tags = self.result_queue.get()
            self.tags_dict[src] = tags

        if src in self.tags_dict:
            return self.tags_dict[src]

    def get_tags(self, src: int):
        tag_list = self.get_tags_r(src)
        if tag_list is None:
            return []
        return tag_list

    def get_id_by_name(self, name: str):
        for tag in self.get_tags(self.current_src):
            if tag.name == name:
                return tag.id

        return None

    def get_autocomplete_tags(self):
        return [tag.name for tag in self.get_tags(self.current_src)]

class Result:
    def __init__(self, src: int, quarry: str):
        self.src = src
        self.quarry = quarry

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
        self.base_color = rgb_to_hex(base_color_r)
        self.text_base_color = "#000" if np.average(base_color_r) > text_threshold else "#fff"
        elem_color_r = [255 if color + brighten_value > 255 else color + brighten_value for color in base_color_r]
        self.elem_color = rgb_to_hex(elem_color_r)
        self.text_elem_color = "#000" if np.average(elem_color_r) > text_threshold else "#fff"

    def set_sfw(self, sfw: bool):
        self.sfw = sfw

    def set_translation(self, translation: str):
        self.translation = translation

    def set_tags(self, tags: list):
        self.tags = tags

    def get_image_tk(self):
        return ImageTk.PhotoImage(self.image)

    image_tk = property(get_image_tk)

class GetData:
    def __init__(self):
        self.session = get_request_session()

    def get_request(self, url: str):
        try:
            r = self.session.get(url)
            if r.status_code != 200:
                return None
            return r
        except requests.exceptions.RequestException:
            return None

    def get_image_from_url(self, url):
        print(f"Getting image from {url}")
        r = self.get_request(url)
        try:
            image = Image.open(BytesIO(r.content))
        except PIL.UnidentifiedImageError:
            return None

        return image

class HellowNeko(GetData):
    def __init__(self, all_tags: AllTags):
        super().__init__()
        self.src = 0
        self.api = "https://ln.topdf.de/HellowNekoNew/api/"

        self.all_tags = all_tags

    def get_result_from_endpoint(self, endpoint: str, quarry: str):
        url = urljoin(self.api, endpoint)
        print(f"Getting {url}")

        # get data from endpoint
        r = self.get_request(url)
        if r is None:
            return None
        data = r.json()

        image = self.get_image_from_url(data["url"])
        if image is None:
            return None

        result = Result(self.src, quarry)
        result.set_image(image)
        result.set_id(data["id"])
        result.set_url(data["url"])
        result.set_sfw(bool(data["sfw"]))
        result.set_translation(data["translation"])
        result.set_tags(data["tags"])

        return result

    def get_from_(self, quarry: str):
        if quarry.isdigit():
            return f"?image_id={quarry}"
        else:
            tag_id = self.all_tags.get_id_by_name(quarry)
            if tag_id is None:
                print(f"Could currently not find tag {quarry}")
                return f"?tag_name={quarry}"
            else:
                return f"?tag_id={tag_id}"

    def get_endpoint_part(self, options: files.Options):
        sfw_str = "&sfw=1" if options.sfw else ""
        return f"image.php/{self.get_from_(options.quarry)}{sfw_str}"

    def next(self, current_opt: files.Options, prev_res: Result):
        rand_str = "" if current_opt.random else f"&prev={prev_res.id_}"
        return self.get_result_from_endpoint(f"{self.get_endpoint_part(current_opt)}{rand_str}", quarry=current_opt.quarry)

    def previous(self, next_res: Result):
        rand_str = f"&next={next_res.id_}"
        endpoint = f"image.php/{self.get_from_(next_res.quarry)}{rand_str}"
        return self.get_result_from_endpoint(endpoint, quarry=next_res.quarry)

class NHentai(GetData):
    def __init__(self, all_tags: AllTags):
        super().__init__()
        self.src = 1
        self.all_tags = all_tags

        self.api = "https://nhentai.net/api/"

        self.current_media_id = None
        self.current_page = 0
        self.current_data = None

    @staticmethod
    def extension(t):
        extensions = {
            "j": ".jpg",
            "p": ".png",
            "g": ".gif"
        }
        return extensions[t]

    def get_current_page_data(self):
        return self.current_data['images']['pages'][self.current_page]

    def get_page_url(self):
        return f"https://i.nhentai.net/galleries/{self.current_media_id}/{self.current_page}{NHentai.extension(self.get_current_page_data()['t'])}"

    def next(self, current_opt: files.Options, prev_opt: files.Options):
        if current_opt.quarry.isdigit():
            endpoint = f"gallery/{current_opt.quarry}"

            r = self.get_request(urljoin(self.api, endpoint))
            print(f"Getting {urljoin(self.api, endpoint)}")
            data = r.json()

            if data['media_id'] != self.current_media_id:
                self.current_media_id = data['media_id']
                self.current_page = 0
                self.current_data = data

            self.current_page += 1

            img_url = self.get_page_url()
            img = self.get_image_from_url(img_url)
            result = Result(1, current_opt.quarry)
            result.set_image(img)

            result.set_id(int(current_opt.quarry))
            result.set_url(img_url)
            result.set_sfw(bool(False))
            result.set_tags([tag["name"] for tag in self.current_data["tags"] if tag["type"] == "tag"])

            return result


    def previous(self, next_opt: files.Options):
        self.current_page -= 1

        img_url = self.get_page_url()
        img = self.get_image_from_url(img_url)
        result = Result(1, next_opt.quarry)
        result.set_image(img)

        result.set_id(int(next_opt.quarry))
        result.set_url(img_url)
        result.set_sfw(bool(False))
        result.set_tags([tag["name"] for tag in self.current_data["tags"] if tag["type"] == "tag"])

        return result

class Downloader(threading.Thread):
    def __init__(self, new_request_queue: queue.Queue, work_queue: queue.Queue, prev_work_queue: queue.Queue,
                 result_queue: queue.Queue, prev_result_queue: queue.Queue, all_tags: AllTags):
        super().__init__()
        self.hellow_neko = HellowNeko(all_tags)
        self.nhentai = NHentai(all_tags)

        self.source_map = {
            0: self.hellow_neko,
            1: self.nhentai
        }

        self.new_request_queue = new_request_queue
        self.work_queue = work_queue
        self.prev_work_queue = prev_work_queue
        self.result_queue = result_queue
        self.prev_result_queue = prev_result_queue

        self.last_working_options = None
        self.last_working_endpoint = None

        self.prev_neko_id = 1592

        self.all_tags = all_tags

    def get_from_src(self, options: files.Options, prev=False):
        if prev:
            return self.source_map[options.source].previous(options), ""
        else:
            return self.source_map[options.source].next(options, options), ""



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
                    self.result_queue.put(self.last_working_options.quarry)

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



class Tag:
    def __init__(self, name: str, id_: int = 0, frequency: int = 0):
        self.name = name
        self.id = id_
        self.frequency = frequency

    def __str__(self):
        return f"{self.name} ({self.frequency})"

class DownloaderAllTags(threading.Thread):
    def __init__(self, sources: list, result_queue: queue.Queue):
        super().__init__()
        self.session = get_request_session()

        self.sources = sources
        self.result_queue = result_queue

    def download_hellow_neko_tags(self):
        url = "https://ln.topdf.de/HellowNekoNew/api/all_tag.php"

        try:
            r = self.session.get(url)
            if r.status_code != 200:
                return None
        except requests.exceptions.RequestException:
            return None

        return [Tag(tag["name"], id_=tag["id"], frequency=tag["frequency"]) for tag in r.json()]

    def download_neko_life_tags(self):
        url = "https://nekos.life/api/v2/endpoints"

        try:
            r = self.session.get(url)
            if r.status_code != 200:
                return None
        except requests.exceptions.RequestException:
            return None

        for endpoint in r.json():
            if not "/api/v2/img/" in endpoint:
                continue
            tag_list = endpoint.split("/api/v2/img/")[1].replace("<", "[").replace(">", "]").replace("'", "\"")
            return [Tag(tag) for tag in tag_list]


    def download_tags(self, src: int):
        if src == 0:
            return src, self.download_hellow_neko_tags()

        return src, None


    def run(self):
        for src in self.sources:
            self.result_queue.put(self.download_tags(src))

class Api:
    def __init__(self, config: files.Config):
        self.config = config

        self.history = []
        self.index = -1

        self.all_tags = AllTags(self.config.current_source)
        self.all_tags_result_queue = queue.Queue()
        self.downloader_all_tags = DownloaderAllTags([src["id"] for src in self.config.sources], self.all_tags.result_queue)
        self.downloader_all_tags.start()

        self.new_request_queue = queue.Queue()
        self.work_queue = queue.Queue()
        self.prev_work_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.prev_result_queue = queue.Queue()
        self.downloader_thread = Downloader(self.new_request_queue, self.work_queue, self.prev_work_queue, self.result_queue,
                                            self.prev_result_queue, all_tags=self.all_tags)
        self.downloader_thread.start()

        self.gui = None

        self.requested_next = False
        self.requested_prev = False
        self.from_index = False
        self.request_next()

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

    def get_autocomplete_tags(self):
        return self.all_tags.get_autocomplete_tags()

    def terminate(self):
        self.work_queue.queue.clear()
        self.work_queue.put("terminate")

    autocomplete_tags = property(fget=get_autocomplete_tags)
