
import sys
sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON\venv\Lib\site-packages")
sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON")
import datetime
import shutil
import pandas as pd
import schedule
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
class recwest():
    def __init__(self):
        self.response = None

    def check_website(self):
        global mes
        try:
            # Записываем текущее время перед отправкой запроса
            start_time = time.time()
            # Отправка GET-запроса к сайту
            self.response = requests.get(url)
            # Записываем время, затраченное на получение ответа
            self.response_time = round(time.time() - start_time, 2)
            t = "✅"
            # Проверка статуса ответа
            if self.response.status_code == 200:
                r1 = f"✅ Сайт работает"
                if self.response_time > 3:
                    t = "❌"
                r2 = f"{t} Время ответа: {self.response_time} сек"
            else:
                if self.response_time > 3:
                    t = "❌"
                r1 = f"❌ Не доступен: {self.response.status_code}"
                r2 = f"{t} Время ответа: {self.response_time} сек"

            # Проверка содержимого страницы
            if expected_content in self.response.text:
                r22 = f"✅ Найден номер - {expected_content}"
            else:
                r22 = f"❌ Не найден номер телефона"
            mes = f'<b>Проверка сайта kalina-malina.ru</b>\n' \
                  f'{ini.dat_seychas} {ini.time_seychas}\n'\
                  f'{r1}\n' \
                  f'{r22}\n' \
                  f'{r2}\n'
        except requests.ConnectionError:
            mes = f"отказ в подключении или нет интернета"
        finally:
            path = r"C:\Users\lebedevvv\Desktop\FRS\PYTHON\Bot_FRS_v2\LOGI"

            data = {
                'Дата': [ini.dat_seychas],
                'Время': [ini.time_seychas],
                'Страница': [url],
                'Метод': ['get'],
                'Код ответа': [self.response.status_code],
                'Время ответа': [self.response_time]
            }

            # Create a tab-separated string for the current row
            row_data = "\t".join([str(value[0]) for value in data.values()]) + "\n"

            # Write the row to the file
            with open(path + "\Log_site.txt", 'a', encoding="utf-8") as file:
                file.write(row_data)


        #self.response.status_code = 202
        if self.response.status_code != 200:
            current_time = datetime.datetime.now().time()
            if current_time.hour != 0 and current_time.minute != 0:
                print(mes)
                BOT.BOT().bot_proverka_KM(mes=mes)
                return

        if self.response_time > 10:
            current_time = datetime.datetime.now().time()
            if current_time.hour != 0 and current_time.minute != 0:
                mes = f"✅❌ Работает, время ответа: {self.response_time}"
                print(mes)
                BOT.BOT().bot_proverka_KM(mes=mes)
        return

recwest().check_website()
"""while True:
    current_time = datetime.datetime.now().time()
    print(current_time)
    if current_time.hour == 0 and current_time.minute == 0:
        check_website()
    # Ожидание до следующей минуты
    time.sleep(60 - current_time.second)"""