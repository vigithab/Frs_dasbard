import selenium
import warnings
import time as t
##import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import psutil
import shutil
import xlsxwriter
from pandas.tseries.offsets import DateOffset
from datetime import datetime, timedelta, time, date
from pandas.tseries.offsets import MonthBegin
import os
import pandas as pd
import sys
import math
import gc
import requests
# from memory_profiler import profile
import numpy as np
import calendar
import holidays
#import bot_TELEGRAM as bot
#import GOOGL as gg
from dateutil import parser
from dateutil import relativedelta
from dateutil import rrule
import datetime
pd.set_option("expand_frame_repr", False)
pd.set_option('display.max_colwidth', None)
gc.enable()
TY_GROP = 00
geo = "w"

# region расположение данных home или work

if geo == "h":
    # основной каталог расположение данных дашборда
    PUT = "D:\\Python\\DASHBRD_SET\\"
    # путь до файлов с данными о продажах
    PUT_PROD = PUT + "ПУТЬ ДО ФАЙЛОВ С ПРОДАЖАМИ\\Текущий год\\"
    """Путь до не разбитых файлов"""
    PUT_SEBES = "D:\\Python\\DASHBRD_SET\\Источники\\Себестоемость\\Исходные\\"
    """Путь до разбитых файлов по дням"""
    PUT_SEBES_day = "D:\\Python\\DASHBRD_SET\\Источники\\Себестоемость\\Архив\\"
    """Путь до источника"""
    PUT_SET = "D:\\Python\\DASHBRD_SET\\Источники\\паблик\\"
    """путь переноса файла"""
    PUT_SET_copy = "D:\\Python\\DASHBRD_SET\\Источники\\Чеки_сет\\Текущий день\\"
    """сохранение файла продаж"""
    PUT_SET_sales = "D:\\Python\\DASHBRD_SET\\Продаж_Set\\Текущий день\\"
    """сохранение файла чеков"""
    PUT_SET_chek = "D:\\Python\\DASHBRD_SET\\ЧЕКИ_set\\Текущий день\\"
else:
    PUT = "C:\\Users\\lebedevvv\\Desktop\\Дашборд_бот\\"
# endregion

class CustomRusHolidays(holidays.RU):
    def _populate(self, year,):
        super()._populate(year)
        # Добавляем в наш пользовательский набор праздников все официальные выходные дни.
        self[date(year, 5, 6)] = "День Воинской славы России"
        self[date(year, 5, 7)] = "День Воинской славы России"
        self[date(year, 5, 8)] = "День Победы"
        self[date(year, 5, 9)] = "День Победы"
        # Коректировка выходных дней
class RENAME:
    def Rread(self, name_data, name_col, name):
        print("Загрузка справочника магазинов...")
        while True:
            try:
                replacements = pd.read_excel("https://docs.google.com/spreadsheets/d/1SfuC2zKUFt6PQOYhB8EEivRjy4Dz-o4WDL-IR7CT3Eg/export?exportFormat=xlsx")
                """replacements = pd.read_excel(PUT + "Справочники\\ДЛЯ ЗАМЕНЫ.xlsx",
                                                 sheet_name="Лист1")"""
                rng = len(replacements)
                for i in range(rng):
                    name_data[name_col] = name_data[name_col].replace(replacements["НАЙТИ"][i], replacements["ЗАМЕНИТЬ"][i], regex=False)
                break
            except:
                print("Произошла ошибка при загрузке справочника магазинов. Повторяем попытку...")
        return name_data
    """функция переименование"""
    def magazin_info(self):
        print("Загрузка справочника магазинов...")
        while True:
            try:
                spqr = pd.read_excel("https://docs.google.com/spreadsheets/d/1qXyD0hr1sOzoMKvMyUBpfTXDwLkh0RwLcNLuiNbWmSM/export?exportFormat=xlsx")
                spqr = spqr[['ID', '!МАГАЗИН!']]
                break
            except:
                print("Произошла ошибка при загрузке справочника магазинов. Повторяем попытку...")
        return spqr
    """функция магазины для мердж"""

    def TY(self):
        # загрузка файла справочника териториалов
        ty = pd.read_excel("https://docs.google.com/spreadsheets/d/1rwsBEeK_dLdpJOAXanwtspRF21Z3kWDvruani53JpRY/export?exportFormat=xlsx")

        ty = ty[["Название 1 С (для фин реза)", "Менеджер"]]
        RENAME().Rread(name_data = ty, name_col= "Название 1 С (для фин реза)", name="TY")
        ty = ty.rename(columns={"Название 1 С (для фин реза)": "!МАГАЗИН!"})
        return ty

    def TY_Spravochnik(self):
        ty = pd.read_excel("https://docs.google.com/spreadsheets/d/1qXyD0hr1sOzoMKvMyUBpfTXDwLkh0RwLcNLuiNbWmSM/export?exportFormat=xlsx")
        ty = ty[["!МАГАЗИН!","Менеджер"]]
        Ln_tip = {'Турова Анна Сергеевна': 'Турова А.С',
                  'Баранова Лариса Викторовна': 'Баранова Л.В',
                  'Геровский Иван Владимирович': 'Геровский И.В',
                  'Изотов Вадим Валентинович': 'Изотов В.В',
                  'Томск': 'Томск',
                  'Павлова Анна Александровна': 'Павлова А.А',
                  'Бедарева Наталья Геннадьевна': 'Бедарева Н.Г',
                  'Сергеев Алексей Сергеевич': 'Сергеев А.С',
                  'Карпова Екатерина Эдуардовна': 'Карпова Е.Э'}
        ty["Менеджер"] = ty["Менеджер"].map(Ln_tip)

        #ty  = ty .rename(columns={"!МАГАЗИН!": "магазин"})
        return ty
        # переименование магазинов справочник ТУ
class MEMORY:
    def mem(self, x, text):
        total_memory_usage = x.memory_usage(deep=True).sum()
        print(text + " - Использовано памяти: {:.2f} MB".format(total_memory_usage / 1e6))
    """использование памяти датафрейм"""
    def mem_total(self,x):
        process = psutil.Process()
        memory_info = process.memory_info()
        total_memory_usage = memory_info.rss
        print(x +" - Использование памяти: {:.2f} MB".format(total_memory_usage / 1024 / 1024))
    """использование памяти программой полная"""
        # Память
