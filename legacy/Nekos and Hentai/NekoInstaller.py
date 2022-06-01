import urllib.request
import os
from os import path
import tkinter
from tkinter import *
from tkinter import filedialog

install_directory = 'Downloads'

external_files_directory = '%APPDATA%\\Neko'
external_files_directory = path.expandvars(external_files_directory)
print(external_files_directory)

install_directory = os.getcwd()

url_external_files = 'https://ln.topdf.de/Neko%20URL%20cute', 'https://ln.topdf.de/Neko%20URL%20lewd', 'https://ln.topdf.de/version', 'https://ln.topdf.de/NekoInstaller.exe'
url_config = 'https://ln.topdf.de/config.txt', 'https://ln.topdf.de/config_presets.txt'
names_external_files = 'Neko URL cute', 'Neko URL lewd', 'version', 'NekoInstaller.exe'
program_url = 'https://ln.topdf.de/Neko.exe'

config_start = urllib.request.urlopen(url_config[0])
lines_start = []
lines_preset = []
for line in config_start:
    decoded_line = line.decode("utf-8")
    lines_start.append(decoded_line)

try:
    current_file = open(external_files_directory+'\\config.txt', 'r')

    for line in lines_start:
        current_line = current_file.readline()
        print(current_line)
        current_line = current_line[len(line)-1:len(current_line)]
        lines_preset.append(current_line)
    
    current_file.close()

except:
    config_preset = urllib.request.urlopen(url_config[1])
    print('dats not good')

    for line in config_preset:
        decoded_line = line.decode("utf-8")
        lines_preset.append(decoded_line)

for i in range(len(lines_start)):
    lines_start[i] = lines_start[i].replace('\n', '') + lines_preset[i]




config = ''
for line in lines_start:
    config += line
print(config)






try:
    os.mkdir(external_files_directory)
except OSError:
    print('Folder already exists')




def browseFiles():
    global install_directory
    install_directory = filedialog.askdirectory(initialdir = "/", title = "Select a directory")
    label_file_explorer.config(text = install_directory)

def Install():
    global install_directory
    global config

    print('write config')
    with open(external_files_directory+'\\config.txt', 'w') as config_file:
        config_file.write(config)

    print('write database')
    for i in range(len(url_external_files)):
        urllib.request.urlretrieve(url_external_files[i], external_files_directory + '\\' + names_external_files[i])
        print(url_external_files[i])
        print(external_files_directory + names_external_files[i])
    print('write executable')
    urllib.request.urlretrieve(program_url, install_directory + '\\Neko.exe')
    tk.destroy()




tk = Tk()  

tk.title('Neko Installer')
tk.geometry("500x80")

install_button = Button(tk, text = 'Install', command = Install)
install_button.place(x=0,y=0)
  
button_explore = Button(tk, text = ":3", command = browseFiles)
button_explore.place(x=0,y=30)
  
label_file_explorer = Label(tk, text = install_directory)
label_file_explorer.place(x=30,y=32)
  
tk.mainloop()
