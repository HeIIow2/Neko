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


global size
global liked_neko_cute


number_int = 0
total = 0
tupelList = 0

hentai_page = 1


neko_cute = (10, 12, 14, 15, 22, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 37, 38, 47, 48, 49, 51, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 111, 112, 113, 114, 183, 184, 187, 188, 189, 190, 191, 192, 193, 195, 196, 197, 198, 199, 203, 204, 205, 206, 207, 209, 211, 216, 218, 219, 220, 221, 222, 225, 226, 228, 229, 230, 231, 232, 233, 235, 236, 240, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 259, 260, 261, 263, 264, 265, 266, 267, 276, 278, 279, 280, 281, 283, 284, 285, 292, 293, 294, 295, 296, 320, 325, 343, 344, 399, 401)
neko_lewd = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 35, 36, 38, 39, 40, 41, 42, 43, 44, 46, 48, 49, 50, 51, 52, 53, 55, 57, 58, 63, 65, 66, 67, 69, 81, 84, 104, 106, 138, 140, 173, 175, 178, 181, 183, 185, 186, 187, 188, 189, 190, 191, 192, 216, 220, 221, 222, 223, 224, 226, 227, 228, 229, 231, 241, 251, 252, 254, 265, 281, 282, 283, 284, 285, 286, 287, 342, 349, 360, 361, 363, 364, 365, 366, 367, 368, 369, 370, 371, 389, 390, 391, 392, 393, 394, 397, 398, 400, 401, 404, 405, 406, 407, 408, 409, 410, 411, 412, 414, 418, 424, 426, 427, 428, 429, 430, 431, 433, 437, 439, 444, 448, 449, 450, 451, 452, 453, 454, 460, 464, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 479, 480, 482, 500, 501, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 530, 531, 532, 533, 542, 574, 575, 578, 579, 580, 582, 583, 586, 588, 591, 592, 594, 618, 619, 620, 621, 622, 623, 652, 653, 654, 655, 656, 657, 658, 659, 660, 661, 662, 663, 664, 665, 666, 667, 668, 669, 670, 671, 672, 673, 674, 675, 676, 677, 678, 679, 680, 681, 682, 683, 684, 685, 686, 687, 688, 689, 690, 691, 692, 693, 694, 695, 696, 697, 698, 699, 700, 701, 702, 703, 704, 705, 706, 707, 708, 709, 710, 711, 712, 713, 714, 715, 716, 717, 718, 719, 720, 721, 722, 723, 724, 725, 726, 727, 728, 729, 730, 731, 733, 734, 735, 736, 737, 738, 739, 740, 741, 742, 743, 744, 745, 747, 748, 749, 755, 757, 758, 760, 761, 762, 763, 766, 767, 768, 769, 770, 771, 772, 774, 775, 776, 777, 778, 779, 781, 782, 785, 786, 789, 792, 796, 797, 798, 800, 801, 802, 803, 804, 805, 806, 807, 808, 810, 837)




fav = open('these are cute.txt', 'r+')
allFav = fav.read()
splitFav = allFav.split('\n')
liked_nekos_cute = splitFav[0].split(', ')
liked_nekos_lewd = splitFav[1].split(', ')
print(splitFav)
fav.close()




width, height = pyautogui.size()
print(width)
print(height)




window = tkinter.Tk()

LewdOrNot = IntVar()
LikeOrNot = IntVar()
OnlyLike = IntVar()
RandomOrNot = IntVar()
imgLabel = tkinter.Label()

window.title('NEKOS!!!')

window.geometry(str(width) + "x" + str(height) + "+-8+0")

size = width-232, height-75


lewdNeko = 'https://cdn.nekos.life/lewd/lewd_neko'
cuteNeko = 'https://cdn.nekos.life/neko/neko'





def NewNeko():
    global number_int
    global tupelList
    
    try:
        CheckForLike(number_int)

        
        if LewdOrNot.get() == 1:
            if RandomOrNot.get() == 1:
                if OnlyLike.get() == 1:
                    tupelList = random.randint(0, len(liked_nekos_lewd) - 1)
                else:
                    tupelList = random.randint(0, len(neko_lewd) - 1)

                    
            else:
                tupelList = tupelList + 1
                if OnlyLike.get() == 1:                
                    if tupelList >= len(liked_nekos_lewd):
                        tupelList = 0
                else:
                    if tupelList >= len(neko_lewd):
                        tupelList = 0

                        
            if OnlyLike.get() == 1:
                number_int = liked_nekos_lewd[tupelList]
            else:
                number_int = neko_lewd[tupelList]         

            zero_filled_number = str(number_int).zfill(3)

            neko = Image.open(requests.get(lewdNeko + zero_filled_number + '.jpg', stream=True).raw)


            
        else:
            if RandomOrNot.get() == 1:
                if OnlyLike.get() == 1:
                    tupelList = random.randint(0, len(liked_nekos_cute) - 1)
                else:
                    tupelList = random.randint(0, len(neko_cute) - 1)
            else:
                tupelList = tupelList + 1
                if OnlyLike.get() == 1:  
                    if tupelList >= len(liked_nekos_cute):
                        tupelList = 0
                else:
                    if tupelList >= len(neko_cute):
                        tupelList = 0


            if OnlyLike.get() == 1:
                number_int = liked_nekos_cute[tupelList]
            else:
                number_int = neko_cute[tupelList]
            number_str = str(number_int)

            zero_filled_number = number_str.zfill(3)

            neko = Image.open(requests.get(cuteNeko + zero_filled_number + '.jpg', stream=True).raw)


        SetLike(str(number_int))
        
        ShowImage(neko)

        inNekoNumber.delete(0,END)
        inNekoNumber.insert(0,number_int)
    except:
        print(zero_filled_number)





