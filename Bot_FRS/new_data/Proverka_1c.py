import pandas as pd
from Bot_FRS.inf import NASTROYKA as setting
from Bot_FRS.inf import memory as memory
import os
import shutil
import zipfile

pd.set_option("expand_frame_repr", False)
pd.set_option('display.max_colwidth', None)

PUT = setting.PUT

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
                print("Произошла ошибка при загрузке справочника магазинов. Повторяе попытку...")
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

class data():
    def setreteyl(self):

        folder1 = PUT + "Selenium\\исходники\\"
        folders = [ folder1]
        # Получение списка всех файлов в папках и подпапках
        all_files = []
        for folder in folders:
            for root, dirs, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    all_files.append(file_path)
            for i in all_files:
                memory.MEMORY().mem_total(x=i)
                x = pd.read_excel(i, parse_dates=["Дата/Время чека"], date_format="%Y-%m-%d %H:%M:%S")




                spqr = RENAME().magazin_info()
                x = x.rename(columns={"Магазин": 'ID'})
                x = x.merge(spqr[['!МАГАЗИН!', 'ID']], on='ID', how="left")

                x = x.loc[x["Тип"].notnull()]
                x['!МАГАЗИН!'] = x['!МАГАЗИН!'].astype("str")

                x = x[["Тип","Дата/Время чека","ID","Касса", "Смена","Чек","Сумма чека","Сумма скидки чека","!МАГАЗИН!"]]
                # Формирование ID Чека

                x["ID_Chek"] = x["!МАГАЗИН!"].astype(str) + x["Касса"].astype(int).astype(str) + x["Чек"].astype(int).astype(
                    str) + x["Дата/Время чека"].astype(str) + x["Смена"].astype(int).astype(str)

                x = x.drop(columns={"!МАГАЗИН!", "ID","Касса","Смена","Чек" })



                print(x)



                return
        return

    def one_c(self):

        zip  =r"\\rtlfranch3\Данные из 1С\Для Дашборда\Проверка Сетретейл-1С(потерянные чеки)"
        not_zip = PUT + "Selenium\\Сетевой диск\\Распоковкадля проверки_чеков\\"

        """#put_zip = r'\\rtlfranch3\Данные из 1С\Для Дашборда\Себестоимость'
        put_zip_end = PUT + "\\Selenium\\Сетевой диск\\"
        put_zip_extract = PUT + "Selenium\\Сетевой диск\\Распаковка_штрихкод_сибестоемость_проверка\\"
        put_sebes = PUT + "NEW\\Сибестоемость\\"
        put_proverca = PUT + "NEW\\ОБРАБОТКА ОШИБОК\\Продажи 1с по магазинам для проверки\\"
        put_spravka = PUT + "Справочники\\"""

        # Получение списка файлов в заданной директории
        files = os.listdir(zip)
        # Фильтрация списка файлов для получения только ZIP-архивов
        zip_files = [file for file in files if file.endswith('.zip')]
        # Создание списка пар (время изменения, имя файла)
        file_times = [(os.path.getmtime(os.path.join( zip, file)), file) for file in zip_files]
        # Сортировка списка пар по времени изменения (последний измененный файл будет первым)
        file_times.sort(reverse=True)
        # Получение пути к последнему измененному ZIP-архиву
        last_modified_zip = os.path.join( zip, file_times[0][1])
        # Имя файла
        name_fail = os.path.basename(last_modified_zip)
        # Копирование ZIP-файла в указанный путь
        shutil.copy(last_modified_zip, not_zip)
        # Распаковка файла
        zip_files = os.path.join(not_zip, name_fail)
        print(zip_files)



        # Разархивирование файла
        with zipfile.ZipFile(zip_files, 'r') as zip_ref:
            zip_ref.extractall(not_zip)
        # Удаление архива
        os.remove(zip_files)
        file = os.path.join(not_zip, name_fail)
        print(file)
        return
    def union(self):
        return
data().one_c()
#data().setreteyl()





