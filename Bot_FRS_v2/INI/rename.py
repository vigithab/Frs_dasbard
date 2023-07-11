"""import sys
from Bot_FRS_v2.INI import ini
PUT = ini.PUT
sys.path.append(ini.PUT_python)"""
import sys
sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON\venv\Lib\site-packages")
sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON")
import pandas as pd
import os
from Bot_FRS_v2.INI import ini



pd.set_option("expand_frame_repr", False)
pd.set_option('display.max_colwidth', None)

PUT = ini.PUT


class RENAME:
    def Rread(self, name_data, name_col, name = None):
            try:
                print("Загрузка справочника магазинов...")
                replacements = pd.read_excel("https://docs.google.com/spreadsheets/d/1SfuC2zKUFt6PQOYhB8EEivRjy4Dz-o4WDL-IR7CT3Eg/export?exportFormat=xlsx")
                replacements.to_excel(PUT + "Справочники\\Найти_заменить\\Замена адресов.xlsx")
                rng = len(replacements)
                for i in range(rng):
                    name_data[name_col] = name_data[name_col].replace(replacements["НАЙТИ"][i], replacements["ЗАМЕНИТЬ"][i], regex=False)
            except:
                print("Не удалось загрузить справоник найти знаменить, данные с пк")
                replacements = pd.read_excel(PUT + "Справочники\\Найти_заменить\\Замена адресов.xlsx")
                rng = len(replacements)
                for i in range(rng):
                    name_data[name_col] = name_data[name_col].replace(replacements["НАЙТИ"][i], replacements["ЗАМЕНИТЬ"][i], regex=False)
            return name_data
    """функция переименование"""
    def magazin_info(self):
            print("Загрузка справочника магазинов...")
            try:
                sprav_magaz = pd.read_excel("https://docs.google.com/spreadsheets/d/1qXyD0hr1sOzoMKvMyUBpfTXDwLkh0RwLcNLuiNbWmSM/export?exportFormat=xlsx")
                sprav_magaz.to_excel(PUT + "Справочники\\Магазины\\Справочник ТТ.xlsx")
                spqr = sprav_magaz[['ID', '!МАГАЗИН!']]
                open_mag =  sprav_magaz.loc[ (sprav_magaz["Старые/Новые"] == "Новые ТТ") |
                                          (sprav_magaz["Старые/Новые"] == "Релокация")|
                                          (sprav_magaz["Старые/Новые"] == "Без новых ТТ")]
            except:
                print("Не удалось загрузить справочник магазинов, данные с пк")
                sprav_magaz = pd.read_excel(PUT + "Справочники\\Магазины\\Справочник ТТ.xlsx")
                spqr = sprav_magaz[['ID', '!МАГАЗИН!']]
                open_mag = sprav_magaz.loc[(sprav_magaz["Старые/Новые"] == "Новые ТТ") |
                                           (sprav_magaz["Старые/Новые"] == "Релокация") |
                                           (sprav_magaz["Старые/Новые"] == "Без новых ТТ")]
            return spqr, sprav_magaz, open_mag
    """функция магазины для мердж"""
    def TY(self):
        # загрузка файла справочника териториалов
        ty = pd.read_excel("https://docs.google.com/spreadsheets/d/1rwsBEeK_dLdpJOAXanwtspRF21Z3kWDvruani53JpRY/export?exportFormat=xlsx")
        ty = ty[["Название 1 С (для фин реза)", "Менеджер"]]
        RENAME().Rread(name_data = ty, name_col= "Название 1 С (для фин реза)", name="TY")
        ty = ty.rename(columns={"Название 1 С (для фин реза)": "!МАГАЗИН!"})
        return ty

    def TY_Spravochnik(self):
        try:
            print("Загрузка справочника магазинов...")
            ty = pd.read_excel("https://docs.google.com/spreadsheets/d/1qXyD0hr1sOzoMKvMyUBpfTXDwLkh0RwLcNLuiNbWmSM/export?exportFormat=xlsx")
            ty.to_excel(PUT + "Справочники\\Магазины\\Справочник ТТ.xlsx")
        except:
            print("Не удалось загрузить справочник магазинов, данные с пк")
            ty = pd.read_excel(PUT + "Справочники\\Магазины\\Справочник ТТ.xlsx")
        Ln_tip = {'Турова Анна Сергеевна': 'Турова А.С',
                  'Баранова Лариса Викторовна': 'Баранова Л.В',
                  'Геровский Иван Владимирович': 'Геровский И.В',
                  'Изотов Вадим Валентинович': 'Изотов В.В',
                  'Томск': 'Томск',
                  'Павлова Анна Александровна': 'Павлова А.А',
                  'Вакансия': 'Вакансия',
                  'Сергеев Алексей Сергеевич': 'Сергеев А.С',
                  'Карпова Екатерина Эдуардовна': 'Карпова Е.Э'}
        ty["Менеджер"] = ty["Менеджер"].map(Ln_tip)
        ty = ty.rename(columns={"!МАГАЗИН!": "магазин"})
        # только открытые
        ty_open_magaz = ty.loc[(ty["Старые/Новые"] == "Новые ТТ") |
                        (ty["Старые/Новые"] == "Релокация") |
                        (ty["Старые/Новые"] == "Без новых ТТ")]
        ty_open_magaz = ty_open_magaz[["магазин", "Менеджер"]]
        ty = ty[["магазин","Менеджер"]]
        return ty, ty_open_magaz
        # переименование магазинов справочник ТУ
    """функция переименование"""
    def nomenklatura_rename(self):
        sp = pd.read_excel(PUT +"Справочники\\Найти_заменить\\Копия Номенклатра.xlsx")
        sp = sp.loc[sp["заменить"]!="#Н/Д"]
        c1 = sp['Найти'].tolist()
        c2 = sp['заменить'].tolist()
        dictionary = dict(zip(c1, c2))
        def SEB():
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

                    x['номенклатура_1с'] = x['номенклатура_1с'].map(dictionary).fillna(x['номенклатура_1с'])
                    if folder == "C:\\Users\\Lebedevvv\\Desktop\\FRS\\DATA_copy\\♀Сибестоемость\\Архив\\":
                        print(folder)
                        x.to_csv("C:\\Users\\Lebedevvv\\Desktop\\Новая папка\\♀Сибестоемость\\Архив\\" + file[:-4] + ".csv", sep=";", encoding="utf-8", index=False)

                        file_path = os.path.join(root, file)

                    # Сохранение DataFrame в новом пути
                    #x
        def spis():
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
                    x = pd.read_csv(i, sep="\t", encoding="utf-8", parse_dates=["дата"], date_format='%Y-%m-%d')
                    x['Номенклатура'] = x['Номенклатура'].map(dictionary).fillna(x['Номенклатура'])

                    new_directory = 'C:\\Users\\Lebedevvv\\Desktop\\FRS\\Dashbord_new\\'
                    # Получение относительного пути от исходного пути
                    relative_path = os.path.relpath(i)
                    # Создание нового пути на основе новой директории и относительного пути
                    new_path = os.path.join(new_directory, relative_path)
                    # Создание директории, если она не существует
                    os.makedirs(os.path.dirname(new_path), exist_ok=True)
                    print(new_path)
                    # Сохранение DataFrame в новом пути
                    x.to_csv(new_path[:-4] + ".csv", sep=";", encoding="utf-8", index=False)
        def sales():
            folder2 = PUT + "♀Продажи\\2023\\"
            folder1 = PUT + "♀Продажи\\История\\"
            folder3 = PUT + "♀Продажи\\текущий месяц\\"
            folders = [folder2, folder1, folder3]
            #folders = [folder3]
            # Получение списка всех файлов в папках и подпапках
            all_files = []
            for folder in folders:
                for root, dirs, files in os.walk(folder):  # folder2,folder1,folder3
                    for file in files:
                        file_path = os.path.join(root, file)
                        all_files.append(file_path)
                for file_path in all_files:
                    file_extension = os.path.splitext(file_path)[-1].lower()
                    if file_extension == '.txt':
                        # Обработка TXT файла
                        x = pd.read_csv(file_path, sep="\t", encoding="utf-8", parse_dates=["По дням"], date_format='%Y-%m-%d')

                        x['Номенклатура'] = x['Номенклатура'].map(dictionary).fillna(x['Номенклатура'])

                        new_directory ='C:\\Users\\Lebedevvv\\Desktop\\FRS\\Dashbord_new\\'
                        # Получение относительного пути от исходного пути
                        relative_path = os.path.relpath(file_path)
                        # Создание нового пути на основе новой директории и относительного пути
                        new_path = os.path.join(new_directory, relative_path)
                        # Создание директории, если она не существует
                        os.makedirs(os.path.dirname(new_path), exist_ok=True)
                        print(new_path)
                        # Сохранение DataFrame в новом пути
                        x.to_csv(new_path[:-4]+".csv", sep=";", encoding="utf-8", index=False)

                        #x.to_csv(PUT + "♀Продажи\\Сгрупированные файлы по дням\\" + str(os.path.basename(file_path)[:-4]) + ".csv", encoding="utf=8", sep='\t', index=False,decimal=',')

                    elif file_extension in ['.xls', '.xlsx']:
                        # Обработка Excel файла
                        x = pd.read_excel(file_path, parse_dates=["Дата/Время чека"], date_format='%Y-%m-%d %H:%M:%S')
                        x.loc[x["номенклатура_1с"].isnull(),"номенклатура_1с"]=x["Наименование товара"]
                        x['номенклатура_1с'] = x['номенклатура_1с'].map(dictionary).fillna(x['номенклатура_1с'])
                        print(x)
                        new_directory = 'C:\\Users\\Lebedevvv\\Desktop\\FRS\\Dashbord_new\\'
                        # Получение относительного пути от исходного пути
                        relative_path = os.path.relpath(file_path)
                        # Создание нового пути на основе новой директории и относительного пути
                        new_path = os.path.join(new_directory, relative_path)
                        # Создание директории, если она не существует
                        os.makedirs(os.path.dirname(new_path), exist_ok=True)
                        print(new_path)
                        # Сохранение DataFrame в новом пути
                        print(new_directory + str(os.path.basename(file_path)[:-5]))
                        x.to_csv(new_directory + str(os.path.basename(file_path)[:-5]) + ".csv", sep=";", encoding="utf-8", index=False)
        SEB()
        sales()

        spis()

    def Rread_kassa(self, name_data, name_col, name):
        print("Загрузка справочника кассы...")
        replacements = pd.read_excel(PUT + "Справочники\\Кассы\\Найи_заменить касса.xlsx", sheet_name="Sheet1")
        rng = len(replacements)
        for i in range(rng):
            name_data[name_col] = name_data[name_col].replace(replacements["Найти"][i], replacements["заменить"][i],
                                                              regex=False)
            # print(replacements["Найти"][i], " / ", replacements["заменить"][i])
        return name_data

#RENAME().nomenklatura_rename()
