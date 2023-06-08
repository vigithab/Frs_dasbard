import datetime
import os
import pandas as pd
import gc
import time
from Bot_FRS_v2.INI import ini
import numpy as np
from Levenshtein import distance
from Bot_FRS_v2.INI import rename
from Bot_FRS_v2.INI import Float
from Bot_FRS_v2.GooGL_TBL import Google as g


pd.set_option("expand_frame_repr", False)
pd.set_option('display.max_colwidth', None)
PUT = ini.PUT


class PERSONAL():
    def history(self):
        def get_closest_match(name, valid_names):
            min_distance = float('inf')
            closest_name = None

            for valid_name in valid_names:
                dist = distance(name, valid_name)
                if dist < min_distance:
                    min_distance = dist
                    closest_name = valid_name

            return closest_name
        personal = pd.read_excel(PUT+ "Персонал\\Копия Укомплектованность ФРС.xlsx",dtype={"!МАГАЗИН!": str})  # Датафрейм с корявыми названиями магазинов
        # Преобразование значений столбца в строки
        personal['!МАГАЗИН!'] = personal['!МАГАЗИН!'].astype(str)
        spqr, sprav_magaz = rename.RENAME().magazin_info()  # Датафрейм с правильными названиями магазинов
        # Отфильтровать непустые строки в столбце '!МАГАЗИН!'
        non_empty_rows = personal['!МАГАЗИН!'].notnull()
        # Создание нового столбца с правильными названиями только для непустых строк
        personal.loc[non_empty_rows, 'Правильное название'] = personal.loc[non_empty_rows, '!МАГАЗИН!'].apply(
            lambda x: get_closest_match(x, spqr['!МАГАЗИН!']))

        personal = personal.drop(columns="!МАГАЗИН!")
        personal = personal.rename(columns={"Ответственный за подбор/информацию":"Ответственный за персонал","Правильное название":"!МАГАЗИН!","Плановая чис-ть":"Плановая численность","Фактич.чис-ть":"Фактическая численность",
                                            "стаж-ка":"Стажеровка","Причина некомплекта ":"Причина некомплекта"})

        personal = personal[["Ответственный за персонал","Неделя","!МАГАЗИН!","Плановая численность","Фактическая численность","Принято","Уволено","Кол-во вакансий","м/о","Стажеровка","студентов работает","Причина некомплекта"]]
        ln =["Плановая численность","Фактическая численность","Принято","Уволено","Кол-во вакансий","м/о","Стажеровка","студентов работает"]
        Float.FLOAT().float_colms(name_data=personal,name_col=ln)
        personal['Год'] = "2023"
        personal['Неделя'] = personal['Неделя'].apply(lambda x: str(x).zfill(2))
        # Преобразование номера недели и года в дату начала недели
        personal['Дата начала недели'] = pd.to_datetime(personal['Год'] + personal['Неделя'].astype(str) + '-1', format='%Y%W-%w')
        personal['Дата конца недели'] = personal['Дата начала недели'] + pd.DateOffset(days=6)
        # Извлечение информации о месяце из даты начала недели
        personal['Месяц'] = personal['Дата начала недели'].dt.month

        personal["Дата начала недели"] = pd.to_datetime(personal["Дата начала недели"], format="%Y-%m-%d")
        personal["Дата конца недели"] = pd.to_datetime(personal["Дата начала недели"], format="%Y-%m-%d")
        personal["Дата начала недели"] = personal["Дата начала недели"].dt.strftime("%d.%m.%Y")
        personal["Дата конца недели"] = personal["Дата конца недели"].dt.strftime("%d.%m.%Y")
        personal["Диапозон"] = personal["Дата начала недели"].astype(str) + " - " + personal[
            "Дата конца недели"].astype(str)



        personal =  personal[
            ["Дата начала недели", "Дата конца недели", "Диапозон", "Неделя", "Ответственный за персонал", "Неделя",
             "!МАГАЗИН!", "Плановая численность", "Фактическая численность", "Принято", "Уволено", "Кол-во вакансий",
             "м/о", "Стажеровка", "студентов работает", "Причина некомплекта"]]
        personal.to_csv(PUT + "Персонал\\Data\\персонал.csv", sep=";",encoding="utf-8",index=False)
        print(personal)
    def new_data(self):
        spqr, sprav_magaz = rename.RENAME().magazin_info()
        sprav_magaz = sprav_magaz.loc[sprav_magaz["Старые/Новые"] != "ЗАКРЫТЫЕ"]
        sprav_magaz = sprav_magaz.loc[sprav_magaz['Ответственный за персонал'].notnull()]
        sprav_magaz = sprav_magaz[['Ответственный за персонал', '!МАГАЗИН!']]
        ln = ["Плановая численность","Фактическая численность","Принято","Уволено","Кол-во вакансий","м/о","Стажеровка","студентов работает","Причина некомплекта"]
        for i in ln:
            sprav_magaz[i]= np.nan
        sprav_magaz.fillna('', inplace=True)
        week_number,start_of_week_str,end_of_week_str = ini.weck()
        week_info = f"Данные будут записаны для недели № {week_number} с: {start_of_week_str} по: {end_of_week_str}"
        g.tbl().record(name="Укомплектованность ФРС", name_df=sprav_magaz, sheet_name="ПЕРСОНАЛ", zagolovok = 1, zagolovok_name =week_info)
    def tudey(self):
        try:
            date_weck = pd.read_excel("https://docs.google.com/spreadsheets/d/13tsxHb82mRcyQiYn78EGh7uV_6sUiq1zcAW3mo2aIFQ/export?exportFormat=xlsx",skiprows=1)
        except:
            try:
                time.sleep(240)
                date_weck = pd.read_excel(
                    "https://docs.google.com/spreadsheets/d/13tsxHb82mRcyQiYn78EGh7uV_6sUiq1zcAW3mo2aIFQ/export?exportFormat=xlsx",skiprows=1)
            except:
                return

        week_number, start_of_week_str, end_of_week_str = ini.weck()
        date_weck["Неделя"] = week_number
        date_weck['Неделя'] = date_weck['Неделя'].apply(lambda x: str(x).zfill(2))

        date_weck["Дата начала недели"]= pd.to_datetime(start_of_week_str, format="%Y-%m-%d")
        date_weck["Дата конца недели"] =  pd.to_datetime(end_of_week_str, format="%Y-%m-%d")
        date_weck["Дата начала недели"] = date_weck["Дата начала недели"].dt.strftime("%d.%m.%Y")
        date_weck["Дата конца недели"] = date_weck["Дата конца недели"].dt.strftime("%d.%m.%Y")

        date_weck["Диапозон"] = date_weck["Дата начала недели"].astype(str) + " - " + date_weck["Дата конца недели"].astype(str)
        date_weck = date_weck[["Дата начала недели","Дата конца недели","Диапозон", "Неделя", "Ответственный за персонал","Неделя","!МАГАЗИН!","Плановая численность","Фактическая численность","Принято","Уволено","Кол-во вакансий","м/о","Стажеровка","студентов работает","Причина некомплекта"]]
        print(date_weck)





#PERSONAL().new_data()
#PERSONAL().history()
PERSONAL().tudey()