'''
import tkinter 
from tkinter import *
from tkinter import messagebox

import pyautogui
import keyboard

from PIL import ImageTk, Image, ImageFilter
import requests
import random


from urllib.request import Request, urlopen
import urllib.request
from lxml import html, etree
from io import StringIO

from os import path
import os
'''
import urllib.request

from os import path

import pyautogui
from tkinter import *
from PIL import ImageTk, Image, ImageFilter


ext_path = path.expandvars('%APPDATA%\\Neko\\')
print(ext_path)

def Initialize():
    global ext_path
    url = 'https://ln.topdf.de/'

        
    img_count = []
    liked = []
    with urllib.request.urlopen(url + '/img/table') as table:
        for line in table:
            img_count.append(int(line.decode('utf-8').rstrip('\n')))
        print(img_count)


    with open(ext_path + 'liked', 'r') as file:
        for line in file:
            line = line.rstrip('\n')
            line = line.split(', ')
            for i in range(len(line)):
                line[i] = line[i].zfill(4) + '.png'
            liked.append(line)
        print(liked)


    with open(ext_path + 'config.txt', 'r') as file:
        line = file.readline()
        line = line[14:19]
        print(bool(line))

    
Initialize()






'''
neko_tag = 0
total = 0
neko_index = [0, 0]

hentai_page = 1
load_new_pages = False
load_new_nekos = False
run = True
neko_mode = True

with open(path.expandvars('%APPDATA%\\Neko\\version'), 'r') as version_file:
    version = version_file.readline()
    version_web_file = urllib.request.urlopen('https://ln.topdf.de/version')
    for line in version_web_file:
        version_web = line.decode('utf-8')

    if version_web != version:
        print('new Version available')
        os.startfile(path.expandvars('%APPDATA%\\Neko\\NekoInstaller.exe'))
        exit()
    else:
        print('no new Version available')


conf = open(path.expandvars('%APPDATA%\\Neko\\config.txt'), 'r')
Neko_cute_path = conf.readline()
Neko_cute_path = Neko_cute_path[12:len(Neko_cute_path)]
Neko_cute_path = Neko_cute_path.replace('\n', '')
print(Neko_cute_path)


Neko_lewd_path = conf.readline()
Neko_lewd_path = Neko_lewd_path[12:len(Neko_lewd_path)]
Neko_lewd_path = Neko_lewd_path.replace('\n', '')
print(Neko_lewd_path)


EndMessageOrNot_str = conf.readline()
if 'True' in EndMessageOrNot_str:
    EndMessageOrNot = True
else:
    EndMessageOrNot = False
    if not 'False' in EndMessageOrNot_str:
        print("Config Error: Can't Find bool in Line 1 (Maybe check the capital letter)")

NSFWorNot_str = conf.readline()
if 'True' in NSFWorNot_str:
    NSFWorNot = True
else:
    NSFWorNot = False
    if not 'False' in NSFWorNot_str:
        print("Config Error: Can't Find bool in Line 1 (Maybe check the capital letter)")

paralax_str = conf.readline()


paralax = float(paralax_str[10:len(paralax_str)])
print(paralax)
                



print(NSFWorNot)
conf.close()


neko_list_cute_all = []
neko_list_cute_liked = []
neko_cute_file = open(path.expandvars(Neko_cute_path), 'r')

neko_cute = neko_cute_file.readline()
neko_cute = neko_cute.rstrip('\n')
liked = neko_cute_file.readline()

while liked != '':
    neko_list_cute_all.append(neko_cute)
    if 'True' in liked:
        neko_list_cute_liked.append(neko_cute)

    neko_cute = neko_cute_file.readline()
    neko_cute = neko_cute.rstrip('\n')
    liked = neko_cute_file.readline()

    
neko_cute_file.close()
#print(neko_list_cute_liked)



neko_list_lewd_all = []
neko_list_lewd_liked = []

neko_lewd_file = open(path.expandvars(Neko_lewd_path), 'r')

neko_lewd = neko_lewd_file.readline()
neko_lewd = neko_lewd.rstrip('\n')
liked = neko_lewd_file.readline()

while liked != '':
    neko_list_lewd_all.append(neko_lewd)
    if 'True' in liked:
        neko_list_lewd_liked.append(neko_lewd)

    neko_lewd = neko_lewd_file.readline()
    neko_lewd = neko_lewd.rstrip('\n')
    liked = neko_lewd_file.readline()

    
neko_cute_file.close()
    






neko_tuple_cute = tuple(neko_list_cute_all), tuple(neko_list_cute_liked)
neko_tuple_lewd = tuple(neko_list_lewd_all), tuple(neko_list_lewd_liked)

neko_tuple = neko_tuple_cute, neko_tuple_lewd














width, height = pyautogui.size()

window_size = width, height
print(window_size)
canvas_size = width-232, height-75


tk = Tk()

LewdOrNot = IntVar()
LikeOrNot = IntVar()
OnlyLike = IntVar()
RandomOrNot = IntVar()

imgLabel_canvas = tkinter.Label()



tk.title('NEKOS!!!')

tk.geometry(str(width) + "x" + str(height) + "+-8+0")


neko_url = ''





def NewNeko():
    global load_new_nekos
    global neko_index
    global next_neko_index
    global settings
    global next_neko
    global neko_url
    global next_neko_url

    

    new_settings = [LewdOrNot.get(), RandomOrNot.get(), OnlyLike.get()]

    if settings != new_settings:
        LoadNekos()
        
    ShowImage(next_neko)
    
    inNekoNumber.delete(0,END)
    inNekoNumber.insert(0,next_neko_index[new_settings[0]])
    
    CheckForLike(neko_url)
    print('neko url: ' + neko_url)
    SetLike(next_neko_url)

    print('neko URL')
    print(next_neko_url)
    print('')
    
    neko_index = next_neko_index

    neko_url = next_neko_url
    load_new_nekos = True
      
        
        







def SearchNeko():
    global load_new_nekos
    global neko_index
    global neko_url

    
    settings = [LewdOrNot.get(), RandomOrNot.get(), OnlyLike.get()]
    
    CheckForLike(neko_url)

    neko_index[settings[0]] = int(inNekoNumber.get())

    

    
    neko_url = neko_tuple [settings[0]] [0][next_neko_index[settings[0]]]

    SetLike(neko_url)

    print('neko URL:')
    print(neko_url + '\n')
    
    neko = Image.open(requests.get(neko_url, stream=True).raw)

    ShowImage(neko)

    neko_index = next_neko_index

    load_new_nekos = True
    




def LoadNekos():
    global neko_index
    global next_neko_index
    global neko_tuple
    global settings
    global next_neko
    global next_neko_url

    next_neko_index = neko_index
    settings = [LewdOrNot.get(), RandomOrNot.get(), OnlyLike.get()]

    if settings[1] == 0:
        next_neko_index[settings[0]] += 1
        if next_neko_index[settings[0]] >= len(neko_tuple [settings[0]] [settings[2]]):
            next_neko_index[settings[0]] = 0
        
    else:
        next_neko_index[settings[0]] = random.randint(0, len(neko_tuple [settings[0]] [settings[2]]) - 1)
        
    next_neko_url = neko_tuple [settings[0]] [settings[2]][next_neko_index[settings[0]]]
    


    

    next_neko = Image.open(requests.get(next_neko_url, stream=True).raw)

    neko_mode = True
   







def CheckForLike(nekoURL):
    if LikeOrNot.get() == 1:
        if LewdOrNot.get() == 1:
            if nekoURL not in neko_list_lewd_liked:
                neko_list_lewd_liked.append(nekoURL)             
        else:
            if nekoURL not in neko_list_cute_liked:
                neko_list_cute_liked.append(nekoURL)
    else:
        if LewdOrNot.get() == 1:
            if nekoURL in neko_list_lewd_liked:
                neko_list_lewd_liked.remove(nekoNumber)
                        
        else:
            if nekoURL in neko_list_cute_liked:
                neko_list_cute_liked.remove(nekoURL)
    LikeOrNot.set(0)







def SetLike(nekoURL):
    if LewdOrNot.get() == 1:
        if nekoURL in neko_list_lewd_liked:
            LikeOrNot.set(1)
        else:
            LikeOrNot.set(0)

    else:
        if nekoURL in neko_list_cute_liked:
            LikeOrNot.set(1)
        else:
            LikeOrNot.set(0)



def on_closing():
    global run
    global neko_mode
    global EndMessageOrNot
    global neko_list_cute_liked
    global neko_list_lewd_liked


    neko_cute_file = open(path.expandvars(Neko_cute_path), 'r')
    lines = neko_cute_file.readlines()
    i = 0
    while i <= len(lines)-2:
        lines[i+1] = 'liked = ' + str(lines[i].rstrip('\n') in neko_list_cute_liked) + '\n'
        i += 2
    neko_cute_file = open(path.expandvars(Neko_cute_path), 'w')   
    neko_cute_file.writelines(lines)
    neko_cute_file.close()


    neko_lewd_file = open(path.expandvars(Neko_lewd_path), 'r')
    lines = neko_lewd_file.readlines()
    i = 0
    while i <= len(lines)-2:
        lines[i+1] = 'liked = ' + str(lines[i].rstrip('\n') in neko_list_lewd_liked) + '\n'
        i += 2
    neko_lewd_file = open(path.expandvars(Neko_lewd_path), 'w')   
    neko_lewd_file.writelines(lines)
    neko_lewd_file.close()




    
    run = False


    if EndMessageOrNot == True:
        if neko_mode == True:
            if LewdOrNot.get() == 0:
                end_message = "No more Neko cuties?"
            else:
                end_message = "This Neko was lewd!\nDid you cum?"
        else:
            end_message = "This Hentai was lewd!\nDid you cum?" 
        if messagebox.askokcancel("^^", end_message):
            tk.destroy()
    else:
        tk.destroy()
tk.protocol("WM_DELETE_WINDOW", on_closing)




def SearchHentai():
    global hentai_page
    global hentai_next
    global hentai_current
    
    global imgURL
    global load_new_pages

    global neko_mode

    
    hentai_page = 1

    
    
    hentaiNumber = inHentaiNumber.get()
    hentaiURL = 'https://nhentai.net/g/' + str(hentaiNumber) + '/1/'
    print(hentaiURL)    

    page = requests.get(hentaiURL)
    tree = html.fromstring(page.content)

    imgURLlist = tree.xpath('//*[@id="image-container"]/a/img/@src')
    imgURLstr = imgURLlist[0]
    imgURL = imgURLstr[:len(imgURLstr) - 5]
    
    hentai_current = Image.open(requests.get(imgURL + str(hentai_page) + '.jpg', stream=True).raw)

    ShowImage(hentai_current)

    inPage.delete(0,END)
    inPage.insert(0,hentai_page)

    load_new_pages = True





def PrevPage():
    global hentai_page
    global hentai_next
    global hentai_current
    global hentai_prev
    
    global load_new_pages
    
    if hentai_prev != None:
        ShowImage(hentai_prev)

        hentai_page = hentai_page - 1
        inPage.delete(0,END)
        inPage.insert(0,hentai_page)
        
        hentai_current = hentai_prev        

        load_new_pages = True
            
    else:
        print('sadly this was the first page')



def NextPage():
    global hentai_page
    global hentai_next
    global hentai_current
    global hentai_prev

    global load_new_pages


    if hentai_next != None:
        ShowImage(hentai_next)

        hentai_page = hentai_page + 1
        inPage.delete(0,END)
        inPage.insert(0,hentai_page)
        
        hentai_current = hentai_next

        load_new_pages = True
    else:
        print('sadly this was the last page')
  


def GoToPage():
    global hentai_page
    global hentai_next
    global hentai_current
    global hentai_prev
    
    global load_new_pages

    new_hentai_page = int(inPage.get())

    try:
        hentai_current = Image.open(requests.get(imgURL + str(new_hentai_page) + '.jpg', stream=True).raw)
        ShowImage(hentai_current)

        inPage.delete(0,END)
        inPage.insert(0,new_hentai_page)
        hentai_page = new_hentai_page

        load_new_pages = True        
    except:
        print('This Hentai is not so long')


def LoadPages():
    global hentai_page
    global hentai_next
    global hentai_current
    global hentai_prev
    
    global imgURL

    global neko_mode


    if hentai_page > 1:
        hentai_prev = Image.open(requests.get(imgURL + str(hentai_page - 1) + '.jpg', stream=True).raw)
    else:
        hentai_prev = None

    try:
        hentai_next = Image.open(requests.get(imgURL + str(hentai_page + 1) + '.jpg', stream=True).raw)
    except:
        hentai_next = None

    neko_mode = False
    



def ResizeImage(img, size, mode):
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
    
    return(img_rz)


    

def ShowImage(img):
    global window_size
    global canvas_size
    global img_bg
    global img_fg



    mouse_x, mouse_y = pyautogui.position()
    if window_size[0] < window_size[1]:
        paralax_size = window_size[0]
    else:
        paralax_size = window_size[1]


    
    img_fg = ResizeImage(img, canvas_size, True)
    img_bg = ResizeImage(img_fg, (window_size[0] * (1+paralax), window_size[1] * (1+paralax)), False)
    img_bg = img_bg.filter(ImageFilter.BoxBlur(30))

    pos_bg = (window_size[0]-img_bg.size[0])/2 * (paralax*((window_size[0] - mouse_x)/paralax_size)), (paralax_size-img_bg.size[1])/2 * (paralax*((window_size[1] - mouse_y)/paralax_size))

    img_canvas = img_bg.copy()
    img_whidth, img_height = img_fg.size
    img_canvas.paste(img_fg, (int(-pos_bg[0] + (canvas_size[0]-img_whidth)/2), int(-pos_bg[1]+ (canvas_size[1]-img_height)/2)))

    
    

    imgTk_canvas = ImageTk.PhotoImage(img_canvas)
    imgLabel_canvas.configure(image=imgTk_canvas)
    imgLabel_canvas.img_canvas = imgTk_canvas
    mouse_x, mouse_y = pyautogui.position()
    imgLabel_canvas.place(x=pos_bg[0],y=pos_bg[1])


    

def UpdateImage():
    global img_bg
    global img_fg

    mouse_x, mouse_y = pyautogui.position()
    if window_size[0] < window_size[1]:
        paralax_size = window_size[0]
    else:
        paralax_size = window_size[1]
        
    pos_bg = (window_size[0]-img_bg.size[0])/2 * (paralax*((window_size[0] - mouse_x)/paralax_size)), (paralax_size-img_bg.size[1])/2 * (paralax*((window_size[1] - mouse_y)/paralax_size))

    img_canvas = img_bg.copy()
    img_whidth, img_height = img_fg.size
    img_canvas.paste(img_fg, (round(-pos_bg[0] + (canvas_size[0]-img_whidth)/2), round(-pos_bg[1]+ (canvas_size[1]-img_height)/2)))

    
    

    imgTk_canvas = ImageTk.PhotoImage(img_canvas)
    imgLabel_canvas.configure(image=imgTk_canvas)
    imgLabel_canvas.img_canvas = imgTk_canvas
    mouse_x, mouse_y = pyautogui.position()
    imgLabel_canvas.place(x=pos_bg[0],y=pos_bg[1])

    












#UI


NewNeko_Button = tkinter.Button(master = tk, text ="New NEKOOOO!", command = NewNeko)
NewNeko_Button.place(x=width-230, y=0)

if NSFWorNot == True:
    Checkbutton(master = tk, text="Lewd?", variable=LewdOrNot).place(x=width-230, y=30)

    Checkbutton(master = tk, text="Random?", variable=RandomOrNot).place(x=width-230, y=50)
else:
    Checkbutton(master = tk, text="Random?", variable=RandomOrNot).place(x=width-230, y=30)

SearchNeko_Button = tkinter.Button(master = tk, text ="Browse Neko", command = SearchNeko).place(x=width-230, y= 80)
inNekoNumber = Entry(master = tk)
inNekoNumber.place(x=width-140, y=83)
inNekoNumber.insert(0,0)

Checkbutton(master = tk, text="is this cute?", variable=LikeOrNot).place(x=width-230, y=130)

Checkbutton(master = tk, text="only cute?", variable=OnlyLike).place(x=width-230, y=150)

if NSFWorNot == True:
    SearchHentai_Button = tkinter.Button(master = tk, text ="Browse Hentai", command = SearchHentai).place(x=width-230, y= 300)
    inHentaiNumber = Entry(master = tk)
    inHentaiNumber.place(x=width-140, y=303)

    PrevHentai_Button = tkinter.Button(master = tk, text ="Prev. Page", command = PrevPage).place(x=width-230, y= 335)
    NextHentai_Button = tkinter.Button(master = tk, text ="Next Page", command = NextPage).place(x=width-150, y= 335)

    GoToPage_Button = tkinter.Button(master = tk, text ="Goto Page", command = GoToPage).place(x=width-230, y= 370)
    inPage = Entry(master = tk)
    inPage.place(x=width-140, y=373)










LoadNekos()
SearchNeko()
while run == True:    
    if load_new_pages == True:
        LoadPages()
        load_new_pages = False

    if load_new_nekos == True:
        LoadNekos()
        load_new_nekos = False

    if paralax != 0:
        UpdateImage()

    if keyboard.is_pressed('d') or keyboard.is_pressed('space') or keyboard.is_pressed('right'):
        NewNeko()
    
    
    tk.update_idletasks()
    tk.update()
'''
