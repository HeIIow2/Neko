import urllib.request
import os
from os import path
import tkinter
from tkinter import *
from tkinter import filedialog

install_directory = 'Downloads'

files_directory = '%APPDATA%\\Neko\\'
files_directory = os.path.expandvars(files_directory)
print(files_directory)


install_directory = os.getcwd()

try:
    os.mkdir(files_directory)
    install_directory = os.getcwd()
except OSError:
    print('Folder already exists')
    try:
        with open(files_directory+'path', 'r') as path_file:
            install_directory = path_file.readline()
            exit()
    except:
        install_directory = os.getcwd()
print(install_directory)


url = 'https://ln.topdf.de/files/'
name_names = 'all_files'
names_external_files = []

with urllib.request.urlopen(url + name_names) as table:
    for row in table:
        names_external_files.append(row.decode('utf-8').rstrip('\n'))

print(names_external_files)

def browseFiles():
    global install_directory
    install_directory = filedialog.askdirectory(initialdir="/", title="Select a directory")
    label_file_explorer.config(text=install_directory)


def Install():
    global install_directory
    install_directory += '/Neko'
    try:
        os.mkdir(install_directory)
    except OSError:
        print('Folder already exists')

    print('download stuff please hold on')
    urllib.request.urlretrieve(url + 'NekoUpdater.exe', install_directory + '/' + 'NekoUpdater.exe')
    print(url + 'NekoUpdater.exe', install_directory + '/' + 'NekoUpdater.exe')
    urllib.request.urlretrieve(url + names_external_files[0], install_directory + '/' + names_external_files[0])
    print(url + names_external_files[0], install_directory + '/' + names_external_files[0])
    try:
        with open(install_directory+'/'+names_external_files[1]):
            pass
    except:
        urllib.request.urlretrieve(url + names_external_files[1], install_directory + '/' + names_external_files[1])

    for i in range(len(names_external_files) - 2):
        urllib.request.urlretrieve(url + names_external_files[i+2], install_directory + '/' + names_external_files[i+2])
        print(url + names_external_files[i+2], install_directory + '/' + names_external_files[i+2])

    with open(files_directory + 'path', 'w') as path_file:
        path_file.write(install_directory.rstrip('/Neko'))

    tk.destroy()


tk = Tk()

tk.title('Neko Installer')
tk.geometry("500x80")

install_button = Button(tk, text='Install', command=Install)
install_button.place(x=0, y=0)

button_explore = Button(tk, text=":3", command=browseFiles)
button_explore.place(x=0, y=30)

label_file_explorer = Label(tk, text=install_directory)
label_file_explorer.place(x=30, y=32)

tk.mainloop()
