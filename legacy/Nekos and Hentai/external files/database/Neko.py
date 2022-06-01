'''
TO DO
classe you say new neko and you get the finished image
face recognition
easter egg
Desktop
installer or updater
Logik hinzufügen
'''
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

loading_screen = 'loading_screen.jpg'
start_filter = 'all and not lewd'
prev_filter = start_filter
img_description = ''
ui_width = 150
tags = []
run = True
cycle_speed = 0
prev_window_size = []


class ReadDatabase:
    def __init__(self, url_table, like_name='likes', config_name='config.txt'):
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
            tuple1 = tuple(list1)
        if isinstance(list2, str):
            tuple2 = globals()[list2]
        else:
            tuple2 = tuple(list2)

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


class Images:
    def __init__(self, start_filter):
        global tags
        self.img_url_base = 'https://ln.topdf.de/img/images/'

        self.data = ReadDatabase('https://ln.topdf.de/img/table')
        tags = self.data.parse_data()
        self.prev_filer = start_filter
        self.current_list = []
        self.filter_neko(start_filter)

        self.img_tag = 0
        self.history = []

    def resize_image(self, img, size, mode):
        img_width, img_height = img.size

        if mode is True:
            if img_width / size[0] < img_height / size[1]:
                count = img_height / size[1]
                img_width = img_width / count
                img_height = size[1]
            else:
                count = img_width / size[0]
                img_height = img_height / count
                img_width = size[0]
        else:
            if img_width / size[0] < img_height / size[1]:
                count = img_width / size[0]
                img_height = img_height / count
                img_width = size[0]
            else:
                count = img_height / size[1]
                img_width = img_width / count
                img_height = size[1]

        img_size = round(img_width), round(img_height)
        img_rz = img.resize(img_size)

        return img_rz

    def create_img(self, img, size):
        img = img.convert('RGB')

        canvas_size = size[0], size[1]
        img_fg = self.resize_image(img, size, True)
        img_bg = self.resize_image(img_fg, size, False)

        img_bg = img_bg.filter(ImageFilter.BoxBlur(30))

        fg_size = img_fg.size
        bg_size = img_bg.size

        img_bg.paste(img_fg, (
            int((bg_size[0] - fg_size[0]) / 2), int((bg_size[1] - fg_size[1]) / 2)))

        img_size = img_bg.size
        left = (img_size[0] - canvas_size[0]) / 2
        right = (img_size[0] - canvas_size[0]) / 2 + canvas_size[0]
        top = (img_size[1] - canvas_size[1]) / 2
        bottom = (img_size[1] - canvas_size[1]) / 2 + canvas_size[1]
        img_bg = img_bg.crop((left, top, right, bottom))

        return img_bg

    def filter_neko(self, filter):
        try:
            list = self.data.string_to_list(filter)
            print('new list: ' + str(list))
            if len(list) > 0:
                self.current_list = list
            else:
                print('theres nothing here')
        except Exception as e:
            print(e)
            print('check your spelling')

    def prev_neko(self, size):
        if len(self.history) > 0:
            self.history.pop(-1)
            self.img_tag = self.history[-1]

            img_url = self.img_url_base + str(self.img_tag).zfill(4) + '.png'
            self.img = Image.open(requests.get(img_url, stream=True).raw)
            self.img = self.create_img(self.img, size)

            img_description = table[self.current_list[self.img_tag]]
            img_description_str = 'Index: ' + str(img_description[0]).zfill(4) + '\n'
            for element in img_description[2]:
                img_description_str = img_description_str + element + '\n'

        return self.img, img_description_str

    def new_neko(self, filter, random_or_not, size):
        print('new neko')
        if filter != self.prev_filer:
            print(filter)
            self.filter_neko(filter)
            self.prev_filer = filter

        print(self.current_list)
        if random_or_not:
            self.img_tag = random.randint(0, len(self.current_list) - 1)
        else:
            if self.img_tag + 1 < len(self.current_list):
                self.img_tag += 1
            else:
                self.img_tag = 0

        if len(self.history) >= 128:
            self.history.pop(0)
        self.history.append(self.current_list[self.img_tag])

        img_url = self.img_url_base + str(self.current_list[self.img_tag]).zfill(4) + '.png'
        self.img = Image.open(requests.get(img_url, stream=True).raw)
        self.img = self.create_img(self.img, size)

        img_description = table[self.current_list[self.img_tag]]
        img_description_str = 'Index: ' + str(img_description[0]).zfill(4) + '\n'
        for element in img_description[2]:
            img_description_str = img_description_str + element + '\n'

        return self.img, self.prev_filer, img_description_str

    def search_neko(self, img_tag, size):
        img_url = self.img_url_base + str(img_tag).zfill(4) + '.png'
        self.img = Image.open(requests.get(img_url, stream=True).raw)
        self.img = self.create_img(self.img, size)

        img_description = table[self.current_list[self.img_tag]]
        img_description_str = 'Index: ' + str(img_description[0]).zfill(4) + '\n'
        for element in img_description[2]:
            img_description_str = img_description_str + element + '\n'

        return self.img, img_description_str


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
def on_searching(event):
    dummy.focus()
    new_neko()
def set_background(img, size):
    print('bg')
    img.convert('RGB')
    final_image = create_image(img, size)
    final_image.save(os.path.expandvars(os.getcwd() + '/' + background_name))

    folder = os.path.expandvars(os.getcwd() + '/' + background_name)

    key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,
                                "Control Panel\\\\Desktop",
                                0, win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "0")
    win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "0")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, folder, 1 + 2)
def show_image(img):
    img_tk = ImageTk.PhotoImage(img)
    label.configure(image=img_tk)
    label.img = img_tk
    label.update()
    update_color(img)
def new_neko(event=None):
    global cycle_speed
    global prev_filter

    easter_eg = 'play easter egg'
    cycle = 'cycle: '

    if event is not None:
        if str(filter_source.focus_get()) != '.!entry': get_new=True
        else:   get_new=False
    else:   get_new=True

    if get_new is True:
        filter = filter_source.get()
        if filter == easter_eg:
            trex_game = Game(root, 'trex game')
            filter_source.delete(0, len(filter))
            filter_source.insert(0, prev_filter)
            return
        if filter.isdigit() is True:
            print(filter)
            search_neko(int(filter))
            filter_source.delete(0, len(filter))
            filter_source.insert(0, prev_filter)
            return
        if cycle in filter:
            cycle_speed = float(filter[len(cycle):])
            filter_source.delete(0, len(filter))
            filter_source.insert(0, prev_filter)
            print(cycle_speed)
            return

        random_ = True
        size = root.winfo_width(), root.winfo_height()

        neko_image, prev_filter, img_description_str = Neko.new_neko(filter, random_, size)
    
        show_image(neko_image)
def prev_neko(event=None):
    if event is not None:
        if str(filter_source.focus_get()) != '.!entry': get_new=True
        else:   get_new=False
    else:   get_new=True

    if get_new is True:
        size = root.winfo_width(), root.winfo_height()
        neko_img = Neko.prev_neko(size)
        show_image(neko_img)
def search_neko(tag):
    size = root.winfo_width(), root.winfo_height()
    neko_img = Neko.search_neko(tag, size)
    show_image(neko_img)

def update_color(img):
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
    avr_color = "#%02x%02x%02x" % _avr_color
    fg_color = "#%02x%02x%02x" % _fg_color
    select_color = "#%02x%02x%02x" % _select_color

    new_neko_button.configure(bg=avr_color, fg=fg_color, activebackground=select_color, activeforeground=fg_color)
    prev_neko_button.configure(bg=avr_color, fg=fg_color, activebackground=select_color, activeforeground=fg_color)
    filter_source.configure(bg=avr_color, fg=fg_color, bd=1)

    bg_label.configure(bg=avr_color)
    global_tags_label.configure(bg=avr_color)
def update(size):
    global ui_width
    new_neko_button.place(x=(size[0] - ui_width) - 2 - new_neko_button.winfo_width())
    new_neko_button.update()
    prev_neko_button.place(x=size[0] - (4 + prev_neko_button.winfo_width() + (size[0] - new_neko_button.winfo_x())))
    prev_neko_button.update()
    filter_source.place(width=size[0] - (8 + (size[0] - prev_neko_button.winfo_x())))

    bg_label.place(x=size[0] - ui_width, y=0, width=ui_width, height=size[1])
    pass


# creating instance of Images class
Neko = Images('all and not lewd')

# create loading screen and window
img = Image.open(loading_screen)
screen_size = pyautogui.size()
img = Neko.create_img(img, screen_size)

root = tkinter.Tk()
root.title('NEKOS!!!')
root.state('zoomed')
label = tkinter.Label(master=root)
img_tk = ImageTk.PhotoImage(img)
label.configure(image=img_tk)
label.img = img_tk
label.place(x=0, y=0)
root.update()

root.protocol('WM_DELETE_WINDOW', on_closing)

# keybindings
try:
    with open('config.txt', 'r') as keybinds_file:
        keywords = 'new neko keys = ', 'prev neko keys = ', 'like_keys = '
        for line in keybinds_file:
            for i in range(len(keywords)):
                if keywords[i] in line:
                    if i == 0:
                        right_keys = line[len(keywords[i]):].split(', ')
                    elif i == 1:
                        left_keys = line[len(keywords[i]):].split(', ')
                    elif i == 2:
                        like_keys = line[len(keywords[i]):].split(', ')

        globals()['likes'] = likes_string.split(', ')
except:
    left = ['<Left>', 'a']
    right = ['<Right>', '<space>', 'd']
    like_keys = ['l']

window_size = [root.winfo_width(), root.winfo_height()]

# search bar
filter_source = tkinter.Entry(master=root, width=70, justify='left')
filter_source.place(x=4, y=4)
filter_source.insert(tkinter.INSERT, start_filter)
filter_source.bind('<Return>', on_searching)
dummy = tkinter.Entry(master=root)
dummy.place(x=-1000000, y=1000000)

# buttons top
new_neko_button = tkinter.Button(master=root, text='new neko', command=new_neko)
prev_neko_button = tkinter.Button(master=root, text='prev neko', command=prev_neko)

# ui side
bg_label = tkinter.Label(master=root, justify='left', anchor='nw')
all_tags_str = ''
for tag in tags:
    all_tags_str += tag + ' (' + str(len(globals()[tag])) + ')\n'
global_tags_label = tkinter.Label(master=root, justify='left', anchor='nw', text=all_tags_str)
global_tags_label.place(x=window_size[0]-(ui_width-1), y=1)
global_tags_label.update()

for key in left_keys:
    root.bind(key, prev_neko)
for key in right_keys:
    root.bind(key, new_neko)
for key in like_keys:
    root.bind(key, new_neko)

new_neko()
update((root.winfo_width(), root.winfo_height()))

prev_time = 0.0
while run is True:
    root.update()
    if cycle_speed > 0:
        current_time = time.time()
        if current_time - prev_time >= cycle_speed:
            prev_time = current_time
            new_neko()

    window_size = [root.winfo_width(), root.winfo_height()]
    if window_size != prev_window_size:
        prev_window_size = window_size
        update(window_size)
root.destroy()