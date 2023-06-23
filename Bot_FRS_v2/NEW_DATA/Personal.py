import sys
sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON\venv\Lib\site-packages")
sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON")
import datetime
import os
import pandas as pd
import gc
import time
from Bot_FRS_v2.INI import ini
import numpy as np
from datetime import datetime, timedelta
from Levenshtein import distance
from Bot_FRS_v2.INI import rename
from Bot_FRS_v2.INI import Float
from Bot_FRS_v2.GooGL_TBL import Google as g
from Bot_FRS_v2.BOT_TELEGRAM import BOT


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

        personal = pd.read_excel(PUT + "Персонал\\22.xlsx",dtype={"МАГАЗИН": str})  # Датафрейм с корявыми названиями магазинов
        # Преобразование значений столбца в строки
        personal = personal.drop_duplicates()

        personal['МАГАЗИН'] = personal['МАГАЗИН'].astype(str)
        spqr, sprav_magaz = rename.RENAME().magazin_info()  # Датафрейм с правильными названиями магазинов

        # Отфильтровать непустые строки в столбце '!МАГАЗИН!'
        non_empty_rows = personal['МАГАЗИН'].notnull()
        # Создание нового столбца с правильными названиями только для непустых строк
        personal.loc[non_empty_rows, 'Правильное название'] = personal.loc[non_empty_rows, 'МАГАЗИН'].apply(
            lambda x: get_closest_match(x, sprav_magaz['МАГАЗИН']))
        print(personal)
        personal = personal.rename(columns={"МАГАЗИН":"3"})
        personal = personal.rename(columns={"Ответственный за подбор/информацию":"Ответственный за персонал","Правильное название":"МАГАЗИН","Плановая чис-ть":"Плановая численность","Фактич.чис-ть":"Фактическая численность",
                                            "стаж-ка":"Стажеровка","Причина некомплекта ":"Причина некомплекта"})

        personal = personal[["Ответственный за персонал","Неделя","МАГАЗИН","3","Плановая численность","Фактическая численность","Принято","Уволено","Кол-во вакансий","м/о","Стажеровка","студентов работает","Причина некомплекта"]]
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
             "МАГАЗИН","3", "Плановая численность", "Фактическая численность", "Принято", "Уволено", "Кол-во вакансий",
             "м/о", "Стажеровка", "студентов работает", "Причина некомплекта"]]
        personal.to_csv(PUT + "Персонал\\Data\\персонал.csv", sep=";",encoding="utf-8",index=False)
        print(personal[50:])
    def tudey(self):
        BOT.BOT().bot_mes_html(mes="Обработака ФОТ....", silka=0)
        def open_goggle():
            try:
                print("скачтвание Файла")
                date_weck = pd.read_excel("https://docs.google.com/spreadsheets/d/13tsxHb82mRcyQiYn78EGh7uV_6sUiq1zcAW3mo2aIFQ/export?exportFormat=xlsx",skiprows=1)
            except:
                try:
                    print("ошибка")
                    time.sleep(360)
                    date_weck = pd.read_excel(
                        "https://docs.google.com/spreadsheets/d/13tsxHb82mRcyQiYn78EGh7uV_6sUiq1zcAW3mo2aIFQ/export?exportFormat=xlsx",skiprows=1)
                except:
                    return
            columns_srt = date_weck.columns.tolist()
            date_weck["дата"] = ini.dat_seychas.strftime("%d.%m.%Y")
            date_weck.to_csv(PUT + "Персонал\\Data\\" +
                        str(ini.dat_seychas.strftime("%d.%m.%Y")) + ".csv",
                        encoding="utf-8",
                        sep=';', index=False,
                        decimal=",")
            return date_weck,columns_srt
        def new_magain():
            spqr, sprav_magaz, open_mag = rename.RENAME().magazin_info()
            sprav_magaz = sprav_magaz.loc[ (sprav_magaz["Старые/Новые"] == "Новые ТТ") |
                                          (sprav_magaz["Старые/Новые"] == "Релокация")|
                                          (sprav_magaz["Старые/Новые"] == "Без новых ТТ") |
                                           (sprav_magaz["Старые/Новые"] == "Не магазин")]
            open_mag = sprav_magaz[["МАГАЗИН","Ответственный за персонал"]]
            return open_mag

        df_personal,columns_srt = open_goggle()
        df_personal = df_personal.rename(columns={"Ответственный за персонал":"Ответственный за персонал_del"})
        new_magain = new_magain()

        new_magaz = pd.merge(df_personal,new_magain, on='МАГАЗИН', how='outer')
        l_mag = ["Томск", "Северск"]
        for w in l_mag:
            new_magaz =  new_magaz[~ new_magaz["МАГАЗИН"].str.contains(w)].reset_index(drop=True)
        new_magaz.loc[new_magaz["Ответственный за персонал"].isnull(), "Ответственный за персонал"] = "НЕ НАЗНАЧЕН"

        new_magaz = new_magaz.reindex(columns_srt, axis=1)
        d1 = ini.dat_seychas + timedelta(days=1)
        d1 = d1.strftime("%d.%m.%Y")
        d = ini.dat_seychas.strftime("%d.%m.%Y")
        week_info = f"Данные будут сохранены для даты: {str(d1)} (сохранение данных ежедневно в 23:00)"

        new_magaz.fillna('', inplace=True)
        g.tbl().record(name="Укомплектованность ФРС", name_df=new_magaz, sheet_name="ПЕРСОНАЛ", zagolovok = 1, zagolovok_name =week_info)
        BOT.BOT().bot_mes_html(mes="Обработака ФОТ Завершена", silka=0)
    def grupfile(self):
        folder = PUT + "Персонал\\Data\\"
        folders = [folder]
        # Получение списка всех файлов в папках и подпапках
        grup_pers = pd.DataFrame()
        all_files = []
        for folder in folders:
            for root, dirs, files in os.walk(folder):  # folder2,folder1,folder3
                for file in files:
                    file_path = os.path.join(root, file)
                    all_files.append(file_path)
            for file_path in all_files:
                print(file_path)
                # расширение
                file_put = os.path.splitext(file_path)[-1].lower()
                x = pd.read_csv(file_path,sep=";",encoding="utf-8")

                grup_pers = pd.concat([grup_pers,x],axis=0)

            grup_pers = grup_pers.melt(
                id_vars=["дата", "МАГАЗИН", "Ответственный за персонал"],
                var_name="статья",
                value_name="значение")
            grup_pers.to_csv(PUT + "Персонал\\Data\\" +
                             "бработанный персонад"+ ".csv",
                             encoding="utf-8",
                             sep=';', index=False,
                             decimal=",")

            print(grup_pers) # # гн
            # не использеется








#PERSONAL().grupfile()



#PERSONAL().history()
PERSONAL().tudey()
time.sleep(200)