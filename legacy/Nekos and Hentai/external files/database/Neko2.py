import ctypes
import os
import random
import threading
import time
import tkinter
import urllib
from tkinter import messagebox

import pyautogui
import requests
import win32api
import win32com
import win32con
import win32gui
from PIL import ImageTk, Image, ImageFilter

url_img = 'https://ln.topdf.de/img/images/'
url_table = 'https://ln.topdf.de/img/table'
url_versions = 'https://ln.topdf.de/files/version'
# external_files = '%APPDATA%\\Neko\\'

img = Image.new('RGB', (1, 1))
start_filter = 'all and not lewd'
background_name = 'background.png'
version_name = 'version'
loading_screen = 'loading_screen.jpg'

# with open(os.path.expandvars(external_files + version_name), 'r') as version_file:
with open(version_name, 'r') as version_file:
    version = version_file.readline()
    version_web_file = urllib.request.urlopen(url_versions)
    for line in version_web_file:
        version_web = line.decode('utf-8')

    if version_web != version:
        print('new Version available')
        urllib.request.urlretrieve('https://ln.topdf.de/files/NekoUpdater.exe', 'NekoUpdater.exe')
        os.startfile(os.path.expandvars('NekoUpdater.exe'))
        exit()
    else:
        print('no new Version available')

# create window
screen_size = pyautogui.size()
window_size = screen_size

root = tkinter.Tk()
root.title('NEKOS!!!')
# root.geometry(str(screen_size[0]) + "x" + str(screen_size[1]) + "+" + str(-(265 + screen_size[1])) + "+0")
root.state('zoomed')

label = tkinter.Label(master=root)
# label.place(x=0, y=0)

'''
TO DO
classe you say new neko and you get the finished image
face recognition
easter egg
Desktop
installer or updater
Logik hinzufügen
'''




class ReadDatabase:
    def __init__(self, url_table, external_path, like_name='likes', config_name='config.txt'):
        with open(config_name, 'r') as config_file:
            keywords = 'new neko keys = ', 'prev neko keys = ', 'like_keys = ', 'blacklist = ', 'activate_blacklist = '
            for line in config_file:
                for i in range(len(keywords)):
                    if keywords[i] in line:
                        if i == 0:
                            self.right = line[len(keywords[i]):].split(', ')
                        elif i == 1:
                            self.left = line[len(keywords[i]):].split(', ')
                        elif i == 2:
                            self.like_keys = line[len(keywords[i]):].split(', ')
                        elif i == 3:
                            blacklist = line[len(keywords[i]):].split(', ')
                        elif i == 4:
                            if line[len(keywords[i]):].rstrip('\n') == 'True':
                                activate_blacklist = True
                            else:
                                activate_blacklist = False

        self.tags = ['all', 'liked']
        globals()[self.tags[0]] = []
        globals()[self.tags[1]] = []

        with urllib.request.urlopen(url_table) as table_file:
            globals()['table'] = []
            for row in table_file:
                row = row.decode('utf-8').rstrip('\n')
                if any(blocked in row for blocked in blacklist) is False or activate_blacklist is False:
                    row_list = row.split('; ')

                    # index
                    row_list[0] = int(row_list[0])

                    # tags
                    row_list[2] = row_list[2].replace('(', '')
                    row_list[2] = row_list[2].replace(')', '')

                    row_list[2] = row_list[2].split(', ')
                    row_list[2] = row_list[2][:-1]

                    print(row_list)
                    for tag in row_list[2]:
                        if tag not in self.tags:
                            self.tags.append(tag)
                            globals()[tag] = []
                        globals()[tag].append(int(row_list[0]))
                    globals()[self.tags[0]].append(int(row_list[0]))
                    globals()['table'].append(row_list)

        with open(like_name, 'r') as likes_file:
            likes_string = likes_file.readline()
            likes_string = likes_string.rstrip('\n')

            globals()[self.tags[1]] = likes_string.split(', ')
            print(globals()[self.tags[1]])
            for i in range(len(globals()[self.tags[1]])):
                if globals()[self.tags[1]][i] != '':
                    globals()[self.tags[1]][i] = int(globals()[self.tags[1]][i])
                else:
                    globals()[self.tags[1]].pop(i)

        print(self.tags)
        for tag in self.tags:
            print(tag)
            print(globals()[tag])

    def parse_data(self):
        return self.tags

    def add_lists(self, list1, list2, mode):
        mode_keywords = 0, 2, 1

        if isinstance(list1, str):
            tuple1 = globals()[list1]
        else:
            tuple1 = list1
        if isinstance(list2, str):
            tuple2 = globals()[list2]
        else:
            tuple2 = list2

        print(tuple1, tuple2)

        final_list = []
        if mode == mode_keywords[0]:
            final_list = tuple1
            for element in tuple2:
                if element not in final_list:
                    final_list.append(element)
        elif mode == mode_keywords[1]:
            for element in tuple1:
                if element in tuple2:
                    final_list.append(element)
        elif mode == mode_keywords[2]:
            for element in tuple1:
                if element not in tuple2:
                    final_list.append(element)

        return final_list

    def string_to_list(self, filter_string):
        # final_list = self.add_lists('emo', globals()['epic'], 'or')
        operator_keywords = ' or ', ' and not ', ' and '
        if any(operator in filter_string for operator in operator_keywords) is False:
            print('Hi')
            final_list = globals()[filter_string]
        else:
            for u in range(len(operator_keywords)):
                if operator_keywords[u] in filter_string:
                    filter_strings = filter_string.split(operator_keywords[u])
                    print(filter_strings)
                    final_list = self.add_lists(filter_strings[0], filter_strings[1], u)
                    break

        return final_list


