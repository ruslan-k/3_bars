import json
import re
from functools import partial
import sys


def load_data(filepath):
    try:
        with open(filepath, encoding='cp1251') as jsonfile:
            content = jsonfile.read()
            return json.loads(content)
    except FileNotFoundError:
        sys.exit("Неверный путь к файлу или имя файла")
    except json.decoder.JSONDecodeError:
        sys.exit("Файл не является файлов JSON")

def get_coordinates():
    longitude = latitude = None
    while not longitude or not latitude:
        try:
            if not longitude:
                longitude = float(input('Введите долготу: '))
            latitude = float(input('Введите широту: '))
        except ValueError:
            print('Неверные данные попробуйте еще раз')
    return longitude, latitude

def get_biggest_bar(data):
    bar = max(data, key=lambda seats: seats['SeatsCount'])
    return bar['Name'], bar['Address']


def get_smallest_bar(data):
    bar = min(data, key=lambda seats: seats['SeatsCount'])
    return bar['Name'], bar['Address']


def get_closest_bar(data, coordinates):
    json_coordinates = [bar['geoData']['coordinates'] for bar in data]
    closest_coord = min(json_coordinates, key=lambda c: (c[0]- coordinates[0])**2 + (c[1]-coordinates[1])**2)
    bar = list(filter(lambda x: x.get('geoData').get('coordinates') == closest_coord, data))[0]
    return bar['Name'], bar['Address']

if __name__ == '__main__':
    file_path = sys.argv[1]
    json_data = load_data(file_path)
    coordinates = get_coordinates()
    print("Cамый большой бар: ", get_biggest_bar(json_data))
    print("Cамый маленький бар: ", get_smallest_bar(json_data))
    print("Ближайший бар:", get_closest_bar(json_data, coordinates))