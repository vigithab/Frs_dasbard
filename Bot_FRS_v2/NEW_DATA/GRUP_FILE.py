import sys
sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON\venv\Lib\site-packages")
sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON")

from datetime import date, timedelta
import os
import pandas as pd
import gc
import numpy as np
from Bot_FRS_v2.INI import ini
from Bot_FRS_v2.INI import memory
from Bot_FRS_v2.BOT_TELEGRAM import BOT
from Bot_FRS_v2.INI import log

pd.set_option("expand_frame_repr", False)
pd.set_option('display.max_colwidth', None)
PUT = ini.PUT
class FLOAT:
    def float_colms(self, name_data, name_col):
        for i in name_col:
            name_data[i] = (name_data[i].astype(str)
                                              .str.replace("\xa0", "")
                                              .str.replace(",", ".")
                                              .fillna("0")
                                              .astype("float"))
        return name_data
    """Для нескольких столбцов"""
    def float_colm(self, name_data, name_col):

        name_data[name_col] = (name_data[name_col].astype(str)
                                          .str.replace("\xa0", "")
                                          .str.replace(",", ".")
                                          .fillna("0")
                                          .astype("float"))
        return name_data
    """для одного столбца"""
        # перевод в число
class Spr:
    def Shahlik(self):
        spisok_shash = ['Купаты Барбекю, охл, 0,5 кг', 'Купаты куриные, охл, 0,5 кг', 'Колбаски для гриля Улитка, охл, 0,5 кг',
                        'Колбаски для гриля Ассорти, охл, 0,5 кг', 'Сердце цыпленка-бройлера (шашлык из сердечек), охл, 0,4 кг',
                        'Шашлык из индейки в маринаде, охл, 0,35 кг', 'Колбаски Свиные с вяленными томатами, вар, в/у, охл, 0,3 кг',
                        'Колбаски Свиные с сыром, вар, в/у, охл, 0,3 кг', 'Колбаски для гриля (с соусом Терияки), вар, в/у, охл, 0,3 кг',
                        'Колбаски для гриля (луковые), вар, в/у, охл, 0,3 кг', 'Колбаски Мексиканские, охл, в/у, 0,4 кг', 'Колбаски Нежные, охл, в/у, 0,4 кг']
        spr = pd.read_csv(
            r'C:\Users\lebedevvv\Desktop\Дашборд_бот\Справочники\номенклатура\Справочник номеклатуры.txt',
            sep='\t', skiprows=1)
        spr.columns = ['Владелец', 'Входит в группу', 'Срок годности', 'Классификатор для infovizion', 'Штрихкод']
        spr = spr.dropna(subset='Входит в группу')
        spr['Shsh'] = np.where(spr['Владелец'].str.contains('Р/К', regex=True), "N",
                               np.where(spr['Входит в группу'].str.contains('191.15 Сэндвичи', regex=True), "N",
                                        np.where(spr['Владелец'].str.contains('Шашл', regex=True), "Y",
                                                 np.where(spr['Входит в группу'].str.contains('100', regex=True), "Y",
                                                          np.where(spr['Входит в группу'].str.contains('Шашл', regex=True), "Y",
                                                                   np.where(spr['Входит в группу'].str.contains(
                                                                       '200.07 Гриль (Шашлык на шпажке)', regex=True), "Y",
                                                                       np.where(spr['Владелец'].isin(spisok_shash), "Y",
                                                                                "N")))))))
        spr['Штрихкод'] = spr['Штрихкод'].astype(str)
        spr = spr.dropna(subset='Входит в группу')
        spr["Владелец"] = spr["Владелец"].astype(str).apply(lambda x: (x.replace('Не исп ', '')))
        spr["Владелец"] = spr["Владелец"].astype(str).apply(lambda x: (x.replace('не исп ', '')))
        spr['Входит в группу'] = spr['Входит в группу'].astype(str).apply(lambda x: (x.replace(' ВЫВЕДЕННЫЕ', '')))
        spr = spr[['Владелец', 'Shsh']]
        spr = spr.drop_duplicates()
        spr = spr.loc[spr['Shsh'] == "Y"]
        spr = spr.rename(columns={"Владелец": 'Номенклатура',"Shsh": 'шашлык'})
        spr.to_csv(PUT + "ФОКУС\\шашлычный сезон\\" + "Справочник_шашлычный" + ".csv", encoding="utf=8", sep='\t',
                 index=False,
                 decimal=',')
        return spr
