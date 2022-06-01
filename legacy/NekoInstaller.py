import urllib.request
import os
from os import path
import tkinter
from tkinter import *
from tkinter import filedialog

install_directory = 'Downloads'

external_files_directory = '%APPDATA%\\Neko\\'
external_files_directory = path.expandvars(external_files_directory)
print(external_files_directory)

install_directory = os.getcwd()

# url_config = 'https://ln.topdf.de/config.txt', 'https://ln.topdf.de/config_presets.txt'
url = 'https://ln.topdf.de/files/'
name_names = 'all_files'
names_external_files = []
# program_url = 'https://ln.topdf.de/Neko.exe'

# config_start = urllib.request.urlopen(url_config[0])
# lines_start = []
# lines_preset = []
# for line in config_start:
#     decoded_line = line.decode("utf-8")
#     lines_start.append(decoded_line)
'''
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
'''

with urllib.request.urlopen(url + name_names) as table:
    for row in table:
        names_external_files.append(row.decode('utf-8').rstrip('\n'))

print(names_external_files)

try:
    os.mkdir(external_files_directory)
except OSError:
    print('Folder already exists')


def browseFiles():
    global install_directory
    install_directory = filedialog.askdirectory(initialdir="/", title="Select a directory")
    label_file_explorer.config(text=install_directory)


def Install():
    global install_directory
    print(names_external_files)
    print(names_external_files)
    # global config

    # print('write config')
    # with open(external_files_directory + '\\config.txt', 'w') as config_file:
    #     config_file.write(config)

    print('download stuff please hold on')
    print(url + names_external_files[0], install_directory + '/' + names_external_files[0])
    urllib.request.urlretrieve(url + names_external_files[0], install_directory + '/' + names_external_files[0])
    for i in range(len(names_external_files) - 1):
        urllib.request.urlretrieve(url + names_external_files[i+1],
                                   external_files_directory + '\\' + names_external_files[i + 1])
        print(url + names_external_files[i + 1])
        print(external_files_directory + names_external_files[i + 1])

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
