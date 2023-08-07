import os
import time
import warnings
import pandas as pd
from Bot_FRS_v2.INI import rename, ini
import datetime
from Bot_FRS_v2.BOT_TELEGRAM import BOT
warnings.simplefilter("ignore", category=UserWarning, lineno=226, append=True)


class STORNO():
    def __init__(self):
        spqr, sprav_magaz, open_mag = rename.RENAME().magazin_info()
        sprav_magaz = sprav_magaz.loc[sprav_magaz["Работают или нет"]=="Действующие"]
        self.spisok = sprav_magaz["ID"].tolist()
        while "нет" in self.spisok:
            self.spisok.remove("нет")
        # Получаем текущую дату и время в UTC
        end_date = datetime.datetime.utcnow()

        # Получаем дату и время 5 дней назад в UTC
        start_date = end_date - datetime.timedelta(days=35)

        self.date_dict = {}
        current_date = start_date
        while current_date <= end_date:
            formatted_date = current_date.strftime("%d.%m.%Y")
            unix_timestamp = int(current_date.timestamp() * 1000)

            # Корректируем временную разницу, добавляя 1 день к текущей дате в UTC
            next_day = current_date + datetime.timedelta(days=1)
            next_day_unix_timestamp = int(next_day.timestamp() * 1000)

            self.date_dict[formatted_date] = (unix_timestamp, next_day_unix_timestamp)
            current_date += datetime.timedelta(days=1)



    def storno(self, disk = None):

        if disk is not None:
            # Преобразуем дату из строки в объект datetime
            date_object = datetime.datetime.strptime(disk, "%d.%m.%Y")
            # Получаем Unix-временные метки для данной даты и следующего дня
            unix_timestamp = int(date_object.timestamp() * 1000)
            next_day = date_object + datetime.timedelta(days=1)
            next_day_unix_timestamp = int(next_day.timestamp() * 1000)
            # Создаем словарь
            self.date_dict = {
                disk: (unix_timestamp, next_day_unix_timestamp)}

        print(self.spisok)
        # Перебираем ключи словаря и выводим значения 1 и 2 для каждого ключа
        for key in self.date_dict:
            df_itog = pd.DataFrame()
            value1, value2 = self.date_dict[key]
            print(f"Дата: {key}, Unix-старт: {value1}, Unix-стоп: {value2}")

            for i in self.spisok:
                print(i)
                time.sleep(0.1)
                silka = pd.read_excel(f"http://10.32.2.51:8443/SetXRMI/ReportsProcessorServlet?Action=StornoReport&BEGIN=" \
                         f"{value1}&END={value2}&PURCHASE_ACTION_TYPE=STORNO&SHOP={i}&FILE_TYPE=XLSX",skiprows=6, engine='openpyxl')
                silka['магазин'] = i
                cols = list(silka.columns)
                cols = ['магазин'] + [col for col in cols if col != 'магазин']
                silka = silka[cols]
                silka = silka.drop(columns=["Unnamed: 2","Unnamed: 5","Unnamed: 7","Unnamed: 9","Unnamed: 11","Unnamed: 13"])
                print(silka.head(5))
                df_itog = pd.concat([df_itog,silka],axis=0)
            df_itog.to_csv(ini.PUT + "Selenium\\Сторно\\Исходники\\"+ f"{key}.csv",index=False)
            try:
                df_itog.to_csv( "P:\\Фирменная розница\\ФРС\\Данные из 1 С\\Чеки_Сторно\\Исходники\\" + f"{key}.csv", index=False)
            except:
                BOT.BOT().bot_mes_html(mes=f"📛 Сторно ошибка {key} Ошибка сохранения на паблик", silka=0)
            BOT.BOT().bot_mes_html(mes="✅"+f" Сторно {key} сохранен", silka=0)
    def strno_obrabotka_history(self):
        start = ini.PUT + "Selenium\\Сторно\\Исходники\\"
        start_original = ini.PUT + "Selenium\\Исходники\\"
        for filename in os.listdir(start):
            file_pach = os.path.join(start,filename)
            file_pach_original = os.path.join(start_original, filename[:-4]+".xlsx")
            print(file_pach_original)
            print(file_pach)
            def original():
                orig =pd.read_excel(file_pach_original)
                orig["Дата/Время чека"] = pd.to_datetime(orig["Дата/Время чека"],
                                                        format="%d.%m.%Y %H:%M:%S").dt.date
                orig =orig.loc[orig["Магазин"].notnull()]
                print(orig)
                # Преобразуем числовые столбцы в строковый тип и удаляем десятичные части (.0)
                orig["ID_Chek"] = orig["Магазин"].astype(str).replace('\.0', '', regex=True) + \
                                 orig["Касса"].astype(str).replace('\.0', '', regex=True) + \
                                 orig["Чек"].astype(str).replace('\.0', '', regex=True) + \
                                 orig["Дата/Время чека"].astype(str) + \
                                 orig["Смена"].astype(str).replace('\.0', '', regex=True)


                return orig

            def storno():
                sto = pd.read_csv(file_pach,sep="\t",encoding="utf-8")
                sto["Дата/Время чека"] = pd.to_datetime(sto["Дата/Время чека"],
                                                                   format="%d.%m.%Y %H:%M:%S").dt.date
                sto = sto.loc[sto["Магазин"]!= "NaN"]
                print(sto)
                # Преобразуем числовые столбцы в строковый тип и удаляем десятичные части (.0)
                sto["ID_Chek"] = sto["Магазин"].astype(str).replace('\.0', '', regex=True) + \
                                 sto["Касса"].astype(str).replace('\.0', '', regex=True) + \
                                 sto["Чек"].astype(str).replace('\.0', '', regex=True) + \
                                 sto["Дата/Время чека"].astype(str).replace('\.0', '', regex=True) + \
                                 sto["Смена"].astype(str).replace('\.0', '', regex=True)
                return sto
            original = original()
            print(original)

            storno = storno()
            print(storno)


if __name__ == '__main__':
    #STORNO().storno()
    STORNO().strno_obrabotka_history()