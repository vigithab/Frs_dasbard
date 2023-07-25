import json
import time
import pandas as pd
import requests
from tabulate import tabulate

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



url_cities = "https://admin.kalina-malina.ru/api/v1/cities"
sites = get_data_and_print_table(url_cities)

# Преобразуем данные в DataFrame
if sites:
    df = pd.DataFrame(sites)
    # Сохраняем DataFrame в файл Excel с заголовками
    df.to_excel(r"C:\Users\lebedevvv\Desktop\FRS\PYTHON\Bot_FRS_v2\Kalina_malina_sayt\Файлы\Полный городов.xlsx", index=False)