class Grup():
    def spisania_nistory(self):
        folder2 = PUT + "♀Списания\\История\\"
        folder1 = PUT + "♀Списания\\Текущий месяц\\"
        folders = [folder1, folder2]
        # Получение списка всех файлов в папках и подпапках
        all_files = []
        for folder in folders:
            for root, dirs, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    all_files.append(file_path)
            for i in all_files:
                memory.MEMORY().mem_total(x=i)
                x = pd.read_csv(i, sep="\t", encoding="utf-8", parse_dates=["дата"], date_format='%Y-%m-%d')
                ln= ["Количество вес","Количество","Сумма"]
                FLOAT().float_colms(name_data=x, name_col=ln)
                do = x["Сумма"].sum()
                x.loc[x["Аналитика хозяйственной операции"]=="Хозяйственные товары", "отбор"]="Хозы"


                x = x.groupby(["!МАГАЗИН!", "Аналитика хозяйственной операции","дата","отбор"],
                                                    as_index=False).agg(
                    {"Количество": "sum", "Количество вес": "sum","Сумма":"sum"}).reset_index(drop=True)
                posslw = x["Сумма"].sum()
                print(str(os.path.basename(i)),"  Разница списаия:", do - posslw)
                # перименование столбцов
                y = x.rename(columns={"!МАГАЗИН!": "магазин", "Сумма": "Списания"})
                # удаление микромаркетов
                l_mag = ("Микромаркет", "Экопункт", "Вендинг", "Итого")
                for w in l_mag:
                    y = y[~y["магазин"].str.contains(w)].reset_index(drop=True)
                y.to_csv(PUT + "♀Списания\\Сгрупированные файлы по дням\\" + str(os.path.basename(i)[:-4]) + ".csv", encoding="utf=8", sep='\t', index=False, decimal=',')
                gc.collect()
    def sales_history(self):
        folder2 = PUT + "♀Продажи\\2023\\"
        folder1 = PUT + "♀Продажи\\История\\"
        folder3 = PUT + "♀Продажи\\текущий месяц\\"
        folders = [folder1,folder3, folder2]
        # Получение списка всех файлов в папках и подпапках
        all_files = []
        for folder in folders:
            for root, dirs, files in os.walk(folder): #folder2,folder1,folder3
                for file in files:
                    file_path = os.path.join(root, file)
                    all_files.append(file_path)
            for file_path in all_files:
                file_extension = os.path.splitext(file_path)[-1].lower()
                if file_extension == '.txt':
                    # Обработка TXT файла
                    x = pd.read_csv(file_path, sep="\t", encoding="utf-8", parse_dates=["По дням"], date_format='%Y-%m-%d')
                    ln = ["Себестоимость","Выручка","ВесПродаж", "Прибыль","ВесНом","Количество продаж"]
                    FLOAT().float_colms(name_data=x, name_col=ln)
                    # удаление микромаркетов
                    l_mag = ("Микромаркет", "Экопункт", "Вендинг", "Итого")
                    for w in l_mag:
                        x = x[~x["Склад магазин.Наименование"].str.contains(w)].reset_index(drop=True)
                        # удаление подарочных карт
                    PODAROK = ["Подарочная карта КМ 500р+ конверт", "Подарочная карта КМ 1000р+ конверт",
                               "подарочная карта КМ 500 НОВАЯ",
                               "подарочная карта КМ 1000 НОВАЯ"]
                    for i in PODAROK:
                        x = x.loc[x["Номенклатура"] != i]

                    x = x.rename(columns={"Склад магазин.Наименование": "магазин", "Выручка": "выручка",
                                          "Себестоимость": "себестоимость","ВесПродаж":"вес_продаж","Прибыль":"прибыль",
                                          "Количество продаж":"количество_продаж","По дням":"дата"})
                    do = x["выручка"].sum()
                    x = x.groupby(["магазин", "дата"],
                                  as_index=False).agg({"выручка": "sum","себестоимость": "sum", "вес_продаж": "sum", "прибыль": "sum", "количество_продаж": "sum"}).reset_index(drop=True)
                    posslw = x["выручка"].sum()
                    print(str(os.path.basename(file_path)),"  Разница продажи:", do - posslw)
                    x["скидка"]=0
                    x["ID"]=0
                    x = x[["дата","ID","магазин","выручка","прибыль","себестоимость","вес_продаж","количество_продаж","скидка"]]
                    x.to_csv(PUT + "♀Продажи\\Сгрупированные файлы по дням\\" + str(os.path.basename(file_path)[:-4]) + ".csv", encoding="utf=8", sep='\t', index=False,
                             decimal=',')
                    gc.collect()

                elif file_extension in ['.xls', '.xlsx']:
                    # Обработка Excel файла
                    x = pd.read_excel(file_path, parse_dates=["Дата/Время чека"], date_format='%Y-%m-%d %H:%M:%S')
                    ln = ["Стоимость позиции", "Количество", "Сумма скидки"]
                    FLOAT().float_colms(name_data=x, name_col=ln)
                    do = x["Стоимость позиции"].sum()

                    x = x.groupby(["!МАГАЗИН!", "ID", "Дата/Время чека"],
                                  as_index=False).agg(
                        {"Стоимость позиции": "sum", "Количество": "sum", "Сумма скидки": "sum"}).reset_index(drop=True)
                    posslw = x["Стоимость позиции"].sum()

                    print(str(os.path.basename(file_path)),"  Разница продажи:", do - posslw)
                    x = x.rename(columns={"!МАГАЗИН!": "магазин", "Стоимость позиции": "выручка", "Количество": "количество_продаж",
                                          "Сумма скидки": "скидка", "Дата/Время чека":"дата"})
                    x = x[["дата", "ID", "магазин", "выручка", "количество_продаж", "скидка"]]
                    x.to_csv(PUT + "♀Продажи\\Сгрупированные файлы по дням\\" + str(os.path.basename(file_path)[:-5]) + ".csv", encoding="utf=8", sep='\t',
                             index=False,
                             decimal=',')
    def sebes_history(self):
        folder2 = PUT + "♀Сибестоемость\\Архив\\"
        folder1 = PUT + "♀Сибестоемость\\Текущий месяц\\"
        folders = [folder2, folder1]
        # Получение списка всех файлов в папках и подпапках
        all_files = []
        for folder in folders:
            for root, dirs, files in os.walk(folder):  # folder2,folder1,folder3
                for file in files:
                    file_path = os.path.join(root, file)
                    all_files.append(file_path)
            for file_path in all_files:
                x = pd.read_csv(file_path, sep="\t", encoding="utf-8", parse_dates=["Дата/Время чека"], date_format='%Y-%m-%d')
                ln = ["Сибистоемость", "Вес_продаж", "прибыль"]
                FLOAT().float_colms(name_data=x, name_col=ln)
                # удаление микромаркетов
                l_mag = ("Микромаркет", "Экопункт", "Вендинг", "Итого")
                for w in l_mag:
                    x = x[~x["!МАГАЗИН!"].str.contains(w)].reset_index(drop=True)
                    # удаление подарочных карт
                PODAROK = ["Подарочная карта КМ 500р+ конверт", "Подарочная карта КМ 1000р+ конверт",
                           "подарочная карта КМ 500 НОВАЯ",
                           "подарочная карта КМ 1000 НОВАЯ"]
                for i in PODAROK:
                    x = x.loc[x["номенклатура_1с"] != i]
                do = x["Сибистоемость"].sum()
                x = x.groupby(["!МАГАЗИН!", "Дата/Время чека"],
                              as_index=False).agg(
                    {"Сибистоемость": "sum", "Вес_продаж": "sum", "прибыль": "sum"}).reset_index(drop=True)
                posslw = x["Сибистоемость"].sum()
                print(str(os.path.basename(file_path)),"  Разница Сибестоемость:", do - posslw)
                x = x.rename(columns={"!МАГАЗИН!": "магазин",
                                      "Сибистоемость": "себестоимость", "Вес_продаж": "вес_продаж",
                                      "Дата/Время чека": "дата"})
                x.to_csv(PUT + "♀Сибестоемость\\Сгрупированные файлы по дням\\" + str(os.path.basename(file_path)[:-4]) + ".csv", encoding="utf=8", sep='\t',
                         index=False,
                         decimal=',')
                gc.collect()
    # обработка всех данных
    def spisania_new(self):
        folder1 = PUT + "♀Списания\\Текущий месяц\\"
        # Получение списка всех файлов в папках и подпапках
        all_files = []
        for root, dirs, files in os.walk(folder1):
            for file in files:
                file_path = os.path.join(root, file)
                all_files.append(file_path)
        for i in all_files:
            memory.MEMORY().mem_total(x=i)
            x = pd.read_csv(i, sep="\t", encoding="utf-8", parse_dates=["дата"], date_format='%Y-%m-%d')

            ln = ["Количество вес", "Количество", "Сумма"]
            FLOAT().float_colms(name_data=x, name_col=ln)
            do = x["Сумма"].sum()
            x.loc[x["Аналитика хозяйственной операции"] == "Хозяйственные товары", "отбор"] = "Хозы"

            x = x.groupby(["!МАГАЗИН!", "Аналитика хозяйственной операции", "дата", "отбор"],
                          as_index=False).agg(
                {"Количество": "sum", "Количество вес": "sum", "Сумма": "sum"}).reset_index(drop=True)
            posslw = x["Сумма"].sum()
            print(str(os.path.basename(i)),"  Разница списанияи:", do - posslw)
            # перименование столбцов
            y = x.rename(columns={"!МАГАЗИН!": "магазин", "Сумма": "Списания"})
            # удаление микромаркетов
            l_mag = ("Микромаркет", "Экопункт", "Вендинг", "Итого")
            for w in l_mag:
                y = y[~y["магазин"].str.contains(w)].reset_index(drop=True)
            y.to_csv(PUT + "♀Списания\\Сгрупированные файлы по дням\\" + str(os.path.basename(i)[:-4]) + ".csv", encoding="utf=8", sep='\t', index=False,
                     decimal=',')
            gc.collect()
        return
    def sales_new(self):
        folder2 = PUT + "♀Продажи\\2023\\"
        folder1 = PUT + "♀Продажи\\История\\"
        folder3 = PUT + "♀Продажи\\текущий месяц\\"
        folders = [folder3]
        # Получение списка всех файлов в папках и подпапках
        all_files = []
        for folder in folders:
            for root, dirs, files in os.walk(folder): #folder2,folder1,folder3
                for file in files:
                    file_path = os.path.join(root, file)
                    all_files.append(file_path)
            for file_path in all_files:
                file_extension = os.path.splitext(file_path)[-1].lower()
                if file_extension in ['.xls', '.xlsx']:
                    # Обработка Excel файла
                    x = pd.read_excel(file_path, parse_dates=["Дата/Время чека"], date_format='%Y-%m-%d %H:%M:%S')

                    ln = ["Стоимость позиции", "Количество", "Сумма скидки"]
                    FLOAT().float_colms(name_data=x, name_col=ln)
                    do = x["Стоимость позиции"].sum()
                    x = x.groupby(["!МАГАЗИН!", "ID", "Дата/Время чека"],
                                  as_index=False).agg(
                        {"Стоимость позиции": "sum", "Количество": "sum", "Сумма скидки": "sum"})\
                        .reset_index(drop=True)
                    posslw = x["Стоимость позиции"].sum()

                    print(str(os.path.basename(file_path)),"  Разница Продажи:", do - posslw)
                    x = x.rename(columns={"!МАГАЗИН!": "магазин", "Стоимость позиции": "выручка",
                                          "Количество": "количество_продаж",
                                          "Сумма скидки": "скидка", "Дата/Время чека":"дата"})
                    x = x[["дата", "ID", "магазин", "выручка", "количество_продаж", "скидка"]]
                    x.to_csv(PUT + "♀Продажи\\Сгрупированные файлы по дням\\" +
                             str(os.path.basename(file_path)[:-5]) + ".csv", encoding="utf=8", sep='\t',
                             index=False,
                             decimal=',')
    def sebes_new(self):
        folder2 = PUT + "♀Сибестоемость\\Архив\\"
        folder1 = PUT + "♀Сибестоемость\\Текущий месяц\\"
        folders = [folder1]
        # Получение списка всех файлов в папках и подпапках
        all_files = []
        for folder in folders:
            for root, dirs, files in os.walk(folder):  # folder2,folder1,folder3
                for file in files:
                    file_path = os.path.join(root, file)
                    all_files.append(file_path)
            for file_path in all_files:
                x = pd.read_csv(file_path, sep="\t", encoding="utf-8", parse_dates=["Дата/Время чека"], date_format='%Y-%m-%d')
                ln = ["Сибистоемость", "Вес_продаж", "прибыль"]
                FLOAT().float_colms(name_data=x, name_col=ln)
                # удаление микромаркетов
                l_mag = ("Микромаркет", "Экопункт", "Вендинг", "Итого")
                for w in l_mag:
                    x = x[~x["!МАГАЗИН!"].str.contains(w)].reset_index(drop=True)
                    # удаление подарочных карт
                PODAROK = ["Подарочная карта КМ 500р+ конверт", "Подарочная карта КМ 1000р+ конверт",
                           "подарочная карта КМ 500 НОВАЯ",
                           "подарочная карта КМ 1000 НОВАЯ"]
                for i in PODAROK:
                    x = x.loc[x["номенклатура_1с"] != i]
                do = x["Сибистоемость"].sum()

                x = x.groupby(["!МАГАЗИН!", "Дата/Время чека"],
                              as_index=False).agg(
                    {"Сибистоемость": "sum", "Вес_продаж": "sum", "прибыль": "sum"}).reset_index(drop=True)
                posslw = x["Сибистоемость"].sum()
                print(str(os.path.basename(file_path)),"  разница Себестоемость:", do - posslw)
                x = x.rename(columns={"!МАГАЗИН!": "магазин",
                                      "Сибистоемость": "себестоимость", "Вес_продаж": "вес_продаж",
                                      "Дата/Время чека": "дата"})
                x.to_csv(PUT + "♀Сибестоемость\\Сгрупированные файлы по дням\\" + str(os.path.basename(file_path)[:-4]) + ".csv", encoding="utf=8", sep='\t', index=False,
                         decimal=',')
                gc.collect()
    # обрабока данных за последний месяц
    def grups(self):
        print("групировка файлов")
        #Grup().spisania_nistory()
        #Grup().sebes_history()
        #Grup().sales_history()
        # Обновление тлько последнего месяца и справочника
        def sales():
            BOT.BOT().bot_mes_html(mes="Групировка файлов....", silka=0)
            # Файлы Продаж
            folder1 = PUT + "♀Продажи\\Сгрупированные файлы по дням\\"
            # Получение списка всех файлов в папках и подпапках
            all_files = []
            sales = pd.DataFrame()
            for root, dirs, files in os.walk(folder1):
                for file in files:
                    file_path = os.path.join(root, file)
                    all_files.append(file_path)
            for i in all_files:
                print(i)
                try:
                    x = pd.read_csv(i, sep=";", encoding="utf-8", parse_dates=["дата"], date_format='%Y-%m-%d')
                    sales = pd.concat([sales, x], ignore_index=True)
                except:
                    x = pd.read_csv(i, sep="\t", encoding="utf-8", parse_dates=["дата"], date_format='%Y-%m-%d')
                    sales = pd.concat([sales, x], ignore_index=True)

            # Файлы СИЕСТОЙМОСТИ
            folder1 = PUT + "♀Сибестоемость\\Сгрупированные файлы по дням\\"
            # Получение списка всех файлов в папках и подпапках
            all_files = []
            sebes = pd.DataFrame()
            for root, dirs, files in os.walk(folder1):
                for file in files:
                    file_path = os.path.join(root, file)
                    all_files.append(file_path)
            for i in all_files:
                x = pd.read_csv(i, sep="\t", encoding="utf-8", parse_dates=["дата"], date_format='%Y-%m-%d')
                sebes = pd.concat([sebes, x], ignore_index=True)
            sales = pd.concat([sales, sebes], ignore_index=True)

            ln  = ["выручка","прибыль","себестоимость","вес_продаж","количество_продаж","скидка"]
            FLOAT().float_colms(name_data=sales,name_col=ln)
            do = sales["выручка"].sum()
            sales = sales.groupby(["магазин", "дата"],
                          as_index=False).agg(
                {"выручка": "sum", "прибыль": "sum", "себестоимость": "sum","вес_продаж": "sum","количество_продаж": "sum","скидка": "sum"}).reset_index(drop=True)
            posslw =sales["выручка"].sum()

            # запись в лог
            txt = f'до - {do:.1f}, после - {posslw:.1f},' \
                  f' разница {(do - posslw):.1f}'
            log.LOG().log_obrabotka(mes=txt, priznak="Сводная выручка", name_file="0")

            # Файлы Списания
            folder1 = PUT + "♀Списания\\Сгрупированные файлы по дням\\"
            # Получение списка всех файлов в папках и подпапках
            all_files = []
            spis = pd.DataFrame()
            for root, dirs, files in os.walk(folder1):
                for file in files:
                    file_path = os.path.join(root, file)
                    all_files.append(file_path)
            for i in all_files:
                x = pd.read_csv(i, sep="\t", encoding="utf-8", parse_dates=["дата"], date_format='%Y-%m-%d')
                spis = pd.concat([spis, x], ignore_index=True)

            ln = ["Количество", "Количество вес", "Списания"]
            FLOAT().float_colms(name_data=spis, name_col=ln)

            spis_pocaz = spis.loc[spis["отбор"]=="показатель"]
            do = spis_pocaz["Списания"].sum()
            spis_pocaz  = spis_pocaz.groupby(["магазин", "дата"],as_index=False).agg(
                {"Количество": "sum", "Количество вес": "sum","Списания": "sum"}).reset_index(
                drop=True)
            posslw  = spis_pocaz["Списания"].sum()
            # запись в лог
            txt = f'до - {do:.1f}, после - {posslw:.1f},' \
                  f' разница {(do - posslw):.1f}'
            log.LOG().log_obrabotka(mes=txt, priznak="Сводная Списания", name_file="0")

            spis_pocaz = spis_pocaz.rename(columns={"Списания": "списания_оказатель"})

            spis_hoz = spis.loc[spis["отбор"] == "Хозы"]
            do = spis_hoz["Списания"].sum()
            spis_hoz = spis_hoz.groupby(["магазин", "дата"],as_index=False).agg(
                {"Количество": "sum", "Количество вес": "sum", "Списания": "sum"}).reset_index(
                drop=True)
            posslw = spis_hoz["Списания"].sum()
            # запись в лог
            txt = f'до - {do:.1f}, после - {posslw:.1f},' \
                  f' разница {(do - posslw):.1f}'
            log.LOG().log_obrabotka(mes=txt, priznak="Сводная Хозы", name_file="0")
            spis_hoz = spis_hoz.rename(columns={"Списания": "списания_хозы"})

            sales = pd.merge(sales,spis_pocaz[["магазин","дата","списания_оказатель"]],on=["магазин","дата"], how="left")
            sales = pd.merge(sales, spis_hoz[["магазин", "дата", "списания_хозы"]], on=["магазин", "дата"],how="left")

            folder2 = PUT + "♀Чеки\\История\\"
            folder1 = PUT + "♀Чеки\\2023\\"
            folders = [folder1, folder2]
            # Получение списка всех файлов в папках и подпапках
            all_files = []
            chek = pd.DataFrame()
            for root, dirs, files in os.walk(folder1):  # folder2,folder1,folder3
                for file in files:
                    file_path = os.path.join(root, file)
                    all_files.append(file_path)
            for file_path in all_files:
                print(file_path)
                try:
                    x = pd.read_excel(file_path, parse_dates=["дата"], date_format='%Y-%m-%d %H:%M:%S')
                except:
                    try:
                        x = pd.read_csv(file_path,sep=";",encoding="utf-8", parse_dates=["дата"],
                                        date_format='%Y-%m-%d %H:%M:%S')
                    except:
                        x = pd.read_csv(file_path, sep="\t", encoding="utf-8", parse_dates=["дата"],
                                        date_format='%Y-%m-%d %H:%M:%S')
                print(file_path)
                x = x.rename(columns={"!МАГАЗИН!": "магазин"})
                chek = pd.concat([chek, x], ignore_index=True)
            # Получение списка всех файлов в папках и подпапках
            all_files = []
            for root, dirs, files in os.walk(folder2):  # folder2,folder1,folder3
                for file in files:
                    file_path = os.path.join(root, file)
                    all_files.append(file_path)
            for file_path in all_files:
                try:
                    x = pd.read_excel(file_path, parse_dates=["Дата"], date_format='%d.%m.%Y')
                except:
                    x = pd.read_csv(file_path, sep=";", encoding="utf-8", parse_dates=["дата"],
                                    date_format='%Y-%m-%d %H:%M:%S')
                print(file_path)
                x  = x.rename(columns={"Магазин": "магазин","Дата": "дата","Чеков":"Количество чеков",
                                        "SKU в чеке": "количество уникальных товаров в чеке", "Длина":"количество товаров в чеке"})
                chek = pd.concat([chek, x], ignore_index=True)
            chek['дата'] = pd.to_datetime(chek['дата'])
            sales = pd.merge(sales, chek[["магазин", "дата", "Количество чеков","количество уникальных товаров в чеке","Средний чек","количество товаров в чеке"]], on=["магазин", "дата"], how="left")


            # Сортировка данных по столбцу 'Дата'
            sales = sales.sort_values('дата')

            # Список столбцов, для которых нужно рассчитать накопительные итоги
            columns_to_cumulate = ['выручка', 'прибыль', 'себестоимость', 'вес_продаж', 'количество_продаж', 'скидка',
                                   'списания_оказатель', 'списания_хозы',"Количество чеков"]
            sales_itog = pd.DataFrame()
            sales['год'] = sales['дата'].dt.year
            sales['месяц'] = sales['дата'].dt.month
            year = sales['год'].unique().tolist()
            for i in year:
                x = sales.loc[sales["год"] == i]
                x = x.sort_values('дата')
                # Создание столбцов для накопительных итогов
                for column in columns_to_cumulate:
                    # Накопительный итог по месяцам
                    x[f'накопительный_итог_{column}_месяц'] = x.groupby(['магазин','месяц'])[f'{column}'].cumsum()
                    x[f'накопительный_итог_{column}_год'] = x.groupby(['магазин', 'год'])[f'{column}'].cumsum()
                sales_itog = pd.concat([sales_itog, x], ignore_index=True)

            # Создаем DataFrame с данными о продажах за предыдущий год
            previous_year_sales_df = sales_itog.copy()  # Копируем исходный DataFrame
            previous_year_sales_df['дата'] = previous_year_sales_df['дата'] - pd.DateOffset(years=-1)
            # Объединяем исходный DataFrame и DataFrame с продажами прошлого года по столбцам 'Магазин' и 'Дата'
            sales_itog = pd.merge(sales_itog, previous_year_sales_df[["выручка", 'магазин', 'дата']], on=['магазин', 'дата'], how='left')

            sales_itog.loc[(sales_itog["выручка_x"] > 0) & (sales_itog["выручка_y"] > 0), "LFL"] = "LFL"

            sales_itog= sales_itog.drop(columns="выручка_y")
            sales_itog = sales_itog.rename(columns={"выручка_x": "выручка"})
            # добавление панов прдаж
            x = pd.read_excel(PUT + "♀Планы\\Планы ДЛЯ ДАШБОРДА.xlsx")
            print(x)
            x['дата'] = pd.to_datetime(x['дата'], format='%d.%m.%Y')
            x = x[["магазин", "ПЛАН", "дата", "Показатель"]]
            FLOAT().float_colm(name_data=x, name_col="ПЛАН")
            x["месяц"] = pd.to_datetime(x["дата"]).dt.month
            x["год"] = pd.to_datetime(x["дата"]).dt.year
            x.loc[x["Показатель"] == "Выручка", "план_выручка"] = x["ПЛАН"]
            x.loc[x["Показатель"] == "Средний чек", "план_cредний_чек"] = x["ПЛАН"]
            x.loc[x["Показатель"] == "Кол чеков", "план_кол_чеков"] = x["ПЛАН"]
            x = x.drop(["ПЛАН", "Показатель", "дата"], axis=1)
            x = x.groupby(["магазин", "месяц", "год"]).sum().reset_index()
            sales_itog =  pd.merge(sales_itog, x, on=['магазин', 'месяц',"год"], how='left')

            # создание столбцов с датами(для прогноза)
            # Создание исходного датафрейма с столбцом дат
            # Преобразование столбца 'date' в тип данных даты
            #sales_itog["дата"] = pd.to_datetime(df['date'])

            # Создание столбца с количеством прошедших дней от начала месяца
            sales_itog['Прошло дней'] = sales_itog["дата"].dt.day
            # Создание столбца с количеством оставшихся дней до конца месяца
            sales_itog['осталось дней'] = sales_itog["дата"].dt.daysinmonth - sales_itog["дата"].dt.day
            # Создание столбца с общим количеством дней в месяце
            sales_itog['дней в месяце'] = sales_itog["дата"].dt.daysinmonth

            sales_itog["дневной_план_выручка"] = sales_itog["план_выручка"] / sales_itog["дней в месяце"]
            sales_itog["дневной_план_кол_чеков"] = sales_itog["план_кол_чеков"] / sales_itog["дней в месяце"]

            """sales_itog["дневной_план_выручка"] = (sales_itog["план_выручка"] -sales_itog["накопительный_итог_выручка_месяц"])/sales_itog["осталось дней"]
            sales_itog["дневной_план_кол_чеков"] = ( sales_itog["план_кол_чеков"] - sales_itog["накопительный_итог_Количество чеков_месяц"])/sales_itog["осталось дней"]"""
            sales_itog.loc[sales_itog["год"] != 2023, "LFL"] = np.nan

            sales_itog = sales_itog[["магазин","LFL","дата","год","месяц","Прошло дней","осталось дней","дней в месяце",
            "выручка",
            "накопительный_итог_выручка_месяц",
            "накопительный_итог_выручка_год",
            "план_выручка",
            "дневной_план_выручка",

            "Количество чеков",
            "накопительный_итог_Количество чеков_месяц",
            "накопительный_итог_Количество чеков_год",
            "план_кол_чеков",
            "дневной_план_кол_чеков",

            "Средний чек",
            "план_cредний_чек",

            "прибыль",
            "накопительный_итог_прибыль_месяц",
            "накопительный_итог_прибыль_год",

            "себестоимость",
            "накопительный_итог_себестоимость_месяц",
            "накопительный_итог_себестоимость_год",

            "вес_продаж",
            "накопительный_итог_вес_продаж_месяц",
            "накопительный_итог_вес_продаж_год",

            "количество_продаж",
            "накопительный_итог_количество_продаж_месяц",
            "накопительный_итог_количество_продаж_год",

            "скидка",
            "накопительный_итог_скидка_месяц",
            "накопительный_итог_скидка_год",

            "списания_оказатель",
            "накопительный_итог_списания_оказатель_месяц",
            "накопительный_итог_списания_оказатель_год",

            "списания_хозы",
            "накопительный_итог_списания_хозы_месяц",
            "накопительный_итог_списания_хозы_год",
                                     
            
            "количество уникальных товаров в чеке",
            "количество товаров в чеке"]]

            #sales_itog.to_excel(PUT + "♀Вычисляемые_таблицы\\Нарастающие итоги.xlsx", index=False)
            sales_itog = sales_itog.loc[sales_itog["дата"]!= ini.dat_seychas]
            sales_itog.to_csv(PUT + "♀Вычисляемые_таблицы\\Нарастающие итоги.csv", sep="\t", encoding="utf-8", decimal=".", index=False)
        if ini.time_seychas < ini.time_bot_vrem:
            sales()

#todey_ear()
#lastear()
#d2022()
#Scepka()
#LFL()
#spis()
#Grup().spisania_nistory()
#Grup().Sales()
#Grup().grups()

#test()
