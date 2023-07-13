import sys
sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON\venv\Lib\site-packages")
sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON")

import time
import requests
from Bot_FRS_v2.BOT_TELEGRAM import BOT
from Bot_FRS_v2.INI import ini

# URL сайта, который нужно мониторить
url = 'https://kalina-malina.ru/'
url2 = 'https://lifemart.ru/ekb'
url3  = "https://sbermarket.ru/"
url4 = "https://eda.yandex.ru/kemerovo?shippingType=delivery"

# Ожидаемый контент или фразы на странице
expected_content = "8 (800) 700 81 21"

def check_website():
    try:
        # Записываем текущее время перед отправкой запроса
        start_time = time.time()
        # Отправка GET-запроса к сайту
        response = requests.get(url)
        # Записываем время, затраченное на получение ответа
        response_time = round(time.time() - start_time, 2)

        start_time = time.time()
        response2 = requests.get(url2)
        response_time2 = round(time.time() - start_time, 2)

        start_time = time.time()
        response3 = requests.get(url3)
        response_time3 = round(time.time() - start_time, 2)

        start_time = time.time()
        response4 = requests.get(url4)
        response_time4 = round(time.time() - start_time, 2)


        t = "✅"
        # Проверка статуса ответа
        if response.status_code == 200:
            r1 = f"✅ Сайт работает"
            if response_time>1.5:
                t = "❌"
            r2 = f"{t} Время ответа: {response_time} сек"
            r11 = f"Немного для сравнения"
            r12 = f" - Жизньмарт : {response_time2} сек"
            r13 = f" - sbermarket: {response_time3} сек"
            r14 = f" - eda.yandex: {response_time4} сек"
        else:
            r1 = f"❌ Не доступен: {response.status_code}"
            r2 = f"{t} Время ответа: {response_time} сек"
            r11 = f"Немного для сравнения"
            r12 = f" - Жизньмарт : {response_time2} сек"
            r13 = f" - sbermarket: {response_time3} сек"
            r14 = f" - eda.yandex: {response_time4} сек"


        # Проверка содержимого страницы
        if expected_content in response.text:
            r22 = f"✅ Найден номер - {expected_content}"
        else:
            r22 = f"❌ Не найден номер телефона"

        mes = f'<b>Проверка сайта kalina-malina.ru</b>\n' \
              f'{ini.dat_seychas} {ini.time_seychas}\n'\
              f'{r1}\n' \
              f'{r22}\n' \
              f'{r2}\n' \
              f'{r11}\n' \
              f'{r12}\n' \
              f'{r13}\n' \
              f'{r14}\n'


    except requests.ConnectionError:
        mes = f"отказ в подключении или нет интернета"
    BOT.BOT().bot_proverka_KM(mes=mes)

check_website()