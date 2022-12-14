import time

import requests
from bs4 import BeautifulSoup
import datetime


headers={'accept': '*/*', 'user-agent': 'add_the_info'}
url='https://www.gismeteo.ru/'

res=requests.get(url, headers=headers)
page=res.text
with open(r'D:\1\pycharm project\parser_gismeteo\page_gismeteo.html', 'w', encoding='utf-8') as w:
    w.write(page)

with open(r'D:\1\pycharm project\parser_gismeteo\page_gismeteo.html', 'r', encoding='utf-8') as r:
    lead_page=r.read()

soup=BeautifulSoup(lead_page, 'lxml')
data=soup.find(class_='cities-popular').find_all('div', class_="list-item")

urls=[]
for i in data:
    url=i.find('a').get('href')
    urls.append(url)

temp_dict={}
count=0
for item in urls:
    responce_item=requests.get('https://www.gismeteo.ru/'+item, headers=headers)
    soup_item=BeautifulSoup(responce_item.text, 'lxml')
    city_name=soup_item.find('div', class_='page-title').find('h1').text
    temp=soup_item.find('span', class_='unit unit_temperature_c').text
    temp_dict[city_name]=temp
    time.sleep(2)
    count+=1
    if count<=5:
        print(f'Идет процесс сбора информации о городе № {count}')
    else:
        print('Процесс завершен')
        break


for city, temp in temp_dict.items():
    print(city, temp)





























