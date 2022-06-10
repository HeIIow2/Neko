import files
import gui
import retrieve

if __name__ == '__main__':
    config = files.Config()
    api = retrieve.Api(config)
    gui = gui.Gui(config, api)

    while gui.update() != -1:
        pass
    config.save_config()
    api.terminate()
