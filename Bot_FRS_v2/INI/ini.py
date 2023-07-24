import sys
sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON\venv\Lib\site-packages")
sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON")
import locale
import datetime
import time as t
import pandas as pd
from datetime import date, timedelta

# Определение корнеыйх путей в файле
PUT = "C:\\Users\\Lebedevvv\\Desktop\\FRS\\Dashbord_new\\"
#PUT = "D:\\РАБОТА\\Дашборд_бот — копия\\"
PUT_download = r"C:\Users\Lebedevvv\Downloads"
#PUT_download = r"C:\Users\виталий\Downloads"
PUT_python = r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON\venv\Lib\site-packages"
#PUT_public = "\\tw1\\PUBLIC\\"
PUT_public = "P:\\"

# Текущее дата и время #############################
dat_seychas = datetime.date.today()
date_seychas = dat_seychas.strftime("%Y-%m-%d")
time_seychas = datetime.datetime.now()
time_seychas  = time_seychas.strftime("%H:%M:%S")

# получение ключей
dat = pd.read_excel(PUT + 'Bot\\key\\id.xlsx')
keys_dict = dict(zip(dat.iloc[:, 0], dat.iloc[:, 1]))
token = keys_dict.get('token')
test_all= keys_dict.get('Мой_канал')
#TY_id = keys_dict.get('Мой_канал')
TY_id = keys_dict.get('Мой_канал_ТУ')
avtozakaz_mail = keys_dict.get('avtozakaz_mail')
ya_mail_aps = keys_dict.get('ya_mail_aps')
km = keys_dict.get("km_test")
#test_not = keys_dict.get('testovaya')


# Время рассылки сообщений
time_bot_vrem = "23:30:00"

# БОТ время деления на утреннее и вечернее время до этого времени отправляются итоги дня)
zaderjka = 0
# ожидание перед отправкой соощения
TY_GROP = 1
TEST_BOT = 1


def name_day():
    # Получаем текущую дату
    current_date = datetime.date.today()
    # Получаем день недели (0 - понедельник, 1 - вторник, ..., 6 - воскресенье)
    weekday = current_date.weekday()
    # Преобразуем числовое представление дня недели в текстовое
    weekday_name = current_date.strftime("%A")
    # Выводим результат
    print("Текущий день недели (числовое представление):", weekday)
    print("Текущий день недели (текстовое представление):", weekday_name)
# прошлая неделя список дат
def date_last_week():


    def previous_week_dates():
        today = datetime.date.today()
        weekday = today.weekday()
        # Вычисляем начальную дату прошлой недели
        start_of_last_week = today - datetime.timedelta(days=weekday + 7)
        # Создаем список дат с понедельника по воскресенье прошлой недели
        dates_of_last_week = [start_of_last_week + datetime.timedelta(days=i) for i in range(7)]
        return dates_of_last_week

    # Получаем список дат прошлой недели
    date_list = previous_week_dates()
    my_list = []
    # Выводим список
    for i in date_list:
        i = i.strftime("%Y-%m-%d")
        my_list.append(i)
    print(my_list)
    return my_list

def month_and_god():
    # сохранить локаль
    old_locale = locale.getlocale(locale.LC_TIME)
    locale.setlocale(locale.LC_TIME, 'ru_RU')
    # Получить текущий месяц и год в формате строки
    month_god = dat_seychas.strftime('%B %Y')
    # вернуть локаль
    locale.setlocale(locale.LC_TIME, old_locale)
    return month_god
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
def prognoz():
    # Получаем текущую дату
    current_date = datetime.date.today()
    # Определяем первый день текущего месяца
    first_day = current_date.replace(day=1)
    # Определяем первый день следующего месяца
    next_month = first_day.replace(month=first_day.month + 1)
    # Определяем последний день текущего месяца
    last_day = next_month - datetime.timedelta(days=1)
    # Вычисляем количество дней в текущем месяце
    days_in_month = last_day.day
    # Вычисляем количество прошедших дней в текущем месяце
    days_last = current_date.day-1
    # Вычисляем количество оставшихся дней до конца месяца
    days_ostatok = days_in_month - days_last
    # Выводим результаты
    print("Количество дней в текущем месяце:", days_in_month)
    print("Прошло дней в текущем месяце:", days_last)
    print("Осталось дней до конца месяца:", days_ostatok)

    return days_in_month, days_last, days_ostatok
# словарь с датами, считает и номерует понедельники
def num_pn(yea, mon):
    def get_first_and_following_mondays(year, month):
        # Создаем объект datetime для первого дня месяца
        first_day = datetime.date(year, month, 1)
        # Находим день недели первого дня месяца (с понедельника - 0 до воскресенья - 6)
        first_day_of_week = first_day.weekday()
        # Вычисляем разницу до следующего понедельника и добавляем соответствующее количество дней
        days_until_next_monday = (7 - first_day_of_week) % 7
        next_monday = first_day + datetime.timedelta(days=days_until_next_monday)
        # Создаем список для хранения понедельников месяца
        mondays = [next_monday]
        # Добавляем следующие понедельники месяца
        while next_monday.month == month:
            next_monday += datetime.timedelta(days=7)
            mondays.append(next_monday)
        return mondays
    # Пример использования функции
    year = yea
    month = mon
    mondays = get_first_and_following_mondays(year, month)
    spis = []
    for monday in mondays:
        monday = monday.strftime('%Y-%m-%d')
        spis.append(monday)
    numbered_dict = {date: i for i, date in enumerate(spis)}
    return numbered_dict

