# Краткое описание: парсинг сайта с интересными событиями в Москве и последующий импорт полученных данных в ексель файл.

import requests
from bs4 import BeautifulSoup
import openpyxl

headers={'accept': '', 'user-agent': ''}#добавление юзер агента

url='https://kudago.com/msk/exhibitions/?date=2022-10-16-2022-10-25'
res=requests.get(url, headers=headers) #получени html кода страницы
page=res.text
with open('kudago_page.html', 'w', encoding='utf-8') as f:
    f.write(page) #скачивание HTML кода страницы

with open('kudago_page.html', encoding='utf-8') as file:
    src=file.read()

soup=BeautifulSoup(src, 'lxml') #преобразование кода страницы
data=soup.find_all(class_='post-content') #нахождение всех классов с карточками событий

urls=[]
for item in data[0:10]:
    address=item.find('a').get('href')
    urls.append(address) #добавление url адреса каждого события в список для последующего перебора

book=openpyxl.Workbook() #создание файла excel
page=book.active
#названия сталбцов
page['A1']="name_event"
page['B1']="short_info"
page['C1']="url_address"
page['D1']="age"
page['E1']="event_date"
page['F1']="event_time"
page['G1']="streets"
page['H1']="metro_station"
page['I1']="price_ticket, RUP"
page['J1']="type_show"
row=2
#проход циклом по ссылке каждого события и нахождение нужных данных о событиях
for value in urls[0:10]:
    response=requests.get(value, headers=headers)
    soup_urls=BeautifulSoup(response.text, 'lxml')
    name_event=soup_urls.find('h1', class_='post-big-title').text.strip()
    page[f'A{row}'] = name_event
    short_info=soup_urls.find('div', class_='post-big-tagline').find('p').text.strip()
    page[f'B{row}'] = short_info
    url_address=value
    page[f'C{row}']=url_address
    age=soup_urls.find('span', class_='age-restriction').text.strip()
    page[f'D{row}']=age
    event_date=soup_urls.find('td', class_='post-schedule-container').text.strip()
    page[f'E{row}']=str(event_date)
    event_time=soup_urls.find('td', class_='').text.split()[-1]
    page[f'F{row}']=event_time
    streets=soup_urls.find('span', class_='addressItem addressItem--single').text.strip()
    page[f'G{row}']=streets
    try:
        metro_station=soup_urls.find('span', class_='post-detail-text').text.strip()
        page[f'H{row}']=metro_station
    except AttributeError:
        page[f'H{row}'] = 'Станция метро не указана'
    price_ticket=soup_urls.find('div', 'two-columns waterfall').find('span').text.strip()
    page[f'I{row}']=price_ticket
    demo_type_show=soup_urls.find('div', 'two-columns waterfall').find_all('li')
    type_show=''
    for t in demo_type_show:
        type_show+=t.text+', '
    page[f'J{row}']=type_show[0:-2]
    row+=1

book.save('kudago.xlsx')
book.close()
if book.close:
    print('Книга закрыта')
else:
    print('Произошла ошибка при закрытии книги')
















































































