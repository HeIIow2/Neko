import tkinter as tk

import files

config = files.Config()

if __name__ == '__main__':
    root = tk.Tk()
    root.title(config.window_title)
    root.geometry(config.window_geometry)
    root.state(config.window_state)

    root.mainloop()