class Game:
    def __init__(self, parent, title):
        game = tkinter.Toplevel(parent)
        game.title(title)


def on_closing():
    global run
    run = False
    likes = globals()[tags[1]]
    print('likes.debug:' + str(likes))
    for i in range(len(likes)):
        if likes[i] == '':
            likes.pop(i)
        else:
            likes[i] = str(likes[i])
    likes.sort()
    likes_str = ', '.join(map(str, likes))
    print('liked: ' + likes_str)
    with open('likes', 'w') as likes_file:
        likes_file.write(likes_str)
    root.destroy()


def on_enter(event):
    filter_nekos()


def on_left(event):
    if str(filter_source.focus_get()) != '.!entry':
        prev_neko()


def on_right(event):
    if str(filter_source.focus_get()) != '.!entry':
        new_neko()


def on_like(event):
    liked_or_not.set(not liked_or_not.get())


root.protocol('WM_DELETE_WINDOW', on_closing)



def resize_image(img, size, mode):
    img_whidth, img_height = img.size

    if mode == True:
        if img_whidth / size[0] < img_height / size[1]:
            count = img_height / size[1]
            img_whidth = img_whidth / count
            img_height = size[1]
        else:
            count = img_whidth / size[0]
            img_height = img_height / count
            img_whidth = size[0]
    else:
        if img_whidth / size[0] < img_height / size[1]:
            count = img_whidth / size[0]
            img_height = img_height / count
            img_whidth = size[0]
        else:
            count = img_height / size[1]
            img_whidth = img_whidth / count
            img_height = size[1]

    img_size = round(img_whidth), round(img_height)
    img_rz = img.resize(img_size)

    return img_rz


def filter_nekos():
    global current_list
    global prev_filter_string
    global cycle_speed

    dummy.focus()
    easter_eg = 'play easter egg'
    cycle = 'cycle: '
    filter_string = filter_source.get()

    if filter_string == easter_eg:
        filter_source.delete(0, len(filter_string))
        filter_source.insert(0, prev_filter_string)
        trex_game = Game(root, 'trex game')
    elif filter_string.isdigit() is True:
        search_neko(int(filter_string))
        print(int(filter_string))
        filter_source.delete(0, len(filter_string))
        filter_source.insert(0, prev_filter_string)
    elif cycle in filter_string:
        cycle_speed = float(filter_string[len(cycle):])
        print(cycle_speed)
        filter_source.delete(0, len(filter_string))
        filter_source.insert(0, prev_filter_string)
    else:
        try:
            current_list = data.string_to_list(filter_string)

            if len(current_list) != 0:
                print(current_list)
                prev_filter_string = filter_string
                new_neko()
            else:
                print("there's nothing here")
        except Exception as e:
            print(e)
            print('check your spelling')


