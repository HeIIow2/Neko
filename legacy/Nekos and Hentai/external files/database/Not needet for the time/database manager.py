import tkinter
from tkinter import *
from PIL import ImageTk
from PIL import Image

import keyboard
import time

import os, sys

run = True
clock_intervall = 1
prev_time = 0.0

path = 'images not sorted'
path_save = 'images/'

tags = 'neko', 'lewd', 'cute', 'loli', 'girl', 'boy', 'fox', 'bdsm', 'tiffy', 'emo', 'epic'
keybinds = 'b', 'a', 'd', 'w', 'h', 'j', 'k', 'l', 'ö', 'x', 'ä'
unknown_key = 's'




dirs = os.listdir(path)

paths = []
for file in dirs:
   paths.append(file)

print(paths)

root = Tk()
root.title('NEKOS!!!')
root.geometry(str(1000) + "x" + str(1000) + "+-8+0")





unknown = IntVar()

for tag in tags:
   globals()[tag] = IntVar()


start = 503
img_number = 0

label = tkinter.Label()




img = Image.open(path + '/' + paths[img_number])
img_orig = img
img.thumbnail((1000,1000))
imgTk = ImageTk.PhotoImage(img)
label.configure(image=imgTk)
label.img = imgTk
label.place(x=0, y=0)



def NextImg():
   global img_number
   global path_save
   global img_orig
   global start

   with open('table', 'a+') as table:
      table.write(str(img_number + start).zfill(4) + ';')
      if unknown.get() == False:
         nekoSource = inNekoSource.get()
      else:
         nekoSource = 'unknown'
      table.write(' ' + nekoSource + '; (')


      for tag in tags:
         globals()[tag + '_active'] = globals()[tag].get()
         if globals()[tag + '_active'] == True:
            table.write(tag + ', ')
      table.write(')')

      
      table.write('\n')

   img_orig.save(path_save + str(img_number + start).zfill(4) + '.png')




   img_number += 1

   img = Image.open(path + '/' + paths[img_number])
   img_orig = img
   img.thumbnail((1000,1000))
   imgTk = ImageTk.PhotoImage(img)
   label.configure(image=imgTk)
   label.img = imgTk
   label.place(x=0, y=0)

   








def on_closing():   #stops the loop if tk is closed
    global run
    run = False
    root.destroy()
root.protocol("WM_DELETE_WINDOW", on_closing)




    
NewNeko_Button = tkinter.Button(master = root, text ="New NEKOOOO!", command = NextImg)
NewNeko_Button.place(x=900, y=0)

inNekoSource = Entry(master = root)
inNekoSource.place(x=900, y=30)
inNekoSource.insert(INSERT, 'https://nekos.life/')

Checkbutton(master = root, text="unknown source?", variable=unknown).place(x=900, y=60)

ypos = 60
for i in range(len(tags)):
   tag = tags[i]
   ypos += 20
   Checkbutton(master = root, text=tag + ' ' + keybinds[i], variable=globals()[tag]).place(x=900, y=ypos)




def UpdateKey():
   for key in keybinds:
      if keyboard.is_pressed(key):
         index = keybinds.index(key)
         if globals()[tags[index]].get() == 0:
            globals()[tags[index]].set(1)
         else:
            globals()[tags[index]].set(0)
         time.sleep(0.2)
         break;
   if keyboard.is_pressed(unknown_key):
      if unknown.get() == 0:
         unknown.set(1)
      else:
         unknown.set(0)
      time.sleep(0.2)
   

   

while run == True: 
   current_time = time.time()
   if keyboard.is_pressed('space') and current_time - prev_time >= clock_intervall:
         NextImg()  
         prev_time = current_time
        
        
   UpdateKey()
   root.update_idletasks()   
   root.update()

