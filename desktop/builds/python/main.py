import files
import gui
import retrieve
from plyer import notification


if __name__ == '__main__':
    notification.notify(
        title='Hellow Neko',
        message='Loading could take a couple of seconds...',
        app_icon=None,  # e.g. 'C:\\icon_32x32.ico'
        timeout=3,  # seconds
    )

    config = files.Config()
    api = retrieve.Api(config)
    gui = gui.Gui(config, api)

    while gui.update() != -1:
        pass
    config.save_config()
    api.terminate()
