import files
import gui
import retrieve

from tkinter import messagebox

if __name__ == '__main__':
    config = files.Config()
    if config.show_messagebox:
        messagebox.showinfo("Loading could take a couple seconds...",
                            "Loading could take a couple seconds...\n And None of the following pictures belong to me.")
        config.show_messagebox = False
    api = retrieve.Api(config)
    gui = gui.Gui(config, api)

    while gui.update() != -1:
        pass
    config.save_config()
    api.terminate()