class BOT:
    def bot_mes_html_TY(self, mes):
        # получение ключей
        dat = pd.read_excel(PUT + 'Bot\\key\\id.xlsx')
        keys_dict = dict(zip(dat.iloc[:, 0], dat.iloc[:, 1]))
        token = keys_dict.get('token')
        #test = keys_dict.get('test')
        if TY_GROP == 1:
            TY_id = keys_dict.get('TY_id')
            """url = f'https://api.telegram.org/bot{token}/sendMessage'
            # TEST ####################################################
            # Параметры запроса для отправки сообщения
            data = {'chat_id': test, 'text': mes, 'parse_mode': 'HTML'}
            # Отправка запроса на сервер Telegram для отправки сообщения
            response = requests.post(url, data=data)
            # Проверка ответа от сервера Telegram
            if response.status_code == 200:
                print('Отправлено Test')
            else:
                print(f'Ошибка при отправке Test: {response.status_code}')"""

            url = f'https://api.telegram.org/bot{token}/sendMessage'
            # Параметры запроса для отправки сообщения
            params_ty = {'chat_id': TY_id, 'text': mes, 'parse_mode': 'HTML', 'disable_web_page_preview': True}
            # Отправка запроса на сервер Telegram для отправки сообщения
            response_ty = requests.post(url, data=params_ty)
            # Проверка ответа от сервера Telegram
            if response_ty.status_code == 200:
                print('Сообщение успешно Территориалов!')
            else:
                print(f'Ошибка при отправке Территориалов: {response_ty.status_code}')
    """отправка сообщений d в формате HTML в группу Т"""
    def bot_mes_TY(self):
        # получение ключей
        dat = pd.read_excel(PUT + 'BOT\\key\\id.xlsx')
        keys_dict = dict(zip(dat.iloc[:, 0], dat.iloc[:, 1]))
        token = keys_dict.get('token')
        test = keys_dict.get('test')
        TY_id = keys_dict.get('TY_id')
        #analitik = keys_dict.get('analitik')
        #BOT_RUK_FRS = keys_dict.get('BOT_RUK_FRS')
        mes = "Коллеги"
        # TEST ####################################################
        url = f'https://api.telegram.org/bot{token}/sendMessage'
        # Параметры
        params = {'chat_id': TY_id, 'text':mes,}
        # ЗАПРОС ОТПРАВКА
        response = requests.post(url, data=params)
        # Проверка ответа от сервера Telegram
        if response.status_code == 200:
            print('Отправлено Test')
        else:
            print(f'Ошибка при отправке Test: {response.status_code}')
        """if TY_GROP == "y":
            url = f'https://api.telegram.org/bot{token}/sendMessage'
            # Параметры запроса для отправки сообщения
            params_ty = {'chat_id': TY_id, 'text': mes }
            # Отправка запроса на сервер Telegram для отправки сообщения
            response_ty = requests.post(url, data=params_ty)
            # Проверка ответа от сервера Telegram
            if response_ty.status_code == 200:
                print('Сообщение успешно Руководители!')
            else:
                print(f'Ошибка при отправке Группа руководители: {response_ty.status_code}')"""
        # отправка сообщений ботом
    """отправка простого сообщения"""
    def bot_mes(self, mes):
        # получение ключей
        dat = pd.read_excel(PUT + 'BOT\\key\\id.xlsx')
        keys_dict = dict(zip(dat.iloc[:, 0], dat.iloc[:, 1]))
        token = keys_dict.get('token')
        test = keys_dict.get('test')
        #TY_id = keys_dict.get('TY_id')
        #analitik = keys_dict.get('analitik')
        #BOT_RUK_FRS = keys_dict.get('BOT_RUK_FRS')
        # TEST ####################################################
        url = f'https://api.telegram.org/bot{token}/sendMessage'
        # Параметры
        params = {'chat_id': test, 'text':mes,}
        # ЗАПРОС ОТПРАВКА
        response = requests.post(url, data=params)
        # Проверка ответа от сервера Telegram
        if response.status_code == 200:
            print('Отправлено Test')
        else:
            print(f'Ошибка при отправке Test: {response.status_code}')
        """if TY_GROP == "y":
            url = f'https://api.telegram.org/bot{token}/sendMessage'
            # Параметры запроса для отправки сообщения
            params_ty = {'chat_id': TY_id, 'text': mes }
            # Отправка запроса на сервер Telegram для отправки сообщения
            response_ty = requests.post(url, data=params_ty)
            # Проверка ответа от сервера Telegram
            if response_ty.status_code == 200:
                print('Сообщение успешно Руководители!')
            else:
                print(f'Ошибка при отправке Группа руководители: {response_ty.status_code}')"""
        # отправка сообщений ботом
    """отправка простого сообщения"""
    def bot_mes_html(self, mes):
        # получение ключей
        dat = pd.read_excel(PUT + 'Bot\\key\\id.xlsx')
        keys_dict = dict(zip(dat.iloc[:, 0], dat.iloc[:, 1]))
        token = keys_dict.get('token')
        test = keys_dict.get('test')
        #analitik = keys_dict.get('analitik')
        #BOT_RUK_FRS = keys_dict.get('BOT_RUK_FRS')
        #TY_id = keys_dict.get('TY_id')


        url = f'https://api.telegram.org/bot{token}/sendMessage'

        # TEST ####################################################
        # Параметры запроса для отправки сообщения
        data = {'chat_id': test, 'text': mes, 'parse_mode': 'HTML', 'disable_web_page_preview': True}
        # Отправка запроса на сервер Telegram для отправки сообщения
        response = requests.post(url, data=data)
        # Проверка ответа от сервера Telegram
        if response.status_code == 200:
            print('Отправлено Test')
        else:
            print(f'Ошибка при отправке Test: {response.status_code}')
    """отправка сообщений в формате HTML себе"""

class FLOAT:
    def float_colms(self, name_data, name_col):
        for i in name_col:
            name_data[i] = (name_data[i].astype(str)
                                              .str.replace("\xa0", "")
                                              .str.replace(",", ".")
                                              .fillna("0")
                                              .astype("float")
                                              .round(2))
        return name_data
    """Для нескольких столбцов"""
    def float_colm(self, name_data, name_col):

        name_data[name_col] = (name_data[name_col].astype(str)
                                          .str.replace("\xa0", "")
                                          .str.replace(",", ".")
                                          .fillna("0")
                                          .astype("float")
                                          .round(2))
        return name_data
    """для одного столбца"""
        # перевод в число