def SearchNeko():
    global number_int
    global tupelList

    
    CheckForLike(number_int)
    
    number_int = inNekoNumber.get()
    SetLike(str(number_int))
    
    zero_filled_number = number_int.zfill(3)
    number_int = int(number_int)
    try:
        if LewdOrNot.get() == 1:
            tupelList = neko_lewd.index(number_int)
            neko = Image.open(requests.get(lewdNeko + zero_filled_number + '.jpg', stream=True).raw)
        else:
            tupelList = neko_cute.index(number_int)
            neko = Image.open(requests.get(cuteNeko + zero_filled_number + '.jpg', stream=True).raw)

        ShowImage(neko)
    except:
        print('This neko has something to do now :(')







def CheckForLike(nekoNumber):
    if LikeOrNot.get() == 1:
        if LewdOrNot.get() == 1:
            if str(nekoNumber) not in liked_nekos_lewd:
                liked_nekos_lewd.append(str(nekoNumber))             
        else:
            if str(nekoNumber) not in liked_nekos_cute:
                liked_nekos_cute.append(str(nekoNumber))
    else:
        if LewdOrNot.get() == 1:
            if str(nekoNumber) in liked_nekos_lewd:
                liked_nekos_lewd.remove(nekoNumber)
                        
        else:
            if str(nekoNumber) in liked_nekos_cute:
                liked_nekos_cute.remove(nekoNumber)
    LikeOrNot.set(0)






def SetLike(nekoNumber):
    if LewdOrNot.get() == 1:
        if str(nekoNumber) in liked_nekos_lewd:
            LikeOrNot.set(1)
        else:
            LikeOrNot.set(0)

    else:
        if str(nekoNumber) in liked_nekos_cute:
            LikeOrNot.set(1)
        else:
            LikeOrNot.set(0)



def on_closing():
    fav = open('these are cute.txt', 'w')
    fav.write(', '.join(liked_nekos_cute))
    fav.write('\n')
    fav.write(', '.join(liked_nekos_lewd))

    
    if messagebox.askokcancel(":3", "No more Neko cuties?"):
        window.destroy()
window.protocol("WM_DELETE_WINDOW", on_closing)




def SearchHentai():
    global hentai_page
    global imgURL
    
    hentai_page = 1

    
    hentaiNumber = inHentaiNumber.get()
    hentaiURL = 'https://nhentai.net/g/' + str(hentaiNumber) + '/1/'
    print(hentaiURL)    

    page = requests.get(hentaiURL)
    tree = html.fromstring(page.content)

    imgURLlist = tree.xpath('//*[@id="image-container"]/a/img/@src')
    imgURLstr = imgURLlist[0]
    imgURL = imgURLstr[:len(imgURLstr) - 5]
    
    hentai = Image.open(requests.get(imgURL + str(hentai_page) + '.jpg', stream=True).raw)

    ShowImage(hentai)

    inPage.delete(0,END)
    inPage.insert(0,hentai_page)




def PrevPage():
    global hentai_page
    global imgURL
    
    if hentai_page > 1:
        hentai_page = hentai_page - 1
    else:
        print("no Page bevore sorry :'(")
    
    hentai = Image.open(requests.get(imgURL + str(hentai_page) + '.jpg', stream=True).raw)

    ShowImage(hentai)

    inPage.delete(0,END)
    inPage.insert(0,hentai_page)



def NextPage():
    global hentai_page
    global imgURL
    
    hentai_page = hentai_page + 1

    try:
        hentai = Image.open(requests.get(imgURL + str(hentai_page) + '.jpg', stream=True).raw)
        ShowImage(hentai)
        
        inPage.delete(0,END)
        inPage.insert(0,hentai_page)
        
    except:
        hentai_page = hentai_page - 1

        


def GoToPage():
    global hentai_page
    global imgURL

    hentai_page = int(inPage.get())

    try:
        hentai = Image.open(requests.get(imgURL + str(hentai_page) + '.jpg', stream=True).raw)
        ShowImage(hentai)

        inPage.delete(0,END)
        inPage.insert(0,hentai_page)
        
    except:
        hentai_page = hentai_page - 1




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






NewNeko()


#267


#UI

NewNeko_Button = tkinter.Button(master = window, text ="New NEKOOOO!", command = NewNeko)
NewNeko_Button.place(x=width-230, y=0)

Checkbutton(master = window, text="Lewd?", variable=LewdOrNot).place(x=width-230, y=30)

Checkbutton(master = window, text="Random?", variable=RandomOrNot).place(x=width-230, y=50)

SearchNeko_Button = tkinter.Button(master = window, text ="Browse Neko", command = SearchNeko).place(x=width-230, y= 80)
inNekoNumber = Entry(master = window)
inNekoNumber.place(x=width-140, y=83)

Checkbutton(master = window, text="is this cute?", variable=LikeOrNot).place(x=width-230, y=130)

Checkbutton(master = window, text="only cute?", variable=OnlyLike).place(x=width-230, y=150)

SearchHentai_Button = tkinter.Button(master = window, text ="Browse Hentai", command = SearchHentai).place(x=width-230, y= 300)
inHentaiNumber = Entry(master = window)
inHentaiNumber.place(x=width-140, y=303)

PrevHentai_Button = tkinter.Button(master = window, text ="Prev. Page", command = PrevPage).place(x=width-230, y= 335)
NextHentai_Button = tkinter.Button(master = window, text ="Next Page", command = NextPage).place(x=width-150, y= 335)

GoToPage_Button = tkinter.Button(master = window, text ="Goto Page", command = GoToPage).place(x=width-230, y= 370)
inPage = Entry(master = window)
inPage.place(x=width-140, y=373)



mainloop()
