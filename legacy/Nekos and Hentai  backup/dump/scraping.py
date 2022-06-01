import requests
from bs4 import BeautifulSoup
import time
urls = []



for i in range(6):
    URL = 'https://rule34.xxx/index.php?page=post&s=list&tags=tiffy&pid='+str((i+1)*42)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    tiffy_id_container = soup.findAll(class_='thumb')

    for element in tiffy_id_container:
        urls.append('https://rule34.xxx/index.php?page=post&s=view&id='+str(element.get('id')).replace('s', ''))
        # print(element)
    time.sleep(1)

print(urls)
print(len(urls))
img_links = []

for url in urls:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    tiffy_id_container = soup.find(id='image')
    img_link = tiffy_id_container.get('src')
    print(img_link)
    img_links.append(img_link)

    
print(img_links)


with open('tiffy_links', 'w') as file:
    for element in img_links:
        file.write(element + '\n')