class NEW_data:
    def Obrabotka(self):
        NEW_data().Set_obrabotka()

        spqr = RENAME().magazin_info()
        for root, dirs, files in os.walk(PUT + "Selenium\\Оригинальные файлы\\"):
            # "PUT + "Selenium\\Оригинальные файлы\\"
            for file in files:
                if "2023" in file:
                    os.path.basename(file)
                    file_path = os.path.join(root, file)
                    print( "Фаил: ", os.path.basename(file_path)[:-5], " / Начат: ", str(datetime.datetime.now())[:-10],)

                    df  = pd.read_excel(file_path)

                    if "Магазин 1C" in df.columns:
                        # удаление столбца "магазин"
                        df.drop("Магазин 1C", axis=1, inplace=True)

                    d = df['Дата/Время чека'][1]
                    new_filename = d[0:10] + ".xlsx"
                    df = df.rename(columns={"Магазин": 'ID'})
                    table = df.merge(spqr[['!МАГАЗИН!', 'ID']], on='ID', how="left")
                    del df
                    table = table.loc[table["Тип"].notnull()]
                    table['!МАГАЗИН!'] = table['!МАГАЗИН!'].astype("str")
                    table['Наименование товара'] = table['Наименование товара'].fillna("неизвестно").astype("str")

                    sales_day = table.copy()
                    # удаление микромаркетов
                    l_mag = ("Микромаркет", "Экопункт", "Вендинг", "Итого")
                    for w in l_mag:
                        sales_day = sales_day[~sales_day["!МАГАЗИН!"].str.contains(w)].reset_index(drop=True)

                    # удаление подарочных карт
                    PODAROK = ["Подарочная карта КМ 500р+ конверт", "Подарочная карта КМ 1000р+ конверт",
                               "подарочная карта КМ 500 НОВАЯ",
                               "подарочная карта КМ 1000 НОВАЯ"]
                    for x in PODAROK:
                        sales_day = sales_day.loc[sales_day["Наименование товара"]!= x]


                    sales_day.to_excel(PUT + "Selenium\\По дням исходники\\" + new_filename, index=False)
                    # обработка файла чеков
                    sales_day_cehk = NEW_data().selenium_day_chek(name_datafreme=sales_day, name_file=str(new_filename))
                    # сохранение Сгрупированного файла чеков
                    sales_day_cehk.to_excel(PUT + "♀Чеки\\2023\\" + new_filename, index=False)

                    # сохранение Сгрупированного файла продаж;
                    sales_day_sales = NEW_data().Set_sales(name_datafreme=sales_day, name_file=str(new_filename))
                    sales_day_sales.to_excel(PUT + "♀Продажи\\текущий месяц\\" + new_filename, index=False)

                    del sales_day_cehk
                    del sales_day
                    gc.collect()
                    # region СОХРАНЕНИЕ УДАЛЕННЫХ ДАННЫХ
                    # Сохранение отдельно вейдинги и микромаркеты
                    mask_VEN = table["!МАГАЗИН!"].str.contains("|".join(l_mag))
                    sales_day_VEN = table[mask_VEN]
                    sales_day_VEN.to_excel(PUT + "Selenium\\Вейдинги и микромаркет\\" + new_filename, index=False)

                    del sales_day_VEN
                    gc.collect()

                    # Сохранение отдельно подарочные карты
                    sales_day_Podarok = table.loc[(table["Наименование товара"] == "Подарочная карта КМ 500р+ конверт") |
                                                (table["Наименование товара"] ==  "Подарочная карта КМ 1000р+ конверт") |
                                                (table["Наименование товара"] == "подарочная карта КМ 500 НОВАЯ")|
                                                (table["Наименование товара"] == "подарочная карта КМ 1000 НОВАЯ")]

                    sales_day_Podarok.to_excel(PUT + "Selenium\\Подарочные карты\\" + new_filename, index=False)

                    del sales_day_Podarok
                    gc.collect()

                    try:
                        if geo == "w":
                            # Сохранение отдельно анулированные и возвращенные чеки
                            sales_null = table.loc[(table["Тип"] == "Отмена") | (table["Тип"] == "Возврат")]
                            sales_null.to_excel(PUT + "Selenium\\Анулированные и возврат чеки\\" + new_filename, index=False)
                            sales_null.to_excel("P:\\Общие\\ЭБД\\Франшиза\\Аннулированные чеки\\" + new_filename, index=False)
                            del sales_null
                            gc.collect()
                    except:
                        print("Ошибка при сохранении анулированные и возвращенные чеки")
                    try:
                        if geo == "w":
                            # Сохранение ночные магазины
                            noch = table.loc[(table["ID"] == 42008) | (table["ID"] ==42017) | (table["ID"] ==42025)]
                            noch.to_excel("P:\\Фирменная розница\\ФРС\\Данные из 1 С\\Ночные_магазины_set\\" + new_filename, index=False)
                            del noch,table
                            gc.collect()
                    except:
                        print("Ошибка при сохранении ночные магазины")

                # bot.BOT_raschet().BOT()
                # endregion
        NEW_data().selenium_day_Spisania()
        NEW_data().sort_file()
        NEW_data().sebest()
        return
    # основнй файл отвечающий за обработку
    def Set_obrabotka(self):
        def spisok_dat():
            # region СПИСОК ДАТ
            today = datetime.datetime.now()
            tame_Filter = today.strftime("%H:%M:%S")

            spisok_d = [datetime.datetime.now().strftime('%d.%m.%Y')]
            # сохранение файла с датой обновления
            with open(PUT + 'NEW\\дата обновления.txt', 'w') as f:
                f.write(str(today))
            ta = "10:00:00"
            if tame_Filter < ta:
                day_1 = today - timedelta(days=1)
                date_vchera = day_1.strftime('%d.%m.%Y')
                # day_2 = today - timedelta(days=2)
                # date_poz_vchera = day_2.strftime('%d.%m.%Y')
                spisok_d.append(date_vchera)
                # spisok_d.append(date_poz_vchera)

            """start_date = date(2023, 1, 1)  # начальная дата
            end_date = date(2023, 5, 12)  # конечная дата
            delta = timedelta(days=1)  # шаг даты

            dates_list = []
            while start_date < end_date:
                # # преобразование даты в строку в формате 'день.месяц.год' и добавление её в список
                dates_list.append(start_date.strftime('%d.%m.%Y'))
                start_date += delta
                spisok_d = dates_list"""

            #spisok_d = ['11.05.2023', '12.05.2023','13.05.2023']
            print(spisok_d)
            return spisok_d
        # region СКАЧИВАНИЕ С САЙТА
        warnings.filterwarnings('ignore')  ##отключаем warnings
        ua = UserAgent()
        options = webdriver.ChromeOptions()
        options.add_argument("user_agent=" + ua.random)
        driver = webdriver.Chrome(chrome_options=options)
        url = 'http://10.32.2.51:8443/operday/checks'
        driver.get(url)
        t.sleep(3)
        driver.set_window_size(1024, 600)
        driver.maximize_window()
        t.sleep(1)
        id_box = driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/form/div/div[1]/div/input')
        t.sleep(0.5)
        id_box.send_keys('lebedevvv')
        t.sleep(1)
        pass_box = driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/form/div/div[2]/div/input')
        t.sleep(0.5)
        pass_box.send_keys('hCPxMeOdp')
        t.sleep(1)
        print("Вход на сайт...")
        login_button = driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/form/div/button/span[1]')
        t.sleep(0.5)
        login_button.click()
        t.sleep(2)
        def back(pole):
            print("Ввод новойдаты")
            i = 0
            while i < 12:
                pole.send_keys(Keys.BACKSPACE)
                i += 1
        try:
            t.sleep(0.5)
            menu = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, 'appBarLeftButton')))
        except:
            t.sleep(0.5)
            print(menu.text)
        finally:
            t.sleep(0.5)
            menu.click()
        try:
            t.sleep(0.5)
            menu_op_day_cheks = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[3]/div[2]/div[2]/div[2]/div/div/div/div[1]/div[1]/span')))
        except:
            t.sleep(0.5)
            d = "no"
        finally:
            t.sleep(1)
            if d == "no":
                try:
                    menu_op_day = WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div[1]/div/div[2]/div[2]/div[1]/span')))
                finally:
                    t.sleep(2)
                    menu_op_day.click()
                    print("click operday")
                try:
                    menu_op_day_cheks = WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div[1]/div[1]')))
                finally:
                    t.sleep(2)
                    menu_op_day_cheks.click()
                    print("m")
            else:
                t.sleep(1)
                menu_op_day_cheks.click()
        print("Отправлен на скачивание.....")

        spisok_d = spisok_dat()
        for day in spisok_d:
            #bot.BOT().bot_mes(mes="Скачивание файла :" + str(day))
            new_day_1 = day + " 00:00"
            t.sleep(0.5)
            new_day_2 = day + " 23:59"
            try:
                t.sleep(1)
                menu_data_n = WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/div/div[1]/div[2]/div[2]/div[1]/div/div/div[1]/div/div/div/input')))
            finally:
                back(menu_data_n)
                t.sleep(1)
                print("вводим данные")
                menu_data_n.send_keys(new_day_1)
            t.sleep(2)
            try:
                t.sleep(0.5)
                menu_data_k = WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/div/div[1]/div[2]/div[2]/div[1]/div/div/div[2]/div/div/div/input')))
            finally:
                t.sleep(0.5)
                menu_data_k.clear()
                t.sleep(0.5)
                back(menu_data_k)
                t.sleep(1)
                print("вводим данные")
                menu_data_k.send_keys(new_day_2)
            t.sleep(2)
            # endregion
            try:
                t.sleep(1)
                menu_primenit = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div[2]/div/div/div/div[1]/div[2]/div[3]/button[2]/span[1]')))
            finally:
                t.sleep(1)
                menu_primenit.click()
            t.sleep(1)
            down = ""
            try:
                t.sleep(1)
                dowload = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '/html/body/div/div/div/div[2]/div/div/div/div[1]/div[2]/div[3]/div[1]/div/div/button/span[1]')))
            except:
                down = "no"
            finally:
                if down == "no":
                    print("нет кнопки")
                else:
                    t.sleep(0.5)
                    dowload.click()

                try:
                    dowload_all = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[3]/ul/li[2]')))
                finally:
                    t.sleep(0.5)
                    dowload_all.click()
                    t.sleep(2)
                    x = ""
                try:
                    t.sleep(1)
                    dowload_yes = WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[3]/div/div[3]/button[2]/span[1]')))
                except:
                    x = "no"
                finally:
                    if x == "no":
                        print("но")
                    else:
                        t.sleep(1)
                        dowload_yes.click()
                        t.sleep(0.5)


            folder_path = r"C:\Users\lebedevvv\Downloads"  # путь до папки, которую необходимо мониторить
            partial_name = "PurchasePositions"  # подстрока, которую необходимо найти
            found_file = False
            BOT().bot_mes(mes=str(day)+ " - Ожидание файла.... ")
            while not found_file:
                for filename in os.listdir(folder_path):
                    if partial_name in filename and filename.endswith(".xlsx"):
                        # найден файл, удовлетворяющий условиям
                        print(f"Найден файл: {filename}")
                        found_file = True

                        t.sleep(0.7)
                        path_download = r"C:\Users\lebedevvv\Downloads"

                        #spqr = pd.read_excel("https://docs.google.com/spreadsheets/d/1qXyD0hr1sOzoMKvMyUBpfTXDwLkh0RwLcNLuiNbWmSM/export?exportFormat=xlsx")
                        #spqr = spqr[['ID', '!МАГАЗИН!']]
                        files = os.listdir(path_download)
                        #print(files, " и ", path_download)
                        for f in files:
                            #d = len(f)
                            file_name = f[0:17]
                            file = path_download + "\\" + f
                            if str(file_name) == "PurchasePositions":
                                try:
                                    df = pd.read_excel(file, skiprows=1)
                                    MEMORY().mem_total(x="Фаил загружен: " + os.path.basename(file))

                                    d = df['Дата/Время чека'][1]
                                    new_filename = d[0:10] + ".xlsx"

                                    df.to_excel(PUT + "Selenium\\Оригинальные файлы\\" + new_filename, index=False)
                                    #bot.BOT().bot_mes(mes="Фаил скачан: " + str(new_filename))
                                    del df
                                    gc.collect()
                                    os.remove(file)
                                except Exception as e:
                                    with open(PUT + "NEW\\error_log.txt", "a") as f:
                                        f.write(f"Ошибка при открытии файла {file}: {str(e)}\n")
                                    continue  # продолжить выполнение цикла

                # Проверьте, был ли найден файл. Если нет, подождите несколько секунд и повторите попытку
                if not found_file:
                    print(f"Файл {partial_name} не найден. Ожидание...")
                    t.sleep(2)  # задержка в 1 секунд перед следующей попыткой поиска файла


        driver.close()
        driver.quit()
        #SET().History()
        return
    # Загрузка с сайта сетретейл
    def Set_sales(self, name_datafreme, name_file):
        sales_day_sales = name_datafreme[
            [ "ID", "!МАГАЗИН!", "Тип", "Наименование товара", "Количество", "Стоимость позиции", "Сумма скидки","Штрихкод"]]
        sales_day_sales = sales_day_sales.loc[(sales_day_sales["Тип"] == "Продажа") | (sales_day_sales["Тип"] == "Возврат") ]
        sales_day_sales_copy = sales_day_sales[["Наименование товара","Штрихкод"]].drop_duplicates(subset=["Наименование товара"])

        ln = ("Стоимость позиции", "Количество", "Сумма скидки")

        FLOAT().float_colms(name_data=sales_day_sales, name_col=ln)
        sales_day_sales = sales_day_sales.drop(["Тип"], axis=1)
        #sales_day_sales["Дата"] = pd.to_datetime(sales_day_sales["Дата/Время чека"]).dt.date
        #sales_day_sales["Дата/Время чека"] = sales_day_sales["Дата/Время чека"].astype("datetime64[ns]").dt.date
        #sales_day_sales["Дата/Время чека"] = pd.to_datetime(sales_day_sales["Дата/Время чека"], format='%Y-%m-%d')
        er = sales_day_sales["Стоимость позиции"].sum()
        sales_day_sales =  sales_day_sales [[ "ID", "!МАГАЗИН!", "Наименование товара", "Количество", "Стоимость позиции", "Сумма скидки"]]

        sales_day_sales = sales_day_sales.groupby(["!МАГАЗИН!","ID","Наименование товара", ], as_index=False) \
            .agg({"Стоимость позиции": "sum",
                  "Количество": "sum",
                  "Сумма скидки": "sum"}) \
            .sort_values("!МАГАЗИН!", ascending=False).reset_index(drop=True)
        er1 = sales_day_sales["Стоимость позиции"].sum()
        sales_day_sales = sales_day_sales.merge(sales_day_sales_copy,
                                                on=["Наименование товара"], how="left").reset_index(drop=True)
        del sales_day_sales_copy

        # ######################################################################################### Загузка названий с 1 с
        spravka_nom = pd.read_csv(PUT + "Справочники\\Справочник номеклатуры.txt", sep="\t", skiprows=1, encoding="utf-8",
                                  names=('номенклатура_1с', "cрок_годности", "группа", "подгруппа", "Штрихкод",))
        # spravka_dop = pd.read_excel(PUT + "\\Справочники\\Справочник номенклатуры\\Коректировка штрих кодов.xlsx")
        spravka_nom['номенклатура_1с'] = spravka_nom['номенклатура_1с'].fillna("неизвестно").astype("str")
        sales_day_sales["Штрихкод"] = sales_day_sales["Штрихкод"].astype("str").str.replace(".0", "")
        spravka_nom["Штрихкод"] = spravka_nom["Штрихкод"].astype("str").str.replace(".0", "")
        spravka_nom["штрихкод_1c"] = spravka_nom["Штрихкод"]
        sales_day_sales = sales_day_sales.merge(spravka_nom[['номенклатура_1с', "Штрихкод"]],
                            on=["Штрихкод"], how="left").reset_index(drop=True)
        del spravka_nom
        gc.collect()
        # ############################################################################################
        sales_day_sales['filename'] = os.path.basename(name_file)[:-5]
        #sales_day_sales = sales_day_sales.drop(["Штрихкод"], axis=1)
        sales_day_sales = sales_day_sales.rename(columns={'filename': "Дата/Время чека"})
        sales_day_sales["Дата/Время чека"] = pd.to_datetime(sales_day_sales["Дата/Время чека"], format='%d.%m.%Y')

        # Сгруппируем данные по номенклатуре и посчитаем сумму по столбцу "сумма"
        sum_dostavka_im = sales_day_sales.groupby("Наименование товара")["Стоимость позиции"].sum()
        # Получим сумму по номенклатуре "Доставка ИМ" "Пельмени Московские, кат Б, зам, вес"
        sum_dostavka_im = sum_dostavka_im.get("Доставка ИМ", 0)


        infovision = pd.read_excel(PUT + "NEW\\ОБРАБОТКА ОШИБОК\\infovision.xlsx", parse_dates=["Дата"])
        infovision["Дата"] = pd.to_datetime(infovision["Дата"], format='%d.%m.%Y')
        RENAME().Rread(name_data=infovision, name_col="Магазин", name="Суммы 1с")
        infovision = infovision.rename(columns={'Магазин': "!МАГАЗИН!","Дата": "Дата/Время чека"})

        c1 = pd.read_excel(PUT + "NEW\\ОБРАБОТКА ОШИБОК\\Продажи 1 с.xlsx", parse_dates=["Дата/Время чека"])
        c1["Дата/Время чека"] = pd.to_datetime(c1["Дата/Время чека"], format='%d.%m.%Y')

        RENAME().Rread(name_data=c1, name_col="!МАГАЗИН!", name="Суммы 1с")

        setret = sales_day_sales[["!МАГАЗИН!", "Дата/Время чека", "Стоимость позиции"]].copy()
        setret = setret.rename(columns={"Стоимость позиции": "выручка set"})
        setret =  setret.groupby(["!МАГАЗИН!", "Дата/Время чека"], as_index=False) \
            .agg({"выручка set": "sum"}) \
            .sort_values("!МАГАЗИН!", ascending=False).reset_index(drop=True)

        setret = setret.merge(infovision, on=['!МАГАЗИН!', "Дата/Время чека"], how="left")
        setret = setret.merge(c1, on=['!МАГАЗИН!', "Дата/Время чека"], how="left")
        setret["Разница DSH/1 с"] = setret["выручка set"]- setret["Выручка 1с"]
        setret["Разница DSH/Инфовижен(к)"] = setret["выручка set"] - setret["выручка infovision"]
        setret["1 с / Инфовижен(к)"] = setret["Выручка 1с"] - setret["выручка infovision"]

        sum_1c_dh = setret["Разница DSH/1 с"].sum()
        sum_info_dh = setret["Разница DSH/Инфовижен(к)"].sum()

        sum_1c_info = setret["1 с / Инфовижен(к)"].sum()

        setret.to_excel(PUT + "NEW\\ОБРАБОТКА ОШИБОК\\разница сумм\\" + name_file, index=False)
        """  print(infovision[:50])
        print(c1[:50])
        print(setret)
        print(sum_dostavka_im)"""



        mes = os.path.basename(name_file)[:-5] + "\nДо и после оработки:" + str(er1.round() - er.round()) +\
              "\nРазница c 1C: " +str(sum_1c_dh.round()) +"\nРазница c Инфовижен(к): " +str(sum_info_dh.round())+ \
              "\nРазница 1C-Инфовижен(к): "+str(sum_1c_info.round()) + "\nИнтернет магазин: "+str(sum_dostavka_im)
        BOT().bot_mes(mes=mes)

        return sales_day_sales
    # обработка файлов продаж
    def selenium_day_chek(self, name_datafreme, name_file):
        MEMORY().mem_total(x="Формирование чеков: ")
        def cnevk(tip):
            sales_day_cehk = name_datafreme[["Тип","!МАГАЗИН!", "ID", "Дата/Время чека", "Касса", "Чек", "Стоимость позиции", "Код товара","Смена"]]
            print("sales_day_cehk\n", sales_day_cehk)
            if tip=="Продажа":
                sales_day_cehk = sales_day_cehk.loc[(sales_day_cehk["Тип"] == tip) | (sales_day_cehk["Тип"] == "Возврат")]
                sales_day_cehk = sales_day_cehk.drop(["Тип"], axis=1)
            else:
                sales_day_cehk = sales_day_cehk.loc[(sales_day_cehk["Тип"] == tip)]
                sales_day_cehk = sales_day_cehk.drop(["Тип"], axis=1)
            # время обновления
            set_check_date = sales_day_cehk["Дата/Время чека"].max()
            with open(PUT + "NEW\\DATE.txt", "w") as f:
                f.write(str(set_check_date))
            del set_check_date
            sales_day_cehk["Дата/Время чека"] = pd.to_datetime(sales_day_cehk["Дата/Время чека"], format="%d.%m.%Y %H:%M:%S").dt.date
            # Формирование ID Чека
            sales_day_cehk["ID_Chek"] = sales_day_cehk["ID"].astype(int).astype(str) + sales_day_cehk["Касса"].astype(int).astype(str) + sales_day_cehk["Чек"].astype(int).astype(
                str) + sales_day_cehk["Дата/Время чека"].astype(str) + sales_day_cehk["Смена"].astype(str)


            sales_day_cehk = sales_day_cehk.drop(["Касса", "Чек","Смена"], axis=1)
            # удаление не нужных символов
            FLOAT().float_colm(name_data=sales_day_cehk, name_col="Стоимость позиции")
            # Групировки по дням
            sales_day_cehk = sales_day_cehk.groupby(["!МАГАЗИН!", "ID", "Дата/Время чека", "ID_Chek"], as_index=False).agg({
                "Стоимость позиции": "sum",
                "Код товара": [("Количество товаров в чеке", "count"), ("Количество уникальных товаров в чеке", "nunique")]})

            # переименовываем столбцы
            sales_day_cehk.columns = ['!МАГАЗИН!', "ID", 'Дата/Время чека', 'ID_Chek', 'Стоимость позиции', 'Количество товаров в чеке',
                                 'Количество уникальных товаров в чеке']
            # выбираем нужные столбцы и сортируем по дате/времени чека в порядке убывания
            sales_day_cehk = sales_day_cehk[
                ["ID", '!МАГАЗИН!', 'Дата/Время чека', 'ID_Chek', 'Стоимость позиции', 'Количество товаров в чеке', 'Количество уникальных товаров в чеке']] \
                .sort_values('Дата/Время чека', ascending=False) \
                .reset_index(drop=True)
            # групировка по магазинам
            sales_day_cehk = sales_day_cehk.groupby(["ID", "!МАГАЗИН!", "Дата/Время чека"], as_index=False) \
                .agg({"Стоимость позиции": "sum",
                      'ID_Chek': "count",
                      "Количество товаров в чеке": "mean",
                      "Количество уникальных товаров в чеке": "mean"}) \
                .sort_values("Дата/Время чека", ascending=False).reset_index(drop=True)

            # дбавление среднего чека
            sales_day_cehk["Средний чек"] = sales_day_cehk["Стоимость позиции"] / sales_day_cehk["ID_Chek"]
            # переименование столбцов
            sales_day_cehk = sales_day_cehk.rename(columns={ "Дата/Время чека": "дата", "Стоимость позиции": "выручка",
                                                  "ID_Chek": "Количество чеков", "Количество товаров в чеке": "количество товаров в чеке",
                                                  "Количество уникальных товаров в чеке": "количество уникальных товаров в чеке"})
            # округление
            sales_day_cehk= sales_day_cehk.round(2)
            sales_day_cehk['filename'] = os.path.basename(name_file)[:-5]
            sales_day_cehk = sales_day_cehk.drop(['дата'], axis=1)
            sales_day_cehk = sales_day_cehk.rename(columns={'filename': 'дата'})
            sales_day_cehk["дата"] = pd.to_datetime(sales_day_cehk["дата"], format='%d.%m.%Y')

            MEMORY().mem_total(x="Обработан - Фаил чеков: " + str(name_file))
            return sales_day_cehk
        sales_day_cehk = cnevk(tip="Продажа")

        sales_day_cehk = sales_day_cehk.rename(columns={"Количество чеков": "Количество чеков_продажа"})

        vozvrat = cnevk(tip="Возврат")
        vozvrat = vozvrat[["!МАГАЗИН!","Количество чеков","дата"]]
        vozvrat = vozvrat.rename(columns={"Количество чеков": "Количество чеков_возврат"})

        sales_day_cehk = sales_day_cehk.merge(vozvrat,
                                                on=["!МАГАЗИН!","дата"], how="left").reset_index(drop=True)

        sales_day_cehk["Количество чеков_возврат"] = sales_day_cehk["Количество чеков_возврат"].fillna(0)
        sales_day_cehk["Количество чеков"] = sales_day_cehk["Количество чеков_продажа"] # - sales_day_cehk["Количество чеков_возврат"]
        sales_day_cehk = sales_day_cehk.drop(["Количество чеков_продажа", "Количество чеков_возврат"], axis=1)

        return sales_day_cehk
    # обработка файлов чеков
    def selenium_day_Spisania(self):
        today = datetime.datetime.now()
        tame_Filter = today.strftime("%H:%M:%S")
        ta = "11:00:00"


        print("Обработка списания")
        if tame_Filter < ta:
            # Папка для поиска файла
            folder_path = "P:\\Фирменная розница\\ФРС\\Данные из 1 С\\Списания\\"

            # Папка для перемещения файла
            destination_folder = PUT + "NEW\\Списания\\"

            # Получаем список файлов в указанной папке и ее подпапках
            file_list = []
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_list.append(os.path.join(root, file))

            # Находим файл с максимальной датой изменения
            latest_file = max(file_list, key=os.path.getmtime)

            # Копируем найденный файл в указанную папку
            shutil.copy(latest_file, destination_folder)


            for root, dirs, files in os.walk(PUT + "NEW\\Списания\\"):
                for file in files:
                    os.path.basename(file)
                    file_path = os.path.join(root, file)
                    df = pd.read_csv(file_path, sep="\t", encoding='utf-8',skiprows=5, parse_dates=["Регистратор.Дата"], date_format="%d.%m.%Y %H:%M:%S")

                    df = df.rename(columns={"Магазин": "!МАГАЗИН!","Регистратор.Дата":"дата" })
                    # замена корявых названий
                    df = df.loc[(df["Аналитика хозяйственной операции"] =="Дегустации") |
                                (df["Аналитика хозяйственной операции"] == "Питание сотрудников")|
                                (df["Аналитика хозяйственной операции"] == "ПОТЕРИ") |
                                (df["Аналитика хозяйственной операции"] == "МАРКЕТИНГ (блогеры, фотосессии)")|
                                (df["Аналитика хозяйственной операции"] == "Подарок покупателю (бонусы)")|
                                (df["Аналитика хозяйственной операции"] == "Подарок покупателю (сервисная фишка)")|
                                (df["Аналитика хозяйственной операции"] == "Хозяйственные товары")|
                                (df["Аналитика хозяйственной операции"] == "Кражи")]

                    df.loc[(df["Аналитика хозяйственной операции"] == "Дегустации") |
                                (df["Аналитика хозяйственной операции"] == "Питание сотрудников")|
                                (df["Аналитика хозяйственной операции"] == "ПОТЕРИ") |
                                (df["Аналитика хозяйственной операции"] == "МАРКЕТИНГ (блогеры, фотосессии)")|
                                (df["Аналитика хозяйственной операции"] == "Подарок покупателю (бонусы)")|
                                (df["Аналитика хозяйственной операции"] == "Подарок покупателю (сервисная фишка)")|
                                (df["Аналитика хозяйственной операции"] == "Кражи"), "отбор"] = "показатель"

                    df['Причина списания'] = df['Причина списания'].fillna('не определено')
                    df.loc[df['Причина списания'].str.contains('<Объект не найден>'), 'Причина списания'] = 'не определено'
                    df = df.loc[df["дата"] != "Итого"]
                    df = df.loc[df["!МАГАЗИН!"] != "Итого"]
                    print(df)
                    df["дата"] = pd.to_datetime(df["дата"]).dt.strftime('%d.%m.%Y')
                    RENAME().Rread(name_data=df, name_col="!МАГАЗИН!", name="Списания")

                    l_mag = ("Микромаркет", "Экопункт", "Вендинг", "Итого")
                    df["!МАГАЗИН!"] = df["!МАГАЗИН!"].fillna("Не известно")
                    for w in l_mag:
                        df = df[~df["!МАГАЗИН!"].str.contains(w)]

                    # "<Объект не найден>" и пустые удалить из столбца причина

                    # df["Дата/Время чека"] = df["Дата/Время чека"].str[:10]

                    dates = df["дата"].unique()
                    date_str = dates

                    # df["Дата/Время чека"] = pd.to_datetime(df["Дата/Время чека"], format='%d.%m.%Y')

                    for date in date_str:
                        df["дата"] = pd.to_datetime(df["дата"], format="%d.%m.%Y")
                        day_df = df.loc[df["дата"] == pd.to_datetime(date, format="%d.%m.%Y")]
                        file_name = os.path.join(PUT + "♀Списания\\История\\", date + ".txt")
                        day_df.to_csv(file_name, sep="\t", encoding="utf-8", decimal=".", index=False)
                        MEMORY().mem_total(x="Разбиение по дням: " + os.path.basename(file))
                    os.remove(PUT + "NEW\\Списания\\" + file)
                gc.collect()
        return
    # Обработка файлов списания
    def sebest(self):
        print("Обработка сибестоймости")
        for root, dirs, files in os.walk(PUT + "NEW\\Сибестоемость\\"):
            for file in files:

                os.path.basename(file)
                file_path = os.path.join(root, file)
                df = pd.read_csv(file_path, sep="\t", encoding='utf-8',parse_dates=["Дата/Время чека"], date_format="%d.%m.%Y",  skiprows=2, names=("Дата/Время чека", "!МАГАЗИН!","номенклатура_1с", "Сибистоемость", "Вес_продаж", "прибыль"))
                RENAME().Rread(name_data=df, name_col="!МАГАЗИН!", name="Списания")
                df = df.loc[df["!МАГАЗИН!"] != "Итого"]
                df = df.loc[df["Дата/Время чека"] != "Итого"]
                l_mag = ("Микромаркет", "Экопункт", "Вендинг", "Итого")
                df["!МАГАЗИН!"] = df["!МАГАЗИН!"].fillna("Не известно")
                for w in l_mag:
                    df = df[~df["!МАГАЗИН!"].str.contains(w)]

                # "<Объект не найден>" и пустые удалить из столбца причина

                #df["Дата/Время чека"] = df["Дата/Время чека"].str[:10]

                date_str = df["Дата/Время чека"].unique()

                #date_str = dates.strftime("%d.%m.%Y")
                #print(dates)
                #df["Дата/Время чека"] = pd.to_datetime(df["Дата/Время чека"], format='%d.%m.%Y')

                for date in date_str :

                    df["Дата/Время чека"] = pd.to_datetime(df["Дата/Время чека"], format="%d.%m.%Y")
                    day_df = df.loc[df["Дата/Время чека"] == pd.to_datetime(date, format="%d.%m.%Y")]
                    file_name = os.path.join(PUT + "♀Сибестоемость\\Текущий месяц\\", date + ".txt")
                    day_df.to_csv(file_name, sep="\t", encoding="utf-8", decimal=".", index=False)
                    MEMORY().mem_total(x="Разбиение по дням: " + os.path.basename(file))
                #os.remove(PUT + "NEW\\Сибестоемость\\" +file)

            gc.collect()
    # Обработка сиестомости
    def sort_file(self):
        def sales():
            # Путь до папки текущего месяца
            month_folder_path = PUT + "♀Продажи\\текущий месяц\\"
            # Путь до папки текущего дня
            day_folder_path = PUT + "♀Продажи\\текущий день\\"
            # Получение текущей даты в формате "dd.mm.yyyy"
            current_date = datetime.datetime.now().strftime("%d.%m.%Y")
            # Перемещение файлов из папки текущего месяца в папку текущего дня, если такие файлы существуют
            for filename in os.listdir(month_folder_path):
                if current_date in filename:
                    # Файл содержит текущую дату, перемещаем его в папку текущего дня
                    src = os.path.join(month_folder_path, filename)
                    dst = os.path.join(day_folder_path, filename)
                    shutil.move(src, dst)
            # Перемещение файлов из папки текущего дня в папку текущего месяца, если такие файлы существуют
            for filename in os.listdir(day_folder_path):
                if current_date not in filename:
                    # Файл не содержит текущую дату, перемещаем его в папку текущего месяца
                    src = os.path.join(day_folder_path, filename)
                    dst = os.path.join(month_folder_path, filename)
                    shutil.move(src, dst)
            for filename in os.listdir(month_folder_path):
                if "2022" in filename:
                    file_path = os.path.join(month_folder_path, filename)
                    os.remove(file_path)
            return
        def check():
            # Путь до папки текущего месяца
            month_folder_path = PUT + "♀Чеки\\2023\\"
            # Путь до папки текущего дня
            day_folder_path = PUT + "♀Чеки\\Чеки текущий день\\"
            # Получение текущей даты в формате "dd.mm.yyyy"
            current_date = datetime.datetime.now().strftime("%d.%m.%Y")
            # Перемещение файлов из папки текущего месяца в папку текущего дня, если такие файлы существуют
            for filename in os.listdir(month_folder_path):
                if current_date in filename:
                    # Файл содержит текущую дату, перемещаем его в папку текущего дня
                    src = os.path.join(month_folder_path, filename)
                    dst = os.path.join(day_folder_path, filename)
                    shutil.move(src, dst)
            # Перемещение файлов из папки текущего дня в папку текущего месяца, если такие файлы существуют
            for filename in os.listdir(day_folder_path):
                if current_date not in filename:
                    # Файл не содержит текущую дату, перемещаем его в папку текущего месяца
                    src = os.path.join(day_folder_path, filename)
                    dst = os.path.join(month_folder_path, filename)
                    shutil.move(src, dst)
            for filename in os.listdir(month_folder_path):
                if "2022" in filename:
                    file_path = os.path.join(month_folder_path, filename)
                    os.remove(file_path)
            return
        def spipsania():
            # Путь до папки истории
            month_folder_path = PUT + "♀Списания\\История\\"
            # Путь до папки месяца
            day_folder_path = PUT + "♀Списания\\Текущий месяц\\"
            # Получение текущей даты в формате "dd.mm.yyyy"
            current_date = datetime.datetime.now()
            # Извлечение номера текущего месяца и года
            month_year = current_date.strftime("%m.%Y")
            # Перемещение файлов из папки текущего месяца в папку текущего дня, если такие файлы существуют
            for filename in os.listdir(month_folder_path):
                if month_year in filename:
                    # Файл содержит текущую дату, перемещаем его в папку месяца
                    src = os.path.join(month_folder_path, filename)
                    dst = os.path.join(day_folder_path, filename)
                    shutil.move(src, dst)

            # Получение текущей даты в формате "dd.mm.yyyy"
            current_date = datetime.datetime.now()
            # Извлечение номера текущего дня, месяца и года
            day_month_year = current_date.strftime("%d.%m.%Y")

            # Удаление файлов с текущей датой в названии и расширением .txt из папки day_folder_path
            for filename in os.listdir(day_folder_path):
                if filename.endswith('.txt') and day_month_year in filename:
                    file_path = os.path.join(day_folder_path, filename)
                    os.remove(file_path)
            return
        def original():
            # Путь до папки с оригинальными файлами
            original_files_path = r"C:\Users\lebedevvv\Desktop\Дашборд_бот\Selenium\Оригинальные файлы"

            # Путь до папки, в которую копировать файлы
            copy_files_path = r"C:\Users\lebedevvv\Desktop\Дашборд_бот\Selenium\исходники"

            # Перебираем все файлы в папке с оригинальными файлами
            for filename in os.listdir(original_files_path):
                # Если файл оканчивается на ".xlsx" или ".xls"
                if filename.endswith((".xlsx", ".xls")):
                    # Путь до оригинального файла
                    original_file_path = os.path.join(original_files_path, filename)
                    # Путь до копии файла
                    copy_file_path = os.path.join(copy_files_path, filename)
                    # Копируем файл
                    shutil.move(original_file_path, copy_file_path)
                    print(f"Файл {filename} скопирован в {copy_files_path}")
            return

        spipsania()
        sales()
        check()
        original()
    # сортировка файлов

