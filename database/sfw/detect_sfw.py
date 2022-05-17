from nudenet import NudeClassifier, NudeDetector
import mysql.connector
import requests
import os

# initialize classifier (downloads the checkpoint file automatically the first time)
classifier = NudeClassifier()
detector = NudeDetector()
        




def write():
    global start
    with open("start", "w") as file_:
        file_.write(str(start))

# pip install mysql-connector-python

neko_db = mysql.connector.connect(
    host="localhost",
    user="Hellow2",
    password="1234",
    database="neko"
)
cursor = neko_db.cursor()


start=1
with open("start", "r") as file:
    start = int(file.read())
   
def log(msg): 
    print(msg)
    with open("log.log", "a") as log_:
        log_.write(msg + "\n")
        
def scan_img():
    global start
    nsfw_elements = [
        "EXPOSED_ANUS",
        "EXPOSED_ARMPITS",
        "COVERED_BELLY",
        "EXPOSED_BELLY",
        "COVERED_BUTTOCKS",
        "EXPOSED_BUTTOCKS",
        "FACE_F",
        "FACE_M",
        "COVERED_FEET",
        "EXPOSED_FEET",
        "COVERED_BREAST_F",
        "EXPOSED_BREAST_F",
        "COVERED_GENITALIA_F",
        "EXPOSED_GENITALIA_F",
        "EXPOSED_BREAST_M",
        "EXPOSED_GENITALIA_M"
    ]
    

    data = detector.detect('image.png')
    for elem in data:
        if elem['label'] == "EXPOSED_BELLY":
            log(str(start))


print("\n\n")

timeout = 10000
while True:
    sql = "SELECT * FROM image WHERE id=%s;"
    cursor.execute(sql, (start,))
    img_data = [ dict(line) for line in [zip([ column[0] for column in cursor.description], row) for row in cursor.fetchall()] ]
    if len(img_data) <= 0:
        continue
    # print(img_data)
    sql = "SELECT tag.name FROM tag \
			WHERE tag.id IN \
			(SELECT image_tag.tag_id FROM image_tag \
			WHERE image_tag.image_id=%s);"
    cursor.execute(sql, (start,))
    tags_ = [ dict(line) for line in [zip([ column[0] for column in cursor.description], row) for row in cursor.fetchall()] ]
    tags = [elem["name"] for elem in tags_]
    print(start)
    print(tags)
    response = requests.get(img_data[0]['url'])
    open("image.png", "wb").write(response.content)
    scan_img()
        
    
    print()
    start += 1
    write()
    if start > timeout:
        break
        