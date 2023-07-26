import sys
sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON\venv\Lib\site-packages")
sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON")

import holidays
import timeit
from datetime import datetime, timedelta, time, date
import pandas as pd
import requests
import json
from Bot_FRS_v2.INI import ini


pd.set_option("expand_frame_repr", False)
pd.set_option('display.max_colwidth', None)

TY_GROP =  ini.TY_GROP
TEST_BOT = ini.TEST_BOT
PUT = ini.PUT

class CustomRusHolidays(holidays.RU):
    def _populate(self, year,):
        super()._populate(year)
        # Добавляем в наш пользовательский набор праздников все официальные выходные дни.
        self[date(year, 5, 6)] = "День Воинской славы России"
        self[date(year, 5, 7)] = "День Воинской славы России"
        self[date(year, 5, 8)] = "День Победы"
        self[date(year, 5, 9)] = "День Победы"
        # Коректировка выходных дней
class BOT:
    def bot_mes_html_TY(self, mes,silka, url=None):
        token = ini.token
        file_name = ""
        if TY_GROP == 1:
            # ключ группы ТУ
            chat_id = ini.TY_id
            if ini.time_seychas < ini.time_bot_vrem:
                file_name = "id_message_TY_last_day"
            else:
                file_name = "id_message_TY_day"

            def send_message(chat_id, text, token, reply_markup=None):
                url = f'https://api.telegram.org/bot{token}/sendMessage'
                data = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML', "disable_web_page_preview":True}
                if reply_markup:
                    data['reply_markup'] = json.dumps(reply_markup, ensure_ascii=False)
                response = requests.post(url, json=data)
                if response.status_code == 200:
                    print('Сообщение отправлено')
                    return response.json().get('result', {}).get('message_id')
                else:
                    print(f'Ошибка при отправке сообщения: {response.status_code}')

            def save_message_id(message_id):
                with open(PUT + 'BOT\\Temp\\ID_messege\\' + file_name + '.txt', 'a') as file:
                    file.write(str(message_id) + '\n')
                with open(PUT + 'BOT\\Temp\\ID_messege\\' + file_name + '_ALL.txt', 'a') as file:
                    file.write(str(message_id) + '\n')
            buttons = [{"text": "Ссылка Google таблицу", "callback_data": "button1", "url": url}]
            reply_markup = {"inline_keyboard": [[button] for button in buttons]}
            # фильтр прикрепления ссылок
            if silka == 1:
                message_id = send_message(chat_id, mes, token, reply_markup)
            else:
                message_id = send_message(chat_id, mes, token)

            # Сохранение идентификатора сообщения в файл
            if message_id is not None:
                save_message_id(message_id)
    """отправка сообщений d в формате HTML в группу Т"""
    def bot_mes_html(self, mes,silka,url=None):
        token = ini.token
        file_name = ""
        chat_id = ""
        if TEST_BOT == 1:
            # тестовая есть алексей
            chat_id = ini.test_all
            file_name = "id_message_test_all"
        if TEST_BOT == 2:
            # тестовая нет алексея
            chat_id = ini.test_not
            file_name = "id_message_test_not"
        if TEST_BOT == 000:
            return

        def send_message(chat_id, text, token, reply_markup=None):
            url = f'https://api.telegram.org/bot{token}/sendMessage'
            data = {'chat_id': chat_id,'text': text,'parse_mode': 'HTML',}
            if reply_markup:
                data['reply_markup'] = json.dumps(reply_markup, ensure_ascii=False)
            response = requests.post(url, json=data)
            if response.status_code == 200:
                print('Сообщение отправлено')
                return response.json().get('result', {}).get('message_id')
            else:
                print(f'Ошибка при отправке сообщения: {response.status_code}')
                return None
        def save_message_id(message_id):
            with open(PUT + 'BOT\\Temp\\ID_messege\\' + file_name + '.txt', 'a') as file:
                file.write(str(message_id) + '\n')
        buttons = [{"text": "Ссылка Google Docs(в разработке)", "callback_data": "button1", "url": url}]
        reply_markup = {"inline_keyboard": [[button] for button in buttons]}
        # фильтр прикрепления ссылок
        if silka == 1:
            message_id = send_message(chat_id, mes, token, reply_markup)
        else:
            message_id = send_message(chat_id, mes, token)

        # Сохранение айд сообщения
        if message_id is not None:
            save_message_id(message_id)
    """отправка сообщений в формате HTML себе"""
    def __del_lost(self, priznak_grup):
        token = ini.token
        file_name = ""
        chat_id = ""
        if TY_GROP == 1 and priznak_grup == "TY":
            chat_id = ini.TY_id
            if ini.time_seychas < ini.time_bot_vrem:
                # сообщения на начало дня
                file_name= "id_message_TY_last_day"
                # если это начало дня то дозаписыать в файл дневные сообщения прошлого дня
                with open(PUT + 'BOT\\Temp\\ID_messege\\id_message_TY_last_day.txt', 'a') as file1:
                    with open(PUT + 'BOT\\Temp\\ID_messege\\id_message_TY_day.txt', 'r') as file2:
                        file1.write(file2.read())
            else:
                # сообщения в течении дня
                file_name = "id_message_TY_day"
        if TY_GROP != 1 and priznak_grup == "TY":
            # если передан другой признак или отключен ТУ
            return
        # чтение файлов с айди сообщениями в зависимости от условия
        with open(PUT + 'BOT\\Temp\\ID_messege\\' + file_name + '.txt', 'r') as file:
            message_ids = file.read().splitlines()
        print(message_ids)
        if not message_ids:
            print("прервано")
            return  # Если список пуст, прерываем выполнение функции

        # список сообений не удаленных
        updated_message_ids = []
        for message_id in message_ids:
            delete_url = f'https://api.telegram.org/bot{token}/deleteMessage'
            try:
                delete_data = {'chat_id': chat_id, 'message_id': int(message_id)}
                delete_response = requests.post(delete_url, data=delete_data)
                if delete_response.status_code == 200:
                    print(f'Сообщение с идентификатором {message_id} удалено')
                else:
                    print(f'Ошибка при удалении сообщения {message_id}: {delete_response.status_code}')
            except:
                # Если удаление сообщения не удалось, оставляем его в списке
                updated_message_ids.append(message_id)


        # обновление файла с айди сообщений
        with open(PUT + "BOT\\Temp\\ID_messege\\" + file_name + ".txt", 'w') as file:
            file.write('\n'.join(updated_message_ids))

    def bot_proverka_KM(self, mes):
        token = ini.token
        chat_id = ini.km
        url = f'https://api.telegram.org/bot{token}/sendMessage'
        data = {'chat_id': chat_id,'text': mes, 'parse_mode': 'HTML',}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print('Сообщение отправлено')
            return response.json().get('result', {}).get('message_id')
        else:
            print(f'Ошибка при отправке сообщения: {response.status_code}')




