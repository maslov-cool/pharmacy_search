import sys
import requests
import os
from PIL import Image


# поиск долготы + широты
geocode = ' '.join(sys.argv[1:])
server_address = 'http://geocode-maps.yandex.ru/1.x/'
api_key = '8013b162-6b42-4997-9691-77b7074026e0'

# Выполняем запрос
response = requests.get(server_address, params={'apikey': api_key, 'geocode': geocode, 'format': 'json'})

if response:
    # Преобразуем ответ в json-объект
    json_response = response.json()

    # Получаем первый топоним из ответа геокодера.
    # Согласно описанию ответа, он находится по следующему пути:
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    lon, lat = toponym["Point"]["pos"].split()
else:
    print("Ошибка выполнения запроса:")
    print("Http статус:", response.status_code, "(", response.reason, ")")




# поиск долготы + широты аптеки

server_address = 'https://search-maps.yandex.ru/v1/'
api_key = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'
search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": ','.join([str(i) for i in [lon, lat]]),
    "type": "biz"
}
# Выполняем запрос
response = requests.get(server_address, params=search_params)

if response:
    # Преобразуем ответ в json-объект
    json_response = response.json()

    # Получаем первую найденную организацию.
    organization = json_response["features"][0]
    # Получаем координаты ответа.
    lon_a, lat_a = organization["geometry"]["coordinates"]
    print(f'Название:{organization["properties"]["CompanyMetaData"]["name"]}')
    print(f'Адрес:{organization["properties"]["CompanyMetaData"]["address"]}')
    print(f'Время работы:{organization["properties"]["CompanyMetaData"]["Hours"]['text']}')
    print(f'Расстояние:{((abs(float(lon) - lon_a) * 111.3) ** 2 + (abs(float(lat) - lat_a) * 111) ** 2)**0.5}км')
else:
    print("Ошибка выполнения запроса:")
    print("Http статус:", response.status_code, "(", response.reason, ")")




# работа с картами
api_server = "https://static-maps.yandex.ru/v1"
api_key = '99542a9f-3c5d-497e-8c46-c6a5d622268b'
params = {
    "ll": ",".join([lon, lat]),
    "apikey": api_key,
    'pt': ','.join([lon, lat, 'pm']) + 'a' + '~' + ','.join([str(lon_a), str(lat_a), 'pm']) + 'b'
}
response = requests.get(api_server, params=params)

if not response:
    print("Ошибка выполнения запроса:")
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

# Запишем полученное изображение в файл.
map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)
img = Image.open('map.png')
img.show()
os.remove(map_file)

