import requests
import time
from PIL import Image
import os

path_orig = 'database/images not sorted/'

start = 559



def rename():
    for i in range(330):
        os.rename(path_orig + str(i).zfill(4) + '.png', path_orig + str(i+start).zfill(4) + '.png')



def write_table():
    global start
    source = 'rule34'

    with open('tabel_tiffy', 'w') as file:
        for i in range(201):
            file.write(str(i + start).zfill(4) + '; ' + source + '; (neko, lewd, girl, tiffy' + ', )\n')




def download():
    with open('tiffy_links', 'r') as NekoLewd:
        for i in range(330):
            neko_lewd = NekoLewd.readline()
            neko_lewd = neko_lewd.rstrip('\n')
            print(neko_lewd)
            suffix = '.png'
            print(suffix)
            path = path_orig + str(i).zfill(4)
            print(path)

            img = Image.open(requests.get(neko_lewd, stream=True).raw)
            img.save(path + suffix)

            time.sleep(0.2)

write_table()