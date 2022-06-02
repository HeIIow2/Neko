import files

import tkinter as tk

config = files.Config()

if __name__ == '__main__':
    root = tk.Tk()
    root.title(config.app_title)
    root.geometry(config.window_geometry)
    root.state(config.window_state)
    root.mainloop()