class BOT_raschet:

    def tabl_bot_date(self):
        # определение рабочего дня или выходного
        def is_workday(date):
            ru_holidays = CustomRusHolidays()
            if date.weekday() >= 5:  # Если это суббота или воскресенье, то это выходной день.
                return False
            elif date in ru_holidays:  # Если это праздничный день, то это выходной день.
                return False
            else:
                return True  # Иначе это рабочий день.
        def save_date(date_list,name):
            with open(PUT + "BOT\\Temp\\даты_файлов\\" + name + '.txt', 'w') as f:
                f.write(str(date_list))

        # Чтение даты из файла
        with open(PUT + 'NEW\\дата обновления.txt', 'r') as f:
            date_str = f.readline().strip()
        format_date_str = '%d.%m.%Y'
        # Дата обновления
        MAX_DATE = datetime.datetime.strptime(date_str[:10], '%Y-%m-%d').date()
        TODEY = [MAX_DATE.strftime(format_date_str)]
        LAST_DATE = MAX_DATE - datetime.timedelta(days=1)
        print("Дата в файле\n",TODEY)
        print("Дата в файле\n", LAST_DATE)

        # тестовая
        test = 0
        if test ==1:
            MAX_DATE = datetime.datetime.strptime("2023-05-10", '%Y-%m-%d').date()
            LAST_DATE = MAX_DATE - datetime.timedelta(days=1)

        # ФОРМИРОВАНИЕ СПИСКА ВЧЕРАШНЕЙ ДАТЫ
        priznzk = ""
        VCHERA= []
        if is_workday(MAX_DATE):
            priznzk = "рабочий день"
            if is_workday(LAST_DATE):
                priznzk = 'середина недели'
                VCHERA.append(LAST_DATE.strftime(format_date_str))
            else:
                priznzk = "начало недели"
                while not is_workday(LAST_DATE):
                    VCHERA.append(LAST_DATE.strftime(format_date_str))
                    LAST_DATE -= datetime.timedelta(days=1)
                VCHERA.append(LAST_DATE.strftime(format_date_str))
        else:
            priznzk = "выходной день"
        # запись в файл
        print(priznzk)
        print(VCHERA)

        # region ТЕКУШИЙ МЕСЯЦ
        # Определяем первый день текущего месяца
        TODEY_month_min_day = MAX_DATE.replace(day=1)
        # список дат
        TODEY_month = pd.date_range(start=TODEY_month_min_day, end=MAX_DATE  - datetime.timedelta(days=1), freq='D').strftime(format_date_str).tolist()
        print("Текущий месяц\n",TODEY_month)
        # endregion

        # region ПРОШЛЫЙ МЕСЯЦ
        LAST_month_min_day = TODEY_month_min_day - pd.offsets.MonthBegin(1)
        # Определяем последний день прошлого месяца
        LAST_month_max_day = TODEY_month_min_day - pd.offsets.Day(1)
        # Создаем список дат прошлого месяца
        LAST_month = pd.date_range(start=LAST_month_min_day, end=LAST_month_max_day, freq='D').strftime(format_date_str).tolist()

        # Определяем количество дней в каждом месяце
        days_in_today_month = len(TODEY_month)
        days_in_last_month = len(LAST_month)
        # Если количество дней в прошлом месяце больше, отфильтруем его, чтобы было равное количество дней
        if days_in_last_month > days_in_today_month:
            LAST_month = LAST_month[:days_in_today_month]
        print("Прошлый месяц\n",LAST_month)

        # endregion
        save_date(priznzk, "priznzk")
        save_date(TODEY,"TODEY")
        save_date(VCHERA,"VCHERA")
        save_date(TODEY_month,"TODEY_month")
        save_date(LAST_month,"LAST_month")
        return TODEY, VCHERA, TODEY_month, LAST_month, priznzk
    # формирование списка дат
    def tabl_bot_file(self):
        TODEY, VCHERA, TODEY_month, LAST_month, priznzk = BOT_raschet().tabl_bot_date()
        Bot = pd.DataFrame()
        Bot_temp = pd.DataFrame()

        def date():
            # Преобразование строки в datetime
            prognoz_date = TODEY[0]
            date = datetime.datetime.strptime(prognoz_date, '%d.%m.%Y').date()

            # Количество дней в месяце
            month_day_total = calendar.monthrange(date.year, date.month)[1]

            # Прошедших дней с начала месяца
            day_last = date.day - 1

            # Оставшихся дней в месяце
            day_ostatok = month_day_total - date.day + 1

            print("Дней в месяце:", month_day_total)
            print("Прошло дней:", day_last)
            print("Осталось дней:", day_ostatok)

            return month_day_total,day_last,day_ostatok
            # вычисление оставшихся и будуюих дней продаж
        def col_n(x):
            len_float =["выручка","скидка"]
            FLOAT().float_colms(name_data=x, name_col=len_float)
            x.loc[x["Аналитика хозяйственной операции"] == "Дегустации", "Дегустации"] = x["списания"]
            x.loc[x["Аналитика хозяйственной операции"] == "Хозяйственные товары", "Хозяйственные товары"] = x["списания"]
            x.loc[(x["Аналитика хозяйственной операции"] == "Кражи")
                    | (x["Аналитика хозяйственной операции"] == "ПОТЕРИ")
                    | (x["Аналитика хозяйственной операции"] == "Питание сотрудников")
                    | (x["Аналитика хозяйственной операции"] == "Подарок покупателю (сервисная фишка)")
                    | (x["Аналитика хозяйственной операции"] == "Подарок покупателю (бонусы)")
                    | (x["Аналитика хозяйственной операции"] == "Дегустации") | (x["операция"] == "МАРКЕТИНГ (блогеры, фотосессии)"), "Списания_показатель"] = x["списания"]
            return x
        def poisk_sales(file):
            file_p = file + '.xlsx'
            folder1 = PUT + "♀Продажи\\текущий месяц\\"
            folder2 = PUT + "♀Продажи\\2023\\"
            folder3 = PUT + "♀Продажи\\текущий день\\"
            for folder in [folder1, folder2, folder3]:

                file_path = os.path.join(folder, file_p)
                if os.path.exists(file_path):
                    x = pd.read_excel(file_path, parse_dates=["Дата/Время чека"], date_format='%Y-%m-%d %H:%M:%S')
                    y = x[["Дата/Время чека","!МАГАЗИН!","номенклатура_1с","Стоимость позиции","Сумма скидки"]]
                    del x
                    gc.collect()
                    # перименование столбцов
                    y = y.rename(columns={"!МАГАЗИН!":"магазин","номенклатура_1с":"номенклатура",
                                          "Стоимость позиции":"выручка","Сумма скидки":"скидка","Дата/Время чека":"дата"})

                    # перевод во float
                    len_float = ["выручка","скидка"]
                    FLOAT().float_colms(name_data=y,name_col=len_float)
                    # групировка таблицы
                    y= y.groupby(["магазин","номенклатура","дата"],
                                  as_index=False).agg(
                        {"выручка": "sum", "скидка": "sum"}).reset_index(drop=True)
                    return y
            # не ипользуется, для товара дня
        def poisk_check(file):
            file_p = file + '.xlsx'
            folder1 = PUT + "♀Чеки\\2023\\"
            folder2 = PUT + "♀Чеки\\Чеки текущий день\\"
            for folder in [folder1, folder2]:
                file_path = os.path.join(folder, file_p)
                if os.path.exists(file_path):
                    x = pd.read_excel(file_path, parse_dates=["дата"], date_format='%Y-%m-%d %H:%M:%S')
                    y = x[["дата", "!МАГАЗИН!","выручка","Количество чеков"]]
                    del x
                    gc.collect()
                    # перименование столбцов
                    y = y.rename(columns={"Количество чеков":"количество чеков"})
                    FLOAT().float_colm(name_data=y, name_col= "количество чеков")
                    y['месяц'] = pd.to_datetime(y['дата']).dt.month
                    return y
            # продажи и чеки

        def poisk_spisania(file):
            file_p = file + '.csv'
            folder1 = PUT + "♀Списания\\Текущий месяц\\"
            folder2 = PUT + "♀Списания\\История\\"
            for folder in [folder1, folder2]:

                file_path = os.path.join(folder, file_p)
                print(file_path)
                if os.path.exists(file_path):
                    x = pd.read_csv(file_path, parse_dates=["дата"], date_format='%Y-%m-%d')

                    y = x[["дата","!МАГАЗИН!", "Аналитика хозяйственной операции", "Номенклатура", "Сумма","отбор"]]
                    del x
                    gc.collect()
                    # перименование столбцов
                    y = y.rename(columns={"!МАГАЗИН!": "магазин", "номенклатура_1с": "номенклатура"})

                    col_n(y)
                    # перевод во float
                    len_float = ["Дегустации", "Хозяйственные товары","Списания_показатель"]
                    FLOAT().float_colms(name_data=y, name_col=len_float)
                    # групировка таблицы
                    y = y.groupby(["магазин", "номенклатура", "дата"],
                                  as_index=False).agg(
                        {"Дегустации":  "Хозяйственные товары", "Списания_показатель" : "sum"}).reset_index(drop=True)

                    return y
            # списания

        def plan_month():
            # загрузка планов
            x = pd.read_excel(PUT + "♀Планы\\Планы ДЛЯ ДАШБОРДА.xlsx",parse_dates=["дата"], date_format='%d.%m.%Y')
            x = x[["!МАГАЗИН!", "ПЛАН", "дата","Показатель"]]
            FLOAT().float_colm(name_data=x, name_col="ПЛАН")
            x["месяц"] = pd.to_datetime(x["дата"]).dt.month
            x.loc[x["Показатель"] == "Выручка", "план_выручка"] = x["ПЛАН"]
            x.loc[x["Показатель"] == "Средний чек", "план_cредний_чек"] = x["ПЛАН"]
            x.loc[x["Показатель"] == "Кол чеков", "план_кол_чеков"] = x["ПЛАН"]
            x = x.drop(["ПЛАН", "Показатель","дата"], axis=1)
            x = x.groupby(["!МАГАЗИН!", "месяц"]).sum().reset_index()

            """sales_day = pd.merge(sales_day, sales_total, on=["!МАГАЗИН!", 'месяц'], how='left')

            sales_day = pd.merge(sales_day, x, on=["!МАГАЗИН!", 'месяц'], how='left')

            print(sales_day)
            # Рассчитываем дневной план
            sales_day["дневной_план_выручка"] = (sales_day["план_выручка"] - sales_day["выручка_за_текущий_месяц"]) / days_left
            sales_day["дневной_план_кол_чеков"] = (sales_day["план_кол_чеков"] -sales_day["чеков_за_текущий_месяц"]) /days_left
            #sales_day["дневной_cредний_чек"] = sales_day["дневной_план_выручка"] / sales_day["дневной_план_кол_чеков"]


            x.to_excel(PUT + "BOT\\temp\\" + "планы.xlsx", index=False)
            #x = x[["дата","!МАГАЗИН!","выручка","количество чеков","план_выручка","план_кол_чеков","план_cредний_чек","дневной_план_выручка","дневной_план_кол_чеков","дневной_cредний_чек"]]"""
            return x

        # region Сохранение временного файла с общими продажами за ткущий месяц
        for file in TODEY_month:
            print("TODEY_month")
            x = poisk_check(file=str(file))
            Bot_temp = pd.concat([Bot_temp, x], axis=0, ).reset_index(drop=True)
        Bot_temp = Bot_temp.groupby(["!МАГАЗИН!", "месяц"],
                          as_index=False).agg(
            {"выручка": "sum", "количество чеков": "sum"}).reset_index(drop=True)
        Bot_temp.to_excel(PUT + "BOT\\temp\\" + "Выручка за месяц.xlsx", index=False)
        # endregion
        def todey():
            for file in TODEY:
                print("Формирование файла теущего дня: ", file)
                sales = poisk_check(file=str(file))
                total_sales_month = pd.read_excel(PUT + "BOT\\temp\\" + "Выручка за месяц.xlsx")
                total_sales_month = total_sales_month.rename(columns={"выручка": "выручка_total", "количество чеков": "чеков_total"})
                sales = pd.merge(sales, total_sales_month, on=["!МАГАЗИН!", 'месяц'], how='left')
                plan = plan_month()
                sales = pd.merge(sales, plan, on=["!МАГАЗИН!", 'месяц'], how='left')

                month_day_total, day_last, day_ostatok  = date()
                sales["дневной_план_выручка"] = (sales["план_выручка"] - sales["выручка_total"]) / day_ostatok
                sales["дневной_план_кол_чеков"] = (sales["план_кол_чеков"] - sales["чеков_total"]) / day_ostatok
                # sales_day["дневной_cредний_чек"] = sales_day["дневной_план_выручка"] / sales_day["дневной_план_кол_чеков"]
                sales   = sales.round()
                ty = RENAME().TY_Spravochnik()
                sales = sales.merge(ty, on=["!МАГАЗИН!"], how="left").reset_index(drop=True)
                sales = sales.drop([ "дата","месяц"], axis=1)

                sales.to_excel(PUT + "BOT\\Temp\\Файлы_данных_бота\\" + "TODEY.xlsx", index=False)

                del file,total_sales_month,month_day_total, day_last, day_ostatok,plan,ty
                gc.collect()
                MEMORY().mem_total(x="TODEY")
                print(sales)
            return
        todey()

        def vchera():
            for file in VCHERA:
                print("Формирование файла вчерашнего дня: ", file)
                sales = poisk_check(file=str(file))
                total_sales_month = pd.read_excel(PUT + "BOT\\temp\\" + "Выручка за месяц.xlsx")
                total_sales_month = total_sales_month.rename(columns={"выручка": "выручка_total", "количество чеков": "чеков_total"})
                sales = pd.merge(sales, total_sales_month, on=["!МАГАЗИН!", 'месяц'], how='left')
                plan = plan_month()
                sales = pd.merge(sales, plan, on=["!МАГАЗИН!", 'месяц'], how='left')

                month_day_total, day_last, day_ostatok  = date()
                sales["дневной_план_выручка"] = (sales["план_выручка"] - sales["выручка_total"]) / day_ostatok
                sales["дневной_план_кол_чеков"] = (sales["план_кол_чеков"] - sales["чеков_total"]) / day_ostatok
                # sales_day["дневной_cредний_чек"] = sales_day["дневной_план_выручка"] / sales_day["дневной_план_кол_чеков"]
                sales   = sales.round()
                ty = RENAME().TY_Spravochnik()
                sales = sales.merge(ty, on=["!МАГАЗИН!"], how="left").reset_index(drop=True)
                sales = sales.drop([ "дата","месяц"], axis=1)

                sales.to_excel(PUT + "BOT\\Temp\\Файлы_данных_бота\\" + "VCHERA.xlsx", index=False)

                del file,total_sales_month,month_day_total, day_last, day_ostatok,plan,ty
                gc.collect()
                MEMORY().mem_total(x="VCHERA")
                print(sales)
            return
        vchera()









        """



        # загрузка планов
        for file in TODEY_month:
            print("TODEY_month")
            x = poisk_check(file=str(file))
            Bot = pd.concat([Bot, x], axis=0, ).reset_index(drop=True)

            total_sales_month = pd.read_excel(PUT + "BOT\\temp\\" + "Выручка за месяц.xlsx")
            x = paln(dat_total=total_sales_month, dat_day=x)

            Bot = pd.concat([Bot, x], axis=0,).reset_index(drop=True)
            del file
            gc.collect()
            MEMORY().mem_total(x="TODEY_month")

        Bot = Bot.groupby(["!МАГАЗИН!","месяц"],
                          as_index=False).agg(
            {"выручка_за_текущий_день": "sum","чеков_за_текущий_день": "sum","выручка_за_текущий_месяц": "sum","чеков_за_текущий_месяц": "sum",
             "план_выручка":"mean","план_cредний_чек":"mean","план_кол_чеков":"mean","дневной_план_выручка":"sum","дневной_план_кол_чеков":"sum"}).reset_index(drop=True)




        for file in TODEY:
            print("TTODEY")
            x = poisk_check(file=str(file))
            total_sales_month = pd.read_excel(PUT + "BOT\\temp\\" + "Выручка за месяц.xlsx")
            x = paln(dat_total = total_sales_month, dat_day= x )

            #xp = pd.merge(y, p, on=["!МАГАЗИН!",'месяц'])
            #z = poisk_spisania(file=str(file))
            #print(xp)
            #xp = xp[["дата","!МАГАЗИН!","выручка","количество чеков"]]
            x["отбор"] = "TODEY"
            Bot = pd.concat([Bot, x], axis=0,).reset_index(drop=True)
            #Bot = Bot.drop([ "дата"], axis=1)
            print(Bot)
            del file,x,total_sales_month
            gc.collect()
            MEMORY().mem_total(x="TODEY")

        for file in VCHERA:
            X = poisk(file=str(file), otbor="VCHERA")
            Bot = pd.concat([Bot, X], axis=0,).reset_index(drop=True)
            del file
            gc.collect()
            MEMORY().mem_total(x="VCHERA")



        for file in LAST_month:
            X = poisk(file=str(file), otbor="LAST_month")
            Bot = pd.concat([Bot, X], axis=0,).reset_index(drop=True)
            del file
            gc.collect()
            MEMORY().mem_total(x="LAST_month")
        Bot = Bot.groupby(["!МАГАЗИН!", "номенклатура", "отбор", "операция"],
                      as_index=False).agg(
            {"выручка": "sum", "скидка": "sum", "списания": "sum", "Дегустации": "sum", "Хозяйственные товары": "sum",
             "Списания_показатель": "sum"}).reset_index(drop=True)

        # Добавление ТУ
        MEMORY().mem_total(x="3")
        ty = RENAME().TY_Spravochnik()
        Bot = Bot.merge(ty, on=["!МАГАЗИН!"], how="left").reset_index(drop=True)
        del ty,
        gc.collect()

        # переисенование менеджеров
        Ln_tip = {'Турова Анна Сергеевна': 'Турова А.С',
                  'Баранова Лариса Викторовна': 'Баранова Л.В',
                  'Геровский Иван Владимирович': 'Геровский И.В',
                  'Изотов Вадим Валентинович': 'Изотов В.В',
                  'Томск': 'Томск',
                  'Павлова Анна Александровна': 'Павлова А.А',
                  'Бедарева Наталья Геннадьевна': 'Бедарева Н.Г',
                  'Сергеев Алексей Сергеевич': 'Сергеев А.С',
                  'Карпова Екатерина Эдуардовна': 'Карпова Е.Э'}
        Bot["Менеджер"] = Bot["Менеджер"].map(Ln_tip)

        Bot.to_excel(PUT + "BOT\\temp\\" + "Bot_v2test.xlsx", index=False)"""
        return Bot
    # создание таблиц


    def raschet(self):
        def DATE():
            BOT_raschet().tabl_bot_file()
            # Определение даты обновления дашборда
            now = datetime.datetime.now()
            NEW_date = (now.hour + 1) if now.minute >= 30 else (now.hour)
            NEW_date = datetime.datetime(now.year, now.month, now.day, NEW_date, 0, 0)
            NEW_date = NEW_date.strftime("%H:%M")
            print("Текущее время (округлено до часа):", NEW_date)
            current_time = f'🕙 Данные на : {NEW_date}\n'

            # список дат из файла TODEY_month
            with open(PUT + "Bot\\temp\\даты файлов\\TODEY.txt", 'r') as f:
                dates = f.read().strip()[1:-1].split(', ')

            # Формируем сообщение TODEY_month
            TODEY_date = f'Результаты прошлого дня:\n'
            for date in dates:
                TODEY_date +=  f'•\u200E {date[1:-1]}\n'
            print(TODEY_date)

            # список дат из файла TODEY_month
            with open(PUT + "Bot\\temp\\даты файлов\\VCHERA.txt", 'r') as f:
                dates = f.read().strip()[1:-1].split(', ')

            # Формируем сообщение TODEY_month
            VCHERA_date = f'Результаты прошедших выходных:\n'
            for date in dates:
                VCHERA_date += f'•\u200E {date[1:-1]}\n'
            print(VCHERA_date)
            return VCHERA_date,TODEY_date
        # формирование строки с временем
        DATE()
        #now = datetime.now()
        #current_time = now.strftime("%H:%M:%S")
        #f = "10:00:00"
        #df = pd.read_excel(PUT + "Bot\\temp\\" + "Сводная_бот.xlsx")




        return

    def tovar_day(self):
        return
    # отвечает за товар дня
        # расчет для бота


#BOT_raschet().tabl_bot_date()
#BOT_raschet().tabl_bot_file()


#NEW_data().selenium_day_Spisania()
#NEW_data().sort_file()
#NEW_data().sebest()
NEW_data().Obrabotka()
#NEW_data().sort_file()
#