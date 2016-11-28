# coding: utf-8

import json
import re
from functools import partial
import sys


def load_data(filepath):
    with open(filepath, encoding='cp1251') as jsonfile:
        content = jsonfile.read()
        return json.loads(content)

def get_biggest_bar(data):
    bar = max(data, key=lambda seats: seats['SeatsCount'])
    return bar['Name'], bar['Address']


def get_smallest_bar(data):
    bar = min(data, key=lambda seats: seats['SeatsCount'])
    return bar['Name'], bar['Address']


def get_closest_bar(data, longitude, latitude):
    coordinates = [longitude, latitude]
    dist = lambda s, d: (s[0] - d[0]) ** 2 + (s[1] - d[1]) ** 2
    json_coordinates = [bar['geoData']['coordinates'] for bar in data]
    nearest_coordinates = min(json_coordinates, key=partial(dist, coordinates))
    bar = list(filter(lambda bar: bar['geoData']['coordinates'] == nearest_coordinates, data))[0]
    return bar['Name'], bar['Address']

if __name__ == '__main__':
    coordinates = input("Введите ваши координаты через запятую, вида 'долгота, широта': ")
    while not re.match('^(\-?\d+(\.\d+)?),\s*(\-?\d+(\.\d+)?)$', coordinates):
        coordinates = input("Неверный ввод. Введите ваши координаты через запятую, вида 'широта, долгота': ")
    longitude, latitude,  = [float(coordinate.strip()) for coordinate in coordinates.split(",")]

    filepath = sys.argv[1]
    json_data = load_data(filepath)

    print("Cамый большой бар: ", get_biggest_bar(json_data))
    print("Cамый маленький бар: ", get_smallest_bar(json_data))
    print("Ближайший бар:", get_closest_bar(json_data, longitude, latitude))