def load_neko(index):
    global img
    global url_img
    img_url = str(url_img) + str(index).zfill(4) + '.png'
    img = Image.open(requests.get(img_url, stream=True).raw)
    img = img.convert('RGB')

    img_description = table[index]
    img_description_str = 'Index: ' + str(img_description[0]).zfill(4) + '\n'
    for element in img_description[2]:
        img_description_str = img_description_str + element + '\n'
    img_description_label.configure(text=img_description_str)

    window_size = [root.winfo_width(), root.winfo_height()]
    update(window_size)


def manage_likes(index, mode):
    check = 'check'
    safe = 'safe'
    if mode == check:
        if tags[1] in table[index][2]:
            liked_or_not.set(True)
        else:
            liked_or_not.set(False)
    elif mode == safe:
        if liked_or_not.get() is True:
            if tags[1] not in table[index][2]:
                table[index][2].append(tags[1])
                globals()[tags[1]].append(index)
        else:
            if tags[1] in table[index][2]:
                table[index][2].remove(tags[1])
                globals()[tags[1]].remove(index)


def new_neko():
    global current_list
    manage_likes(history[len(history) - 1], 'safe')

    if random_or_not.get() is True:
        if len(current_list) > 1:
            index = random.randint(0, len(current_list) - 1)
            while history[len(history) - 1] == current_list[index]:
                index = random.randint(0, len(current_list) - 1)
            index = current_list[index]
        else:
            index = random.randint(0, len(current_list) - 1)
            index = current_list[index]
    else:
        if history[len(history) - 1] in current_list:
            if current_list.index(history[len(history) - 1]) + 2 < len(current_list):
                index = current_list[current_list.index(history[len(history) - 1]) + 1]
            else:
                index = current_list[0]
        else:
            index = current_list[0]

    history.append(index)
    if len(history) > 128:
        history.pop(0)

    manage_likes(history[len(history) - 1], 'check')
    load_neko(history[len(history) - 1])


def prev_neko():
    if len(history) > 2:
        manage_likes(history[len(history) - 1], 'safe')
        history.pop(len(history) - 1)
        manage_likes(history[len(history) - 1], 'check')

        load_neko(history[len(history) - 1])
    else:
        print('this was the first neko')


def search_neko(index):
    global img
    manage_likes(history[len(history) - 1], 'safe')
    history.append(index)
    manage_likes(index, 'check')
    img_url = str(url_img) + str(index).zfill(4) + '.png'
    img = Image.open(requests.get(img_url, stream=True).raw)

    img_description = table[index]
    img_description_str = 'Index: ' + str(img_description[0]).zfill(4) + '\n'
    for element in img_description[2]:
        img_description_str = img_description_str + element + '\n'
    img_description_label.configure(text=img_description_str)

    update([root.winfo_width(), root.winfo_height()])


def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    str = "#%02x%02x%02x" % rgb
    return str


def create_image(img, size):
    global ui

    canvas_size = size[0], size[1]
    img_fg = resize_image(img, size, True)
    img_bg = resize_image(img_fg, size, False)

    img_bg = img_bg.filter(ImageFilter.BoxBlur(30))

    fg_size = img_fg.size
    bg_size = img_bg.size

    img_bg.paste(img_fg, (
        int((bg_size[0] - fg_size[0]) / 2), int((bg_size[1] - fg_size[1]) / 2)))

    pos = (canvas_size[0] - bg_size[0]) / 2, (canvas_size[1] - bg_size[1]) / 2

    return img_bg, pos


