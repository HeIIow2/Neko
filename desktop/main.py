import files
import gui
import retrieve

config = files.Config()
api = retrieve.Api(config)
gui = gui.Gui(config, api)


if __name__ == '__main__':
    gui.root.mainloop()
    config.save_config()
    api.terminate()
