import tkinter as tk
import webbrowser

import PIL.Image, PIL.ImageTk
import _tkinter
from PIL import ImageFilter, ImageTk

import files
import retrieve as api_module


class SidePanel:
    def __init__(self, other, master, config: files.Config, api: api_module.Api):
        self.other = other
        self.root_ref = other.master
        self.master = master
        self.config = config
        self.api = api

        self.prev_button = tk.Button(self.master, text="Previous", command=self.previous)
        self.prev_button.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=(self.config.padding, 0), pady=self.config.padding)
        for keybinding in config.get_button_keybindings("prev"):
            self.root_ref.bind(keybinding, self.previous)

        self.next_button = tk.Button(self.master, text="Next", command=self.next)
        self.next_button.grid(row=0, column=2, columnspan=2, sticky="nsew", padx=self.config.padding, pady=self.config.padding)
        for keybinding in config.get_button_keybindings("next"):
            self.root_ref.bind(keybinding, self.next)

        self.browse_neko_button = tk.Button(self.master, text="Neko", command=self.browse_neko)
        self.browse_neko_button.grid(row=1, column=0, sticky="nsew", padx=(self.config.padding, 0), pady=(0, self.config.padding))
        self.neko_query_var = tk.StringVar()
        self.neko_query_var.set(self.config.neko_quarry)
        self.neko_query = tk.Entry(self.master, textvariable=self.neko_query_var)
        self.neko_query.bind("<Return>", self.browse_neko)
        self.neko_query.bind("<KP_Enter>", self.browse_neko)
        self.neko_query.grid(row=1, column=1, columnspan=3, sticky="nsew", padx=self.config.padding, pady=(0, self.config.padding))

        # self.browse_hentai_button = tk.Button(self.master, text="Hentai", command=self.browse_hentai)
        # self.browse_hentai_button.grid(row=2, column=0, sticky="nsew", padx=(self.config.padding, 0), pady=(0, self.config.padding))
        # self.hentai_query_var = tk.StringVar()
        # self.hentai_query_var.set(self.config.hentai_quarry)
        # self.hentai_query = tk.Entry(self.master, textvariable=self.hentai_query_var)
        # self.hentai_query.bind("<Return>", self.browse_hentai)
        # self.hentai_query.bind("<KP_Enter>", self.browse_hentai)
        # self.hentai_query.grid(row=2, column=1, columnspan=3, sticky="nsew", padx=self.config.padding, pady=(0, self.config.padding))

        self.random_var = tk.IntVar()
        self.random_var.set(config.random_image)
        self.random_checkbox = tk.Checkbutton(self.master, variable=self.random_var, command=self.toggle_random, text="shuffle Images")
        self.random_checkbox.grid(row=3, column=0, columnspan=4, sticky="nsw", padx=self.config.padding, pady=(0, self.config.padding))
        for keybinding in config.get_button_keybindings("random"):
            self.root_ref.bind(keybinding, self.toggle_random)

        self.sfw_var = tk.IntVar()
        self.sfw_var.set(config.sfw_filter)
        self.sfw_checkbox = tk.Checkbutton(self.master, variable=self.sfw_var, command=self.toggle_sfw, text="Only SFW")
        self.sfw_checkbox.grid(row=4, column=0, columnspan=4, sticky="nsw", padx=self.config.padding, pady=(0, self.config.padding))
        for keybinding in config.get_button_keybindings("sfw"):
            self.root_ref.bind(keybinding, self.toggle_sfw)

        # self.like_var = tk.IntVar()
        # self.like_checkbox = tk.Checkbutton(self.master, variable=self.like_var, command=self.toggle_like, text="Like")
        # self.like_checkbox.grid(row=5, column=0, columnspan=4, sticky="nsw", padx=self.config.padding, pady=(0, self.config.padding))

        self.button_map = {
            "next": self.next_button,
            "prev": self.prev_button,
            "neko": self.browse_neko_button,
            # "hentai": self.browse_hentai_button,
            "random": self.random_checkbox,
            "sfw": self.sfw_checkbox,
            # "like": self.like_checkbox
        }

        self.update_buttons()

        self.master.rowconfigure(6, weight=1)
        self.current_image_label = tk.Label(self.master, text="Current Image:\n", justify="left")
        self.current_image_label.grid(row=6, column=0, columnspan=4, sticky="w", padx=self.config.padding, pady=(0, self.config.padding))

        self.master.rowconfigure(7, weight=1)
        self.all_tag_label = tk.Label(self.master, text=f"all tags:\n{api.all_tags}", justify="left")
        self.all_tag_label.grid(row=7, column=0, columnspan=4, sticky="sw", padx=self.config.padding, pady=(0, self.config.padding))

    def text_entry_is_focused(self):
        return "!entry" in str(self.neko_query.focus_get())

    def next(self, event=None):
        if event is not None and self.text_entry_is_focused():
            return
        print("Next")
        self.other.request_next()

    def previous(self, event=None):
        if event is not None and self.text_entry_is_focused():
            return
        print("Previous")
        self.other.previous()

    def update_buttons(self):
        for key, button in self.button_map.items():
            for property, value in self.config.get_button_properties(key).items():
                button.config(**{property: value})

    def browse_neko(self, event=None):
        self.config.neko_focus = True
        prev_query = self.config.neko_quarry
        self.config.neko_quarry = self.neko_query_var.get()
        if self.api.get_option() is None:
            self.config.neko_quarry = prev_query
            self.neko_query_var.set(prev_query)
            return
        # unfocus entry
        self.master.focus_set()
        self.update_buttons()
        self.other.request_next()
        print("Browse Neko")

    def browse_hentai(self, event=None):
        self.config.hentai_focus = True
        self.master.focus_set()
        self.config.hentai_quarry = self.hentai_query_var.get()
        self.update_buttons()
        print("Browse Hentai")

    def toggle_random(self, event=None):
        if event is not None and self.text_entry_is_focused():
            return
        if event is not None:
            self.random_var.set(not self.random_var.get())
        self.config.random_image = self.random_var.get()

    def toggle_sfw(self, event=None):
        if event is not None and self.text_entry_is_focused():
            return
        if event is not None:
            self.sfw_var.set(not self.sfw_var.get())
        self.config.sfw_filter = self.sfw_var.get()

    def update(self, data: api_module.Result):
        self.current_image_label.config(text=f"Current Tag:\n{data.description}")

        # update the colors
        self.master.config(bg=data.base_color)
        self.current_image_label.config(bg=data.base_color, fg=data.text_base_color)
        self.all_tag_label.config(bg=data.base_color, fg=data.text_base_color)
        self.random_checkbox.config(bg=data.base_color, fg=data.text_base_color, activebackground=data.base_color, activeforeground=data.text_base_color)
        self.sfw_checkbox.config(bg=data.base_color, fg=data.text_base_color, activebackground=data.base_color, activeforeground=data.text_base_color)
        # self.like_checkbox.config(bg=data.base_color, fg=data.text_base_color, activebackground=data.base_color, activeforeground=data.text_base_color)

        self.neko_query.config(bg=data.elem_color, fg=data.text_elem_color)
        # self.hentai_query.config(bg=data.elem_color, fg=data.text_elem_color)
        self.next_button.config(bg=data.elem_color, fg=data.text_elem_color)
        self.prev_button.config(bg=data.elem_color, fg=data.text_elem_color)
        self.browse_neko_button.config(bg=data.elem_color, fg=data.text_elem_color)
        # self.browse_hentai_button.config(bg=data.elem_color, fg=data.text_elem_color)

    def toggle_like(self, event=None):
        print("Toggle like")

