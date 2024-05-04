#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError

# JSON Schema для описания ожидаемой структуры данных
flight_schema = {
    "type": "object",
    "properties": {
        "название пункта назначения": {"type": "string"},
        "номер рейса": {"type": "string"},
        "тип самолета": {"type": "string"}
    },
    "required": ["название пункта назначения", "номер рейса", "тип самолета"]
}

def add_flight():
    destination = input("Введите название пункта назначения: ").strip()
    flight_number = input("Введите номер рейса: ").strip()
    aircraft_type = input("Введите тип самолета: ").strip()

    return {'название пункта назначения': str(destination),
            'номер рейса': str(flight_number),
            'тип самолета': str(aircraft_type)}

def print_flights(flights):
    line = '+-{}-+-{}-+-{}-+'.format(
        '-' * 30,
        '-' * 20,
        '-' * 15
    )
    print(line)
    print('| {:^30} | {:^20} | {:^15} |'.format(
        "Название пункта назначения",
        "Номер рейса",
        "Тип самолета"
    ))
    print(line)

    for flight in flights:
        print('| {:<30} | {:<20} | {:<15} |'.format(
            flight.get('название пункта назначения', ''),
            flight.get('номер рейса', ''),
            flight.get('тип самолета', '')
        ))

    print(line)

def search_flights_by_aircraft_type(flights_list):
    search_aircraft_type = input("Введите тип самолета для поиска: ")
    matching_flights = [flight for flight in flights_list if flight['тип самолета'] == search_aircraft_type]

    if matching_flights:
        print("\nРейсы, обслуживаемые самолетом типа {}: ".format(search_aircraft_type))
        print_flights(matching_flights)
    else:
        print(f"\nРейсов, обслуживаемых самолетом типа {search_aircraft_type}, не найдено.")

def save_to_json(filename, data):
    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_from_json(filename):
    try:
        with open(filename, 'r', encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def validate_flight():
    flight = add_flight()
    try:
        validate(instance=flight, schema=flight_schema)
        print("Введенные данные соответствуют схеме.")
    except ValidationError as e:
        print("Ошибка валидации: ", e)

def main():
    flights_list = load_from_json('flights.json')

    while True:
        print("Выберите действие:")
        print("1. Добавить рейс")
        print("2. Вывести список рейсов")
        print("3. Поиск рейсов по типу самолета")
        print("4. Проверить валидацию данных")
        print("5. Сохранить и выйти")

        choice = input("Введите номер действия: ")

        if choice == '1':
            flight = add_flight()
            try:
                validate(instance=flight, schema=flight_schema)
                flights_list.append(flight)
                flights_list.sort(key=lambda x: x['название пункта назначения'])
            except ValidationError as e:
                print("Ошибка валидации: ", e)

        elif choice == '2':
            print_flights(flights_list)

        elif choice == '3':
            search_flights_by_aircraft_type(flights_list)

        elif choice == '4':
            validate_flight()

        elif choice == '5':
            save_to_json('flights.json', flights_list)
            break

        else:
            print("Некорректный ввод. Пожалуйста, выберите действие из списка.")

if __name__ == '__main__':
    main()
