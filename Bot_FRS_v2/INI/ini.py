import datetime
import time as t
import pandas as pd
from datetime import date, timedelta

# Определение корнеыйх путей в файле
PUT = "C:\\Users\\Lebedevvv\\Desktop\\FRS\\Dashbord_new\\"
#PUT = "D:\\РАБОТА\\Дашборд_бот — копия\\"
PUT_download = r"C:\Users\Lebedevvv\Downloads"
#PUT_download = r"C:\Users\виталий\Downloads"
PUT_python = "C:\\Users\\Lebedevvv\\Desktop\\FRS\\PYTHON\\"
PUT_public = "\\tw1\\PUBLIC\\"

# Текущее дата и время #############################
dat_seychas = datetime.date.today()
date_seychas = dat_seychas.strftime("%Y-%m-%d")
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

# Время рассылки сообщений
time_bot_vrem = "23:30:00"

# БОТ время деления на утреннее и вечернее время до этого времени отправляются итоги дня)
zaderjka = 10
# ожидание перед отправкой соощения
TY_GROP = 0
TEST_BOT = 2

def weck():
    # Получаем номер недели для текущей даты
    week_number = dat_seychas.isocalendar()[1]

    # Получаем дату начала недели (понедельник)
    start_of_week = dat_seychas - datetime.timedelta(days=dat_seychas.weekday())

    # Получаем дату конца недели (воскресенье)
    end_of_week = start_of_week + datetime.timedelta(days=6)

    # Форматируем даты в нужном формате
    start_of_week_str = start_of_week.strftime('%Y-%m-%d')
    end_of_week_str = end_of_week.strftime('%Y-%m-%d')

    return week_number,start_of_week_str,end_of_week_str




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
def last_mount():
    today = datetime.date.today()
    first_day_current_month = today.replace(day=1)
    last_day_previous_month = first_day_current_month - timedelta(days=1)
    first_day_previous_month = last_day_previous_month.replace(day=1)

    date_list = []
    current_date = first_day_previous_month
    while current_date <= last_day_previous_month:
        date_list.append(current_date.strftime('%d.%m.%Y'))
        current_date += timedelta(days=1)


    return date_list


    # Использование функции и вывод списка дат

################# Для бота