def update(window_size):
    global img
    global ui

    img.convert('RGB')
    final_image, pos = create_image(img, (root.winfo_width() - ui, root.winfo_height()))
    img_tk = ImageTk.PhotoImage(final_image)
    label.configure(image=img_tk)
    label.img = img_tk
    label.place(x=int(pos[0]), y=int(pos[1]))

    avr_color_img = img.resize((1, 1))
    _avr_color = avr_color_img.getpixel((0, 0))
    select_color_list = [0, 0, 0]
    for i in range(3):
        if _avr_color[i] + 15 <= 255:
            select_color_list[i] = int(_avr_color[i] + 15)
        else:
            select_color_list[i] = 255
    _select_color = tuple(select_color_list)
    if _avr_color[0] + _avr_color[1] + _avr_color[2] > 450:
        _fg_color = 5, 5, 5
    else:
        _fg_color = 250, 250, 250
    avr_color = _from_rgb(_avr_color)
    fg_color = _from_rgb(_fg_color)
    select_color = _from_rgb(_select_color)

    global_tags_label.place(x=window_size[0] - ui, y=1)
    img_description_label.place(x=window_size[0] - ui, y=window_size[1] / 3)
    help_button.place(x=window_size[0] + 5 - ui, y=(window_size[1] / 3) * 2)
    random_checkbox.place(x=window_size[0] - ui, y=(window_size[1] / 3) * 2 + 30)
    liked_checkbox.place(x=window_size[0] - ui, y=(window_size[1] / 3) * 2 + 50)
    help_button.update()
    desktop_button.place(x=window_size[0] + 10 + help_button.winfo_width() - ui, y=(window_size[1] / 3) * 2)

    new_neko_button.update()
    x_button_pos = (window_size[0] - ui) - 2 - new_neko_button.winfo_width()
    new_neko_button.place(x=x_button_pos)
    x_button_pos = (window_size[0] - ui - new_neko_button.winfo_width()) - 4 - prev_neko_button.winfo_width()
    prev_neko_button.place(x=x_button_pos)
    filter_source.place(width=x_button_pos - (filter_button.winfo_width() + 4))

    global_tags_label.configure(bg=avr_color, fg=fg_color)
    img_description_label.configure(bg=avr_color, fg=fg_color)
    help_button.configure(bg=avr_color, fg=fg_color, activebackground=select_color, activeforeground=fg_color)
    random_checkbox.configure(bg=avr_color, fg=fg_color, activebackground=avr_color, activeforeground=fg_color,
                              selectcolor=avr_color)
    liked_checkbox.configure(bg=avr_color, fg=fg_color, activebackground=avr_color, activeforeground=fg_color,
                             selectcolor=avr_color)
    # up ui
    new_neko_button.configure(bg=avr_color, fg=fg_color, activebackground=select_color, activeforeground=fg_color)
    prev_neko_button.configure(bg=avr_color, fg=fg_color, activebackground=select_color, activeforeground=fg_color)
    filter_source.configure(bg=avr_color, fg=fg_color, bd=1)
    filter_button.configure(bg=avr_color, fg=fg_color, activebackground=select_color, activeforeground=fg_color)
    desktop_button.configure(bg=avr_color, fg=fg_color, activebackground=select_color, activeforeground=fg_color)


def help():
    info = 'type "cycle " and then the speed in s. 0 means no cycle through the imgs at all \njust type the tag of a ' \
           'picture to search it\ntag1 or tag2:              all nekos with at least one of those tags\ntag1 and ' \
           'tag2:           all nekos with both tags\ntag1 and not tag2:    all nekos with tag1 and not ' \
           'tag2\n\nKeybinds:\nnext neko: '

    info += str(right)
    info += '\nprevious neko: '
    info += str(left)
    info += '\nlike neko: '
    info += str(like_keys)
    messagebox.showinfo('info', info)