class Gui:
    def __init__(self, config: files.Config, api: api_module.Api):
        self.config = config
        self.api = api
        self.api.set_gui(self)

        self.open_window = True
        self.loaded = False
        self.current_img = None
        self.current_url = None

        self.master = tk.Tk()
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.master.title(config.window_title)
        self.master.geometry(config.window_geometry)
        self.master.state(config.window_state)

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.main_frame = tk.Frame(self.master)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.width, self.height = self.main_frame.winfo_screenwidth(), self.main_frame.winfo_screenheight()
        self.main_frame.bind("<Configure>", self.on_resize)

        self.current_img_tk = None
        self.image_label = tk.Label(self.main_frame, borderwidth=0, highlightthickness=0)
        self.image_label.grid(row=0, column=0, sticky="nsew")
        self.image_label.bind("<Double-Button-1>", self.open_url)

        self.side_panel_frame = tk.Frame(self.master)
        self.side_panel_frame.grid(row=0, column=1, sticky="nse")
        self.side_panel = SidePanel(self, self.side_panel_frame, self.config, self.api)

        self.request_next()

    def resize_img(self, img: PIL.Image, width, height, mode):
        img_width, img_height = img.size
        size = (width, height)

        if mode:
            if img_width / size[0] > img_height / size[1]:
                count = img_width / size[0]
                img_height = img_height / count
                img_width = size[0]
            else:
                count = img_height / size[1]
                img_width = img_width / count
                img_height = size[1]
        else:
            if img_width / size[0] < img_height / size[1]:
                count = img_width / size[0]
                img_height = img_height / count
                img_width = size[0]
            else:
                count = img_height / size[1]
                img_width = img_width / count
                img_height = size[1]

        img_size = round(img_width), round(img_height)
        img_rz = img.resize(img_size)
        return img_rz

    def fit_img(self, img: PIL.Image) -> PIL.ImageTk.PhotoImage:
        img_fg = self.resize_img(img, self.width, self.height, True)
        img_bg = self.resize_img(img, self.width, self.height, False)
        img_bg = img_bg.filter(ImageFilter.BoxBlur(30))

        pos_bg = (img_bg.size[0] - self.width) / 2, (img_bg.size[1] - self.height) / 2
        img_canvas = img_bg.crop((pos_bg[0], pos_bg[1], pos_bg[0] + self.width, pos_bg[1] + self.height))
        img_width, img_height = img_fg.size
        img_canvas.paste(img_fg, (int((self.width - img_width) / 2), int((self.height - img_height) / 2)))

        return ImageTk.PhotoImage(img_canvas)

    def update_content(self, data: api_module.Result):
        self.side_panel.update(data)
        self.current_img = data.image
        self.current_img_tk = self.fit_img(self.current_img)
        self.image_label.config(image=self.current_img_tk)
        self.current_url = data.url

    def request_next(self):
        self.api.request()
        print("Next")

    def previous(self):
        print("Previous")
        result = self.api.get_previous()
        if result is not None:
            self.update_content(result)
        else:
            print("No previous images saved")

    def open_url(self, event):
        print(f"Open URL {self.current_url}")
        if self.current_url is not None:
            webbrowser.open(self.current_url)

    def on_closing(self):
        self.master.destroy()
        self.open_window = False

    def on_resize(self, event):
        print("Resize")
        self.width, self.height = event.width, event.height
        if self.current_img is None:
            return
        self.current_img_tk = self.fit_img(self.current_img)
        self.image_label.config(image=self.current_img_tk)


    def update(self):
        if not self.open_window:
            return -1

        try:
            request = self.api.get_request()
            if request is not None:
                self.update_content(request)
                self.loaded = True

            if self.loaded:
                self.master.update()

        except _tkinter.TclError:
            return -1
