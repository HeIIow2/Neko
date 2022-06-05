import files
import gui

config = files.Config()

gui = gui.Gui(config)

if __name__ == '__main__':
    gui.root.mainloop()
