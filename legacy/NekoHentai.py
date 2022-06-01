import tkinter 
from tkinter import *
from tkinter import messagebox

import time
import pyautogui

from PIL import ImageTk, Image
import requests
import random

from urllib.request import Request, urlopen
from lxml import html, etree
from io import StringIO




neko_tag = 0
total = 0
neko_index = [0, 0]

hentai_page = 1
load_new_pages = False
load_new_nekos = False
run = True
neko_mode = True




fav = open('these are cute.txt', 'r+')
allFav = fav.read()
splitFav = allFav.split('\n')
neko_list_cute_liked = splitFav[0].split(', ')
neko_list_lewd_liked = splitFav[1].split(', ')
fav.close()


conf = open('config.txt', 'r')
EndMessageOrNot_str = conf.readline()
if 'True' in EndMessageOrNot_str:
    EndMessageOrNot = True
else:
    EndMessageOrNot = False
    if not 'False' in EndMessageOrNot_str:
        print("Config Error: Can't Find bool in Line 1 (Maybe check the capital letter)")
print(EndMessageOrNot)
conf.close()







neko_tuple_cute_all = (10, 12, 14, 15, 22, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 37, 38, 47, 48, 49, 51, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 111, 112, 113, 114, 183, 184, 187, 188, 189, 190, 191, 192, 193, 195, 196, 197, 198, 199, 203, 204, 205, 206, 207, 209, 211, 216, 218, 219, 220, 221, 222, 225, 226, 228, 229, 230, 231, 232, 233, 235, 236, 240, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 259, 260, 261, 263, 264, 265, 266, 267, 276, 278, 279, 280, 281, 283, 284, 285, 292, 293, 294, 295, 296, 320, 325, 343, 344, 399, 401)
neko_tuple_lewd_all = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 35, 36, 38, 39, 40, 41, 42, 43, 44, 46, 48, 49, 50, 51, 52, 53, 55, 57, 58, 63, 65, 66, 67, 69, 81, 84, 104, 106, 138, 140, 173, 175, 178, 181, 183, 185, 186, 187, 188, 189, 190, 191, 192, 216, 220, 221, 222, 223, 224, 226, 227, 228, 229, 231, 241, 251, 252, 254, 265, 281, 282, 283, 284, 285, 286, 287, 342, 349, 360, 361, 363, 364, 365, 366, 367, 368, 369, 370, 371, 389, 390, 391, 392, 393, 394, 397, 398, 400, 401, 404, 405, 406, 407, 408, 409, 410, 411, 412, 414, 418, 424, 426, 427, 428, 429, 430, 431, 433, 437, 439, 444, 448, 449, 450, 451, 452, 453, 454, 460, 464, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 479, 480, 482, 500, 501, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 530, 531, 532, 533, 542, 574, 575, 578, 579, 580, 582, 583, 586, 588, 591, 592, 594, 618, 619, 620, 621, 622, 623, 652, 653, 654, 655, 656, 657, 658, 659, 660, 661, 662, 663, 664, 665, 666, 667, 668, 669, 670, 671, 672, 673, 674, 675, 676, 677, 678, 679, 680, 681, 682, 683, 684, 685, 686, 687, 688, 689, 690, 691, 692, 693, 694, 695, 696, 697, 698, 699, 700, 701, 702, 703, 704, 705, 706, 707, 708, 709, 710, 711, 712, 713, 714, 715, 716, 717, 718, 719, 720, 721, 722, 723, 724, 725, 726, 727, 728, 729, 730, 731, 733, 734, 735, 736, 737, 738, 739, 740, 741, 742, 743, 744, 745, 747, 748, 749, 755, 757, 758, 760, 761, 762, 763, 766, 767, 768, 769, 770, 771, 772, 774, 775, 776, 777, 778, 779, 781, 782, 785, 786, 789, 792, 796, 797, 798, 800, 801, 802, 803, 804, 805, 806, 807, 808, 810, 837)

neko_tuple_cute = neko_tuple_cute_all, tuple(neko_list_cute_liked)
neko_tuple_lewd = neko_tuple_lewd_all, tuple(neko_list_lewd_liked)

neko_tuple = neko_tuple_cute, neko_tuple_lewd









width, height = pyautogui.size()




tk = Tk()

LewdOrNot = IntVar()
LikeOrNot = IntVar()
OnlyLike = IntVar()
RandomOrNot = IntVar()
imgLabel = tkinter.Label()

tk.title('NEKOS!!!')

tk.geometry(str(width) + "x" + str(height) + "+-8+0")

size = width-232, height-75

neko_url = 'https://cdn.nekos.life/neko/neko', 'https://cdn.nekos.life/lewd/lewd_neko'





def NewNeko():
    global load_new_nekos
    global neko_tag
    global new_neko_tag
    global neko_index
    global next_neko_index
    global settings
    global neko

    

    new_settings = [LewdOrNot.get(), RandomOrNot.get(), OnlyLike.get()]

    if settings != new_settings:
        LoadNekos()
        
    ShowImage(neko)
    inNekoNumber.delete(0,END)
    inNekoNumber.insert(0,new_neko_tag)
    CheckForLike(neko_tag)
    SetLike(new_neko_tag)
    neko_index = next_neko_index

    neko_tag = new_neko_tag
    load_new_nekos = True
      
        
        







