import tkinter
import pyautogui
from PIL import ImageTk, Image
import requests
import random
import urllib

table = []
tags = ['all']

url_img = 'https://ln.topdf.de/img/images/'
url_table = 'https://ln.topdf.de/img/table'


with urllib.request.urlopen(url_table) as table_file:
    for row in table_file:
        row = row.decode('utf-8').rstrip('\n')
        row_list = row.split('; ')

        # index
        row_list[0] = int(row_list[0])

        # tags
        row_list[2] = row_list[2].replace('(', '')
        row_list[2] = row_list[2].replace(')', '')

        row_list[2] = row_list[2].split(', ')
        row_list[2] = row_list[2][:-1]

        # search new tags
        for element in row_list[2]:
            if element not in tags:
                tags.append(element)

        table.append(row_list)
print(tags)

for tag in tags:
    globals()[tag] = []

    for row in table:
        if tag in row[2]:
            globals()[tag].append(row[0])

    # print(tag + ':')
    # print(globals()[tag])
    # print('')
for i in range(len(table)):
    globals()[tags[0]].append(i)

for i in range(len(table)):
    element = table[i]
    if element[0] != i:
        print('TFFFFFFFFFFFFFFFFFF?')


def tag_and_tag(_start, include, _include):
    final_list = []


    if _include is True:
        for _element in _start:
            if _element in include:
                final_list.append(_element)
    else:
        for element in _start:
            #start = list(_start)
            if element not in include:
                final_list.append(element)

    return final_list


def tag_or_tag(start, include):
    final_list = start

    for element in include:
        if element not in final_list:
            final_list.append(element)

    return final_list


def substring_to_list(string):
    and_ = ' and '
    and_not = ' and not '
    or_ = ' or '

    final_list = []

    is_tuple = isinstance(string, tuple)
    # print('is tuple: ' + str(is_tuple))
    # print('string: ' + str(string))

    if is_tuple is True:
        liste = [[], []]


        string_list = list(string)
        if or_ in string_list[0] or or_ in string_list[1]:
            for i in range(len(liste)):
                if isinstance(string_list[i], list):
                    liste[i] = string[i]
                else:
                    string_list[i] = string_list[i].replace(or_, '')
                    liste[i] = globals()[string_list[i]]
            final_list = tag_or_tag(liste[0], liste[1])

        if and_not in string_list[0] or and_not in string_list[1]:
            for i in range(len(liste)):
                if isinstance(string_list[i], list):
                    liste[i] = string[i]
                else:
                    string_list[i] = string_list[i].replace(' and not ', '')
                    # print(string_list)
                    liste[i] = globals()[string_list[i]]
            final_list = tag_and_tag(liste[0], liste[1], False)

        if and_ in string_list[0] or and_ in string_list[1]:
            for i in range(len(liste)):
                if isinstance(string_list[i], list):
                    liste[i] = string[i]
                else:
                    string_list[i] = string_list[i].replace(and_, '')
                    liste[i] = globals()[string_list[i]]
            final_list = tag_and_tag(liste[0], liste[1], True)
    else:
        if or_ in string:
            string = string.split(or_)
            final_list = tag_or_tag(globals()[string[0]], globals()[string[1]])

        if and_not in string:
            string = string.split(and_not)
            final_list = tag_and_tag(globals()[string[0]], globals()[string[1]], False)

        if and_ in string:
            string = string.split(and_)
            final_list = tag_and_tag(globals()[string[0]], globals()[string[1]], True)

    return final_list


