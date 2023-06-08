import datetime
import time as t
import pandas as pd
from datetime import date, timedelta

PUT = "C:\\Users\\Lebedevvv\\Desktop\\FRS\\DATA_copy\\"
#PUT = "D:\\РАБОТА\\Дашборд_бот\\"
#PUT_download = r"C:\Users\lebedevvv\Downloads"
PUT_download = r"C:\Users\Lebedevvv\Downloads"
PUT_python = "D:\\РАБОТА\\PAYTHON\\"
PUT_public = 0

# Текущее дата и время #############################
dat_seychas = datetime.date.today()
time_seychas = datetime.datetime.now()
time_seychas  = time_seychas.strftime("%H:%M:%S")


# получение ключей
dat = pd.read_excel(PUT + 'Bot\\key\\id.xlsx')
keys_dict = dict(zip(dat.iloc[:, 0], dat.iloc[:, 1]))
token = keys_dict.get('token')
test_all= keys_dict.get('test')
test_not = keys_dict.get('testovaya')
#TY_id = keys_dict.get('testovaya')
TY_id = keys_dict.get('TY_id')

# признак недели
with open(PUT + "BOT\\Temp\\даты_файлов\\priznzk.txt", "r") as file:
    week_day = file.read().strip()
# признак начала месяца
with open(PUT + "BOT\\Temp\\даты_файлов\\new_month.txt", "r") as file:
    new_month = file.read().strip()
########################################

time_bot_vrem = "23:40:00"
# БОТ время деления на утреннее и вечернее время до этого времени отправляются итоги дня)
zaderjka = 10
# ожидание перед отправкой соощения
TY_GROP = 0
TEST_BOT = 1

time_voropaev_vrem = "10:00:00"
# выбор группы отправки сообщений технических

# ВЫЧИСЛЕНИЕ ДАТЫ ГОДА ПО ВЧЕРАШНИЙ ДЕНЬ список дат до сегоднешнего дня
def god_todey():
    today = date.today()  # Текущая дата
    year_start = date(today.year, 1, 1)  # Первый день текущего года
    yesterday = today - timedelta(days=1)  # Вчерашняя дата
    date_list = []
    # Создаем список дат, начиная с первого дня текущего года и заканчивая вчерашним днем
    current_date = year_start
    while current_date <= yesterday:
        date_list.append(current_date.strftime('%d.%m.%Y'))
        current_date += timedelta(days=1)

    # Выводим список дат
    print(date_list)
    return date_list
# ВЫЧИСЛЕНИЕ ДАТЫ ГОДА ПО ВЧЕРАШНИЙ ДЕНЬ список дат ополыый
def god_todey_total():
    today = date.today()  # Текущая дата
    year_start = date(today.year, 1, 1)  # Первый день текущего года
    yesterday = today - timedelta(days=1)  # Вчерашняя дата
    date_list = []
    # Создаем список дат, начиная с первого дня текущего года и заканчивая вчерашним днем
    current_date = year_start
    while current_date <= yesterday:
        date_list.append(current_date.strftime('%d.%m.%Y'))
        current_date += timedelta(days=1)

    return date_list
# ВЫЧИСЛЕНИЕ ДАТЫ пронлого года
def god_last_year():
    today = date.today()  # Текущая дата
    last_year_start = date(today.year - 1, 1, 1)  # Первый день прошлого года
    last_year_end = date(today.year - 1, 12, 31)  # Последний день прошлого года
    date_list = []
    # Создаем список дат, начиная с первого дня прошлого года и заканчивая последним днем прошлого года
    current_date = last_year_start
    while current_date <= last_year_end:
        date_list.append(current_date.strftime('%d.%m.%Y'))
        current_date += timedelta(days=1)

    return date_list
# позапрошлого
def god_last_year2():
    today = date.today()  # Текущая дата
    last_year_start = date(today.year - 2, 1, 1)  # Первый день прошлого года
    last_year_end = date(today.year - 2, 12, 31)  # Последний день прошлого года
    date_list = []
    # Создаем список дат, начиная с первого дня прошлого года и заканчивая последним днем прошлого года
    current_date = last_year_start
    while current_date <= last_year_end:
        date_list.append(current_date.strftime('%d.%m.%Y'))
        current_date += timedelta(days=1)

    return date_list

