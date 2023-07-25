import json
import time
import pandas as pd
import requests
from tabulate import tabulate
import API_.__Cites as Gorod

pd.set_option("expand_frame_repr", False)
pd.set_option('display.max_colwidth', None)

def get_data_and_print_table(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # Проверяем, что данные не пусты
            if not data:
                print("Данные не найдены.")
                return
            # Формируем список заголовков из ключей первого элемента данных
            headers = list(data[0].keys())
            # Формируем таблицу
            table = [list(item.values()) for item in data]

            # Выводим таблицу
            print(tabulate(table, headers=headers, tablefmt='grid', numalign="center"))
            return data  # Возвращаем данные вместо таблицы
        else:
            print(f"Ошибка при выполнении запроса: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print("Ошибка при выполнении запроса:", e)

def zapros_2(i):
    # Пример использования функции для запроса списка категорий
    url_categories = f"https://admin.kalina-malina.ru/api/v1/stores/id={i}/"
    groups = get_data_and_print_table(url_categories)
    print(groups)
    # Преобразуем данные в DataFrame
    if groups:
        df = pd.DataFrame(groups)
        # Сохраняем DataFrame в файл Excel с заголовками
        df.to_excel(r"C:\Users\borsh\Desktop\Python\Полный список магазинов.xlsx", index=False)
def zapros_1(i):
    # Пример использования функции для запроса списка категорий
    url_categories = f"https://admin.kalina-malina.ru/api/v1/stores?city_id={i}"
    groups = get_data_and_print_table(url_categories)
    # Преобразуем данные в DataFrame
    if groups:
        df = pd.DataFrame(groups)
        # Сохраняем DataFrame в файл Excel с заголовками
        df.to_excel(r"C:\Users\borsh\Desktop\Python\Полный список магазинов.xlsx", index=False)



print("\n")
user_input = input("Введите код группы: ")
print("\n")
print("\n")
zapros_1(user_input)

print("\n")
user_input = input("Введите код группы: ")
print("\n")
print("\n")

zapros_2(user_input)