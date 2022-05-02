import mysql.connector
import json

# !!!! DONT TOUCH DELETES EVERYTHING !!!!
"""
DELETE FROM image;
DELETE FROM tag;
DELETE FROM image_tag;
"""

neko_db = mysql.connector.connect(
    host="localhost",
    user="Hellow2",
    password="1234",
    database="neko"
)

print(neko_db)

cursor = neko_db.cursor()

with open("data/table.json", "r") as f:
    data = json.load(f)

created_tags = []
tag_id = {}

created_images = []

cursor.execute("SELECT id FROM tag")
results = cursor.fetchall()
print(results)
if len(results) > 0:
  cursor.execute("DELETE FROM image;")
  cursor.execute("DELETE FROM tag;")
  cursor.execute("DELETE FROM image_tag;")


def get_tag_id(tag: str):
    global created_tags
    global tag_id

    if tag in created_tags:
        return tag_id[tag]

    cursor.execute(f"SELECT id FROM tag WHERE name='{tag}'")
    results = cursor.fetchall()
    if len(results) == 0:
        sql = "INSERT INTO tag (name) VALUES (%s)"
        cursor.execute(sql, (tag,))
        neko_db.commit()
        cursor.execute(f"SELECT id FROM tag WHERE name='{tag}'")
        results = cursor.fetchall()
        if not len(results):
            raise Exception("something went wrong")
        created_tags.append(tag)
        tag_id[tag] = results[0][0]
        return tag_id[tag]
    else:
        tag_id[tag] = results[0][0]
        return tag_id[tag]


def get_image_id(url: str, translation: str):
    if url in created_images:
        return -1

    if translation == "":
        sql = "INSERT INTO image (url) VALUES (%s)"
        cursor.execute(sql, (url,))
    else:
        sql = "INSERT INTO image (url, translation ) VALUES (%s, %s)"
        try:
            cursor.execute(sql, (url, "\n".join(translation)))
        except Exception as e:
            print(url)
            print(translation)
            print("\n".join(translation))
            print(e)
    neko_db.commit()
    cursor.execute(f"SELECT id FROM image WHERE url='{url}'")
    results = cursor.fetchall()
    if not len(results):
        raise Exception("something went wrong")
    created_images.append(url)
    return results[0][0]


def write_element(url: str, tags: list, translation: str):
    global created_tags

    image_id = get_image_id(url, translation)
    if image_id == -1:
        print(f"{url} already exists. Skipping...")
        print(f"{tags}")
        return

    sql = "INSERT INTO image_tag (tag_id, image_id) VALUES (%s, %s)"
    val = [
    ]
    for tag in tags:
        tag_id = get_tag_id(tag)
        val.append((tag_id, image_id))

    cursor.executemany(sql, val)
    neko_db.commit()


for key in data:
    element = data[key]
    url = element["url"]
    tags = element["tags"]
    translation = ""
    if "translation" in element:
        translation = element["translation"]

    write_element(url, tags, translation)
