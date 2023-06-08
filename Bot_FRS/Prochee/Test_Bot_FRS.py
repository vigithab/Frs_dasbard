
#import psutil
import shutil
import xlsxwriter
from pandas.tseries.offsets import DateOffset
from datetime import datetime, timedelta, time, date
from pandas.tseries.offsets import MonthBegin
import time as t
import os
import pandas as pd
import sys
import math
import gc
import requests
# from memory_profiler import profile
import numpy as np
import calendar

#import bot_TELEGRAM as bot
#import GOOGL as gg
from dateutil import parser
from dateutil import relativedelta
from dateutil import rrule
import datetime
from Bot_FRS_.new_data import set_cd as sd
from Bot_FRS_.new_data import setreteyl as set
from Bot_FRS_.new_data import sort_file as sort
from Bot_FRS_.inf import memory as memory
from Bot_FRS_.bot_telegram import Bot as bot
from Bot_FRS_.rassilka import voropaev_degustaciya as voropaev


pd.set_option("expand_frame_repr", False)
pd.set_option('display.max_colwidth', None)
gc.enable()
TY_GROP = 00
TEST_BOT = 1
ta = "22:00:00"
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
        bot.BOT().bot_mes(mes="Обновление данных....")
        sd.NEW_DATA().setevoy()
        sd.NEW_DATA().setevoy_spisania()
        sd.NEW_DATA().setevoy_degustacia()
        set.SET().Set_obrabotka()

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
        #NEW_data().sort_file()
        sort.sort_file()
        NEW_data().sebest()
        bot.BOT_raschet().tabl_bot_file()
        voropaev.Degustacia().sotka()
        return
    # основнй файл отвечающий за обработку
    def Set_sales(self, name_datafreme, name_file):
        def sravnenie_1c(data):

            file = PUT + "NEW\\ОБРАБОТКА ОШИБОК\\♦разница_1с.xlsx"
            data = data.loc[data["Разница данные set/1 с"] != 0]
            if os.path.exists(file):
                existing_data = pd.read_excel(file)
                existing_dates_stores = existing_data[["Дата/Время чека", "!МАГАЗИН!"]]

                for index, row in data.iterrows():
                    # Проверяем существование каждой строки в существующем файле
                    existing_row = existing_data.loc[
                        (existing_data["Дата/Время чека"] == row["Дата/Время чека"]) &
                        (existing_data["!МАГАЗИН!"] == row["!МАГАЗИН!"])
                        ]

                    if existing_row.empty:
                        # Записываем новую строку, если ее нет в файле
                        existing_data = existing_data.append(row)
                    else:
                        # Если строка уже существует, перезаписываем ее
                        existing_data.loc[existing_row.index] = row

                existing_data.to_excel(file, index=False)
            else:
                data.to_excel(file, index=False)
        bot.BOT().bot_mes(mes="Формирование файлов продаж....")

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
        spravka_nom = pd.read_csv(PUT + "Справочники\\номенклатура\\Справочник номеклатуры.txt", sep="\t", skiprows=1, encoding="utf-8",
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



        # Получение текущей даты
        current_date = datetime.date.today()
        current_date_str = current_date.strftime("%d.%m.%Y")
        if str(name_file[:-5]) == str(current_date_str):
            print("Обрабатывается текущий день - пропустить сравнение с 1 с")
            pass  # Ничего не делать
        else:
            # Сгруппируем данные по номенклатуре и посчитаем сумму по столбцу "сумма"
            sum_dostavka_im = sales_day_sales.groupby("Наименование товара")["Стоимость позиции"].sum()
            # Получим сумму по номенклатуре "Доставка ИМ" "Пельмени Московские, кат Б, зам, вес"
            sum_dostavka_im = sum_dostavka_im.get("Доставка ИМ", 0)


            raznica_1c = pd.read_csv(PUT + "NEW\\ОБРАБОТКА ОШИБОК\\Продажи 1с по магазинам для проверки\\Финрез лебедев ПРоверка (TXT).txt",sep="\t",encoding="utf-8",
                                     skiprows=2, names=("Дата/Время чека","!МАГАЗИН!","выручка 1с","Сумма возврата"))
            raznica_1c = raznica_1c.drop("Сумма возврата", axis=1)


            raznica_1c = raznica_1c.loc[raznica_1c["Дата/Время чека"]!="Итого"]
            raznica_1c["Дата/Время чека"] = pd.to_datetime(raznica_1c["Дата/Время чека"], format="%d.%m.%Y")
            FLOAT().float_colm(name_data=raznica_1c, name_col="выручка 1с")
            RENAME().Rread(name_data=raznica_1c, name_col="!МАГАЗИН!", name="Суммы 1с")
            #infovision = infovision.rename(columns={'Магазин': "!МАГАЗИН!","Дата": "Дата/Время чека"})
            setret = sales_day_sales[["!МАГАЗИН!", "Дата/Время чека", "Стоимость позиции"]].copy()
            setret = setret.rename(columns={'Стоимость позиции': "выручка set"})
            setret = setret.groupby(["!МАГАЗИН!", "Дата/Время чека"], as_index=False) \
                .agg({"выручка set": "sum"}) \
                .sort_values("!МАГАЗИН!", ascending=False).reset_index(drop=True)


            setret = setret.merge(raznica_1c, on=['!МАГАЗИН!', "Дата/Время чека"], how="left")

            setret["Разница данные set/1 с"] = setret["выручка set"]- setret["выручка 1с"]

            sum_1c_dh = setret["Разница данные set/1 с"].sum()

            # Запись разницы в фаил
            sravnenie_1c(setret)
            # Отправка сообщения ботом
            mes = os.path.basename(name_file)[:-5] + "\nДо и после оработки:" + str(er1.round() - er.round()) +\
                  "\nРазница c 1C: " +str(sum_1c_dh.round()) + "\nИнтернет магазин: "+str(sum_dostavka_im)
            bot.BOT().bot_mes(mes=mes)

        return sales_day_sales
    # обработка файлов продаж
    def selenium_day_chek(self, name_datafreme, name_file):
        memory.MEMORY().mem_total(x="Формирование чеков: ")
        bot.BOT().bot_mes(mes="Формирование файлов чеков....")
        def cnevk(tip):
            sales_day_cehk = name_datafreme[["Тип","!МАГАЗИН!", "ID", "Дата/Время чека", "Касса", "Чек", "Стоимость позиции", "Код товара","Смена"]]
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

            memory.MEMORY().mem_total(x="Обработан - Фаил чеков: " + str(name_file))
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

        print("Обработка списания")
        if tame_Filter < ta:
            bot.BOT().bot_mes(mes="Обработка списания....")
            """# Папка для поиска файла
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
            shutil.copy(latest_file, destination_folder)"""

            for root, dirs, files in os.walk(PUT + "NEW\\Списания\\"):
                for file in files:
                    os.path.basename(file)
                    file_path = os.path.join(root, file)
                    try:
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

                        df = df.rename(columns={"Регистратор.Причина списания": "Причина списания"})
                        df['Причина списания'] = df['Причина списания'].fillna('не определено')
                        df.loc[df['Причина списания'].str.contains('<Объект не найден>'), 'Причина списания'] = 'не определено'
                        df = df.loc[df["дата"] != "Итого"]
                        df = df.loc[df["!МАГАЗИН!"] != "Итого"]

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
                            memory.MEMORY().mem_total(x="Разбиение по дням: " + os.path.basename(file))
                        try:
                            os.remove(PUT + "NEW\\Списания\\" + file)
                        except:
                            print("Нет файл для удаления")
                    except:
                        bot.BOT().bot_mes(mes="Фаил списания не найден")
                gc.collect()
        return
    # Обработка файлов списания
    def sebest(self):
        print("Обработка сибестоймости")
        bot.BOT().bot_mes(mes="Обработка сибестоемости....")
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
                    memory.MEMORY().mem_total(x="Разбиение по дням: " + os.path.basename(file))
                #os.remove(PUT + "NEW\\Сибестоемость\\" +file)

            gc.collect()
    # Обработка сиестомости

class error():
    def out(self):
        # Ожидание ввода от пользователя или 1 час задержки
        start_time = t.time()
        user_input = input("вести 'ok', чтобы завершить программу, или подождите 1 час: ")
        # Проверка ввода пользователя или времени задержки
        if user_input.lower() == "ok" or t.time() - start_time >= 3600:
            # Завершение программы
            print("Программа завершается.")
        else:
            # Продолжение выполнения программы
            print("Программа продолжается.")
    def error_log(self):
        try:
            # который может вызвать ошибку
            # Например:
            result = 10 / 0
        except Exception as e:
            # Сохранение текста ошибки в файл
            error_message = str(e)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            formatted_error = f"[{timestamp}] {error_message}\n"
            with open(PUT + "NEW\\ОБРАБОТКА ОШИБОК\\Error_log.txt", "a") as file:
                file.write(formatted_error)
            # Другие действия при возникновении ошибки
            # Например, вывод сообщения об ошибке
            print("Произошла ошибка:", error_message)
    # обработка ошибок



#BOT_raschet().tabl_bot_date()
#BOT_raschet().tabl_bot_file()


#NEW_data().selenium_day_Spisania()
#NEW_data().sort_file()
#NEW_data().sebest()
NEW_data().Obrabotka()
#NEW_data().sort_file()

#