import tkinter as tk

import files

class SidePanel:
    def __init__(self, root_ref, master, config: files.Config):
        self.root_ref = root_ref
        self.master = master
        self.config = config

        self.prev_button = tk.Button(self.master, text="Previous", command=self.previous)
        self.prev_button.grid(row=0, column=0, columnspan=2, sticky="nsew")
        for keybinding in config.get_button_keybindings("prev"):
            self.root_ref.bind(keybinding, self.previous)

        self.next_button = tk.Button(self.master, text="Next", command=self.next)
        self.next_button.grid(row=0, column=2, columnspan=2, sticky="nsew")
        for keybinding in config.get_button_keybindings("next"):
            self.root_ref.bind(keybinding, self.next)

        self.browse_neko_button = tk.Button(self.master, text="Neko", command=self.browse_neko)
        self.browse_neko_button.grid(row=1, column=0, sticky="nsew")
        self.neko_query_var = tk.StringVar()
        self.neko_query_var.set(self.config.neko_quarry)
        self.neko_query = tk.Entry(self.master, textvariable=self.neko_query_var)
        self.neko_query.grid(row=1, column=1, columnspan=3, sticky="nsew")

        self.browse_hentai_button = tk.Button(self.master, text="Hentai", command=self.browse_hentai)
        self.browse_hentai_button.grid(row=2, column=0, sticky="nsew")
        self.hentai_query_var = tk.StringVar()
        self.hentai_query_var.set(self.config.hentai_quarry)
        self.hentai_query = tk.Entry(self.master, textvariable=self.hentai_query_var)
        self.hentai_query.grid(row=2, column=1, columnspan=3, sticky="nsew")

        self.random_var = tk.IntVar()
        self.random_var.set(config.random_image)
        self.random_checkbox = tk.Checkbutton(self.master, variable=self.random_var, command=self.toggle_random, text="shuffle Images")
        self.random_checkbox.grid(row=3, column=0, columnspan=4, sticky="nsw")
        for keybinding in config.get_button_keybindings("random"):
            self.root_ref.bind(keybinding, self.toggle_random)

        self.sfw_var = tk.IntVar()
        self.sfw_var.set(config.sfw_filter)
        self.sfw_checkbox = tk.Checkbutton(self.master, variable=self.sfw_var, command=self.toggle_sfw, text="Only SFW")
        self.sfw_checkbox.grid(row=4, column=0, columnspan=4, sticky="nsw")
        for keybinding in config.get_button_keybindings("sfw"):
            self.root_ref.bind(keybinding, self.toggle_sfw)

        self.like_var = tk.IntVar()
        self.like_checkbox = tk.Checkbutton(self.master, variable=self.like_var, command=self.toggle_like, text="Like")
        self.like_checkbox.grid(row=5, column=0, columnspan=4, sticky="nsw")

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

    def next(self, event=None):
        print("Next")

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

    def toggle_like(self, event=None):
        print("Toggle like")

class Gui:
    def __init__(self, config: files.Config):
        self.config = config

        self.master = tk.Tk()
        self.master.title(config.window_title)
        self.master.geometry(config.window_geometry)
        self.master.state(config.window_state)

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.width, self.height = self.master.winfo_screenwidth(), self.master.winfo_screenheight()

        self.side_panel_frame = tk.Frame(self.master)
        self.side_panel_frame.grid(row=0, column=1, sticky="nse")
        self.side_panel = SidePanel(self.master, self.side_panel_frame, self.config)

    def on_closing(self):
        self.master.destroy()

    def get_root(self):
        return self.master

    root = property(get_root)
