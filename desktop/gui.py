import tkinter as tk

import files

class SidePanel:
    def __init__(self, master, config: files.Config):
        self.master = master
        self.config = config

        self.prev_button = tk.Button(self.master, text="Previous", command=self.previous)
        self.prev_button.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.next_button = tk.Button(self.master, text="Next", command=self.next)
        self.next_button.grid(row=0, column=2, columnspan=2, sticky="nsew")

        self.browse_neko_button = tk.Button(self.master, text="Neko", command=self.browse_neko)
        self.browse_neko_button.grid(row=1, column=0, sticky="nsew")
        self.neko_query = tk.Entry(self.master)
        self.neko_query.grid(row=1, column=1, columnspan=3, sticky="nsew")

        self.browse_hentai_button = tk.Button(self.master, text="Hentai", command=self.browse_hentai)
        self.browse_hentai_button.grid(row=2, column=0, sticky="nsew")
        self.hentai_query = tk.Entry(self.master)
        self.hentai_query.grid(row=2, column=1, columnspan=3, sticky="nsew")

        self.like_var = tk.IntVar()
        self.like_checkbox = tk.Checkbutton(self.master, variable=self.like_var, command=self.toggle_like, text="Like")
        self.like_checkbox.grid(row=3, column=0, columnspan=4, sticky="nsw")

        self.sfw_var = tk.IntVar()
        self.sfw_var.set(config.sfw_filter)
        self.sfw_checkbox = tk.Checkbutton(self.master, variable=self.sfw_var, command=self.toggle_sfw, text="Only SFW")
        self.sfw_checkbox.grid(row=4, column=0, columnspan=4, sticky="nsw")

    def next(self):
        print("Next")

    def previous(self):
        print("Previous")

    def browse_neko(self):
        print("Browse Neko")

    def browse_hentai(self):
        print("Browse Hentai")

    def toggle_like(self):
        print("Toggle like")

    def toggle_sfw(self):
        self.config.sfw_filter = self.sfw_var.get()

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
        self.side_panel_frame.grid(row=0, column=0, sticky="nsew")
        self.side_panel = SidePanel(self.side_panel_frame, self.config)

    def on_closing(self):
        self.master.destroy()

    def get_root(self):
        return self.master

    root = property(get_root)