def string_to_list(string):
    if ' or ' not in string and ' and ' not in string and ' and not ' not in string:
        final_list = globals()[string]
    else:
        final_list = []
        string = '(' + string + ')'

        if '(' in string:
            depth = 0
            brackets = []

            for i in range(len(string)):
                if string[i] == '(':
                    brackets.append([depth, i])
                    depth += 1

                if string[i] == ')':
                    depth -= 1
                    for element in reversed(brackets):
                        if depth == element[0]:
                            u = brackets.index(element)
                            brackets[u].append(i)
                            break

        brackets = sorted(brackets, key=lambda l: l[0], reverse=True)
        # print(brackets)

        temp_list = [[],[]]
        prev_element = brackets[0]
        for i in  range(len(brackets)):
            element = brackets[i]
            # print(element)
            # print(prev_element)
            if element[0] != 0:
                if brackets[i - 1][1] == element[1]:
                    u=0
                else:
                    u=1
                if element[0] == prev_element[0]:
                    temp_list[u] = substring_to_list(string[element[1] + 1:element[2]])
                else:
                    #print('ok')
                    temp_list[1 - last_u] = string[element[1] + 1:prev_element[1]]
                    temp_list[u] = substring_to_list(tuple(temp_list))
                last_u = u
            else:
                if prev_element[0] != 0:
                    temp_list[1 - last_u] = string[element[1] + 1:prev_element[1]]
                    final_list = substring_to_list(tuple(temp_list))
                else:
                    final_list = substring_to_list(string[element[1] + 1:element[2]])

            prev_element = element

    return final_list


current_list = string_to_list('(neko and not lewd)')


# create window
screen_size = pyautogui.size()
window_size = screen_size

root = tkinter.Tk()
root.title('NEKOS!!!')
root.geometry(str(screen_size[0]) + "x" + str(screen_size[1]) + "+" + str(-(265 + screen_size[1])) + "+0")
label = tkinter.Label()
label.place(x=0,y=0)
random_or_not = tkinter.IntVar()



def resize_image(img, size, mode):
    img_whidth, img_height = img.size

    if mode == True:
        if img_whidth/size[0] > img_height/size[1]:
            count = img_whidth/size[0]
            img_height = img_height/count
            img_whidth = size[0]
        else:
            count = img_height/size[1]
            img_whidth = img_whidth/count
            img_height = size[1]
    else:
        if img_whidth/size[0] < img_height/size[1]:
            count = img_whidth/size[0]
            img_height = img_height/count
            img_whidth = size[0]
        else:
            count = img_height/size[1]
            img_whidth = img_whidth/count
            img_height = size[1]

    img_size = round(img_whidth), round(img_height)
    img_rz = img.resize(img_size)

    return img_rz


def filter_nekos():
    global current_list

    filter_string = filter_source.get()

    try:
        current_list = string_to_list(filter_string)

        if len(current_list) != 0:
            print(current_list)
            new_neko()
        else:
            print("there's nothing here")
    except:
        print('check your spelling')


index = -1
def new_neko():
    global current_list
    global index
    global url_img

    if random_or_not.get() == 1:
        index = random.randint(0,len(current_list))
        print(index)
    else:
        if index+1 < len(current_list):
            index += 1
        else:
            index = 0

    img_url = str(url_img) + str(current_list[index]).zfill(4) + '.png'
    img = Image.open(requests.get(img_url, stream=True).raw)
    img_resized = resize_image(img, window_size, True)
    imgTk = ImageTk.PhotoImage(img_resized)
    label.configure(image=imgTk)
    label.img = imgTk
    pos = (window_size[0]-img_resized.size[0])/2, 0
    label.place(x=int(pos[0]),y=int(pos[1]))

    img_description = table[current_list[index]]
    img_description_str = 'Index: ' + str(img_description[0]).zfill(4) + '\n'
    for element in img_description[2]:
        img_description_str = img_description_str + element + '\n'
    img_description_label.configure(text=img_description_str)


    print(img_url)


# ui
filter_button = tkinter.Button(master=root, text='Filter Nekos', command=filter_nekos)
filter_button.place(x=1, y=1)
filter_source = tkinter.Entry(master=root, width=70)
filter_source.insert(tkinter.INSERT, 'neko and not lewd')
filter_source.place(x=79, y=5)

all_tags_str = ''
for tag in tags:
    all_tags_str += tag + ' (' + str(len(globals()[tag])) + ')\n'
global_tags_label = tkinter.Label(master=root, text=all_tags_str).place(x=window_size[0] - 100, y=1)

img_description_label = tkinter.Label(master=root)
img_description_label.place(x=window_size[0] - 100, y=250)

random_checkbox = tkinter.Checkbutton(master=root, text='random', var=random_or_not).place(x=window_size[0]-100,y=200)

new_neko_button = tkinter.Button(master=root, text='NEW NEKO!!!', command=new_neko)
new_neko_button.place(x=510, y=1)

filter_nekos()

root.mainloop()