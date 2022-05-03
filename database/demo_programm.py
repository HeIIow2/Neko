import mysql.connector
import requests
import os

SFW = True

# pip install mysql-connector-python

neko_db = mysql.connector.connect(
    host="localhost",
    user="Hellow2",
    password="1234",
    database="neko"
)
cursor = neko_db.cursor()

"""
SELECT 
	(SELECT tag.name FROM tag WHERE tag.id=image_tag.tag_id) AS tag, 
	COUNT(DISTINCT image_id) AS frequency 
FROM image_tag
GROUP BY tag_id;

SELECT image_id FROM image_tag 
WHERE tag_id=(SELECT id FROM tag WHERE name='belly free');

SELECT image.id, image.url FROM image
WHERE image.id IN (
    SELECT image_id FROM image_tag 
	WHERE tag_id=
    (SELECT id FROM tag WHERE name='belly free')
);

SELECT tag.name FROM tag 
WHERE tag.id IN 
(SELECT image_tag.tag_id FROM image_tag
WHERE image_tag.image_id=19660);
"""


def output_tags():
    print("------------tags------------")
    cursor.execute("""
    SELECT 
        (SELECT tag.name FROM tag WHERE tag.id=image_tag.tag_id) AS tag, 
        COUNT(DISTINCT image_id) AS frequency 
    FROM image_tag
    GROUP BY tag_id;
    """)
    for row in cursor:
        print("tag:", row[0], "frequency:", row[1])

    print("----------------------------")


def fetch_image_ids(tag_name):
    if SFW:
        sql = """
        SELECT image.id FROM image
        WHERE image.id IN (
        SELECT image_id FROM image_tag 
	        WHERE tag_id=
            (SELECT id FROM tag WHERE name=%s AND sfw=TRUE)
        );
        """
    else:
        sql = """
        SELECT image.id FROM image
        WHERE image.id IN (
        SELECT image_id FROM image_tag 
	        WHERE tag_id=
            (SELECT id FROM tag WHERE name=%s)
        );
        """
    cursor.execute(sql, (tag_name,))
    return [row[0] for row in cursor]

def get_image_tags(image_id):
    cursor.execute("""
            SELECT tag.name FROM tag 
            WHERE tag.id IN 
            (SELECT image_tag.tag_id FROM image_tag
            WHERE image_tag.image_id=%s);
            """, (image_id,))
    return [row[0] for row in cursor]

def get_image_url(image_id):
    cursor.execute("""
            SELECT image.url FROM image 
            WHERE image.id=%s;
            """, (image_id,))
    return cursor.fetchone()[0]

def download_image(image_id):
    global tag_name
    url = get_image_url(image_id)
    response = requests.get(url)
    open(f"./images/{tag_name}/{image_id}.png", "wb").write(response.content)


output_tags()
tag_name = input("download tag: ")
print("----------------------------")
current_ids = fetch_image_ids(tag_name)
tag_name = tag_name.replace(" ", "_")
print(f"length of tag: {len(current_ids)}")

exit()
print(current_ids)
if not os.path.exists(f"./images/{tag_name}"):
    os.makedirs(f"./images/{tag_name}")
for id in current_ids:
    print(get_image_tags(id), get_image_url(id), id, sep="; ")
    download_image(id)
