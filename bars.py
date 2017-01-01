import json
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
    try:
        longitude = float(input('Введите долготу: '))
        latitude = float(input('Введите широту: '))
    except ValueError:
        sys.exit('Неверный тип данных при вводе или пустой ввод, попробуйте снова.')
    return longitude, latitude


def get_biggest_bar(data):
    bar = max(data, key=lambda seats: seats['SeatsCount'])
    return bar['Name'], bar['Address']


def get_smallest_bar(data):
    bar = min(data, key=lambda seats: seats['SeatsCount'])
    return bar['Name'], bar['Address']


def get_closest_bar(data, coordinates):
    closest_bar = min(data, key=lambda c: (c['geoData']['coordinates'][0] - coordinates[0]) ** 2 + (c['geoData']['coordinates'][1] - coordinates[1]) ** 2)
    return closest_bar['Name'], closest_bar['Address']


if __name__ == '__main__':
    file_path = sys.argv[1]
    json_data = load_data(file_path)
    coordinates = get_coordinates()
    print("Cамый большой бар: ", get_biggest_bar(json_data))
    print("Cамый маленький бар: ", get_smallest_bar(json_data))
    print("Ближайший бар:", get_closest_bar(json_data, coordinates))
