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

class ReadDatabase:
    def __init__(self, url_table, external_path, like_name='likes', config_name='config.txt'):
        with open(os.path.expandvars(external_path + config_name), 'r') as config_file:
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

        with open(os.path.expandvars(external_path + like_name), 'r') as likes_file:
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

data = ReadDatabase
data = ReadDatabase('https://ln.topdf.de/img/table', '%appdata%/neko/')
tags = data.parse_data()

current_list = data.string_to_list('emo')
print(current_list)
i=0
for index in current_list:
    img_url = str(url_img) + str(index).zfill(4) + '.png'
    img = Image.open(requests.get(img_url, stream=True).raw)
    img.save('emo/' + str(i).zfill(2) + '.png')
    i += 1