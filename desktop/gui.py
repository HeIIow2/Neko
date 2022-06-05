import tkinter as tk

import files
import retrieve as api_module

class SidePanel:
    def __init__(self, other, master, config: files.Config, api: api_module.Api):
        self.other = other
        self.root_ref = other.master
        self.master = master
        self.config = config

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
        self.neko_query.grid(row=1, column=1, columnspan=3, sticky="nsew", padx=self.config.padding, pady=(0, self.config.padding))

        self.browse_hentai_button = tk.Button(self.master, text="Hentai", command=self.browse_hentai)
        self.browse_hentai_button.grid(row=2, column=0, sticky="nsew", padx=(self.config.padding, 0), pady=(0, self.config.padding))
        self.hentai_query_var = tk.StringVar()
        self.hentai_query_var.set(self.config.hentai_quarry)
        self.hentai_query = tk.Entry(self.master, textvariable=self.hentai_query_var)
        self.hentai_query.grid(row=2, column=1, columnspan=3, sticky="nsew", padx=self.config.padding, pady=(0, self.config.padding))

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

        self.like_var = tk.IntVar()
        self.like_checkbox = tk.Checkbutton(self.master, variable=self.like_var, command=self.toggle_like, text="Like")
        self.like_checkbox.grid(row=5, column=0, columnspan=4, sticky="nsw", padx=self.config.padding, pady=(0, self.config.padding))

        self.button_map = {
            "next": self.next_button,
            "prev": self.prev_button,
            "neko": self.browse_neko_button,
            "hentai": self.browse_hentai_button,
            "random": self.random_checkbox,
            "sfw": self.sfw_checkbox,
            "like": self.like_checkbox
        }

        self.update_buttons()

        self.master.rowconfigure(6, weight=1)
        self.current_image_label = tk.Label(self.master, text="Current Image:\n", justify="left", bg="#666")
        self.current_image_label.grid(row=6, column=0, columnspan=4, sticky="w", padx=self.config.padding, pady=(0, self.config.padding))

        self.master.rowconfigure(7, weight=1)
        self.all_tag_label = tk.Label(self.master, text=f"all tags:\n{api.all_tags}", justify="left", bg="#666")
        self.all_tag_label.grid(row=7, column=0, columnspan=4, sticky="sw", padx=self.config.padding, pady=(0, self.config.padding))

    def next(self, event=None):
        print("Next")
        self.other.next()

    def previous(self, event=None):
        print("Previous")

    def update_buttons(self):
        for key, button in self.button_map.items():
            for property, value in self.config.get_button_properties(key).items():
                button.config(**{property: value})

    def browse_neko(self, event=None):
        self.config.neko_focus = True
        self.config.neko_quarry = self.neko_query_var.get()
        self.update_buttons()
        print("Browse Neko")

    def browse_hentai(self, event=None):
        self.config.hentai_focus = True
        self.config.hentai_quarry = self.hentai_query_var.get()
        self.update_buttons()
        print("Browse Hentai")

    def toggle_random(self, event=None):
        if event is not None:
            self.random_var.set(not self.random_var.get())
        self.config.random_image = self.random_var.get()

    def toggle_sfw(self, event=None):
        if event is not None:
            self.sfw_var.set(not self.sfw_var.get())
        self.config.sfw_filter = self.sfw_var.get()

    def update_description(self, data: api_module.Result):
        self.current_image_label.config(text=f"Current Tag:\n{data.description}")

    def toggle_like(self, event=None):
        print("Toggle like")

class Gui:
    def __init__(self, config: files.Config, api: api_module.Api):
        self.config = config
        self.api = api
        self.api.set_gui(self)

        self.master = tk.Tk()
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.master.title(config.window_title)
        self.master.geometry(config.window_geometry)
        self.master.state(config.window_state)

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.width, self.height = self.master.winfo_screenwidth(), self.master.winfo_screenheight()

        self.main_frame = tk.Frame(self.master, bg="#555")
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.current_img = None
        self.image_label = tk.Label(self.main_frame)
        self.image_label.grid(row=0, column=0, sticky="nsew")

        self.side_panel_frame = tk.Frame(self.master, bg="#444")
        self.side_panel_frame.grid(row=0, column=1, sticky="nse")
        self.side_panel = SidePanel(self, self.side_panel_frame, self.config, self.api)

        self.next()

    def update_content(self, data: api_module.Result):
        self.current_img = data.image_tk
        self.image_label.config(image=self.current_img)
        self.side_panel.update_description(data)

    def next(self, no_update=False):
        data = self.api.next()
        self.update_content(data)
        print("Next")

    def previous(self):
        print("Previous")

    def window_update(self):
        self.master.update()

    def on_closing(self):
        self.master.destroy()

    def get_root(self):
        return self.master

    root = property(get_root)