def set_background():
    global img
    global window_size

    print('bg')
    img.convert('RGB')
    final_image, pos = create_image(img, screen_size)
    img_size = final_image.size
    left = (img_size[0] - screen_size[0]) / 2
    right = (img_size[0] - screen_size[0]) / 2 + screen_size[0]
    top = (img_size[1] - screen_size[1]) / 2
    bottom = (img_size[1] - screen_size[1]) / 2 + screen_size[1]
    final_image = final_image.crop((left, top, right, bottom))
    final_image.save(os.path.expandvars(os.getcwd() + '/' + background_name))

    folder = os.path.expandvars(os.getcwd() + '/' + background_name)

    key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,
                                "Control Panel\\\\Desktop",
                                0, win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "0")
    win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "0")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, folder, 1 + 2)





img = Image.open(loading_screen)
# img.show()
final_image, pos = create_image(img, screen_size)
print(final_image)
img_tk = ImageTk.PhotoImage(final_image)
label.configure(image=img_tk)
label.img = img_tk
label.place(x=int(pos[0]), y=int(pos[1]))
root.update()



random_or_not = tkinter.BooleanVar()
liked_or_not = tkinter.BooleanVar()

try:
    # with open(os.path.expandvars(external_files + 'config.txt'), 'r') as keybinds_file:
    with open('config.txt', 'r') as keybinds_file:
        keywords = 'new neko keys = ', 'prev neko keys = ', 'like_keys = '
        for line in keybinds_file:
            for i in range(len(keywords)):
                if keywords[i] in line:
                    if i == 0:
                        right = line[len(keywords[i]):].split(', ')
                    elif i == 1:
                        left = line[len(keywords[i]):].split(', ')
                    elif i == 2:
                        like_keys = line[len(keywords[i]):].split(', ')

        globals()['likes'] = likes_string.split(', ')
except:
    left = ['<Left>', 'a']
    right = ['<Right>', '<space>', 'd']
    like_keys = ['l']

data = ReadDatabase('https://ln.topdf.de/img/table', '%appdata%/neko/')
tags = data.parse_data()

run = True
ui = 100
prev_window_size = []
cycle_speed = 0.0
history = [0]


# initialize ui
all_tags_str = ''
print(tags)
for tag in tags:
    all_tags_str += tag + ' (' + str(len(globals()[tag])) + ')\n'
global_tags_label = tkinter.Label(master=root, justify='left', anchor='nw', text=all_tags_str)

img_description_label = tkinter.Label(master=root, justify='left')

random_checkbox = tkinter.Checkbutton(master=root, justify='left', anchor='nw', text='random', var=random_or_not)
liked_checkbox = tkinter.Checkbutton(master=root, justify='left', anchor='nw', text='liked', var=liked_or_not)
desktop_button = tkinter.Button(master=root, text='set as bg', command=set_background)
random_or_not.set(True)

help_button = tkinter.Button(master=root, text='  ?  ', command=help)
filter_button = tkinter.Button(master=root, text='Filter/Search', command=filter_nekos)
filter_button.place(x=1, y=1)
filter_source = tkinter.Entry(master=root, width=70, justify='left')
filter_source.insert(tkinter.INSERT, start_filter)
filter_source.bind('<Return>', on_enter)
dummy = tkinter.Entry(master=root)
dummy.place(x=-1000000, y=1000000)
filter_button.update()
filter_source.place(x=filter_button.winfo_width() + 4, y=5)

print((global_tags_label.winfo_width(), global_tags_label.winfo_height()))
global_tags_label.configure(width=100, height=int(window_size[1] / 2))

new_neko_button = tkinter.Button(master=root, text='new neko', command=new_neko)

prev_neko_button = tkinter.Button(master=root, text='prev neko', command=prev_neko)
for key in right:
    root.bind(key, on_right)
for key in left:
    root.bind(key, on_left)
for key in like_keys:
    root.bind(key, on_like)

root.update()
filter_nekos()

prev_time = 0.0
while run is True:
    if cycle_speed > 0:
        current_time = time.time()
        if current_time - prev_time >= cycle_speed:
            prev_time = current_time
            new_neko()

    window_size = [root.winfo_width(), root.winfo_height()]
    if window_size != prev_window_size:
        prev_window_size = window_size
        update(window_size)

    root.update()