def SearchNeko():
    global load_new_nekos
    global neko_tag
    
    settings = [LewdOrNot.get(), RandomOrNot.get(), OnlyLike.get()]
    CheckForLike(neko_tag)

    neko_tag = inNekoNumber.get()

    SetLike(neko_tag)

    neko_tag_zero_filled = str(neko_tag).zfill(3)

    print(neko_url[settings[0]] + neko_tag_zero_filled + '.jpg')
    neko = Image.open(requests.get(neko_url[settings[0]] + neko_tag_zero_filled + '.jpg', stream=True).raw)

    ShowImage(neko)

    neko_index = next_neko_index
    neko_tag = new_neko_tag
    load_new_nekos = True
    




def LoadNekos():
    global neko_index
    global next_neko_index
    global neko_tuple
    global settings
    global neko
    global new_neko_tag

    next_neko_index = neko_index
    settings = [LewdOrNot.get(), RandomOrNot.get(), OnlyLike.get()]

    if settings[1] == 0:
        next_neko_index[settings[0]] += 1
        if next_neko_index[settings[0]] >= len(neko_tuple [settings[0]] [settings[2]]):
            next_neko_index[settings[0]] = 0
        
    else:
        next_neko_index[settings[0]] = random.randint(0, len(neko_tuple [settings[0]] [settings[2]]) - 1)
        

    new_neko_tag = neko_tuple [settings[0]] [settings[2]][next_neko_index[settings[0]]]
    neko_tag_zero_filled = str(new_neko_tag).zfill(3)

    print(neko_url[settings[0]] + neko_tag_zero_filled + '.jpg')
    neko = Image.open(requests.get(neko_url[settings[0]] + neko_tag_zero_filled + '.jpg', stream=True).raw)

    neko_mode = True
   







def CheckForLike(nekoNumber):
    if LikeOrNot.get() == 1:
        if LewdOrNot.get() == 1:
            if str(nekoNumber) not in neko_list_lewd_liked:
                neko_list_lewd_liked.append(str(nekoNumber))             
        else:
            if str(nekoNumber) not in neko_list_cute_liked:
                neko_list_cute_liked.append(str(nekoNumber))
    else:
        if LewdOrNot.get() == 1:
            if str(nekoNumber) in neko_list_lewd_liked:
                neko_list_lewd_liked.remove(nekoNumber)
                        
        else:
            if str(nekoNumber) in neko_list_cute_liked:
                neko_list_cute_liked.remove(nekoNumber)
    LikeOrNot.set(0)






def SetLike(nekoNumber):
    if LewdOrNot.get() == 1:
        if str(nekoNumber) in neko_list_lewd_liked:
            LikeOrNot.set(1)
        else:
            LikeOrNot.set(0)

    else:
        if str(nekoNumber) in neko_list_cute_liked:
            LikeOrNot.set(1)
        else:
            LikeOrNot.set(0)



def on_closing():
    global run
    global neko_mode
    global EndMessageOrNot
    
    
    fav = open('these are cute.txt', 'w')
    fav.write(', '.join(sorted(neko_list_cute_liked)))
    fav.write('\n')
    fav.write(', '.join(sorted(neko_list_lewd_liked)))
    
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
    



    

def ShowImage(img):
    img_whidth, img_height = img.size

    if img_whidth/size[0] > img_height/size[1]:
        count = img_whidth/size[0]
        img_height = img_height/count
        img_whidth = size[0]
    else:
        count = img_height/size[1]
        img_whidth = img_whidth/count
        img_height = size[1]


    img_size = round(img_whidth), round(img_height)
    
    img_resized = img.resize(img_size)
 
    imgTk = ImageTk.PhotoImage(img_resized)
    imgLabel.configure(image=imgTk)
    imgLabel.img = imgTk
    imgLabel.place(x=(size[0]-img_whidth)/2, y=(size[1]-img_height)/2)






#UI

NewNeko_Button = tkinter.Button(master = tk, text ="New NEKOOOO!", command = NewNeko)
NewNeko_Button.place(x=width-230, y=0)

Checkbutton(master = tk, text="Lewd?", variable=LewdOrNot).place(x=width-230, y=30)

Checkbutton(master = tk, text="Random?", variable=RandomOrNot).place(x=width-230, y=50)

SearchNeko_Button = tkinter.Button(master = tk, text ="Browse Neko", command = SearchNeko).place(x=width-230, y= 80)
inNekoNumber = Entry(master = tk)
inNekoNumber.place(x=width-140, y=83)

Checkbutton(master = tk, text="is this cute?", variable=LikeOrNot).place(x=width-230, y=130)

Checkbutton(master = tk, text="only cute?", variable=OnlyLike).place(x=width-230, y=150)

SearchHentai_Button = tkinter.Button(master = tk, text ="Browse Hentai", command = SearchHentai).place(x=width-230, y= 300)
inHentaiNumber = Entry(master = tk)
inHentaiNumber.place(x=width-140, y=303)

PrevHentai_Button = tkinter.Button(master = tk, text ="Prev. Page", command = PrevPage).place(x=width-230, y= 335)
NextHentai_Button = tkinter.Button(master = tk, text ="Next Page", command = NextPage).place(x=width-150, y= 335)

GoToPage_Button = tkinter.Button(master = tk, text ="Goto Page", command = GoToPage).place(x=width-230, y= 370)
inPage = Entry(master = tk)
inPage.place(x=width-140, y=373)




LoadNekos()
NewNeko()
while run == True:    
    if load_new_pages == True:
        LoadPages()
        load_new_pages = False

    if load_new_nekos == True:
        LoadNekos()
        load_new_nekos = False
        
    
    tk.update_idletasks()
    tk.update()
