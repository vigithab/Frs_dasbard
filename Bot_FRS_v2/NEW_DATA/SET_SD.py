import sys

import numpy as np
import xlrd

sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON\venv\Lib\site-packages")
sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON")
import os
import shutil
import zipfile
import openpyxl
import pandas as pd
from Bot_FRS_v2.BOT_TELEGRAM import BOT
from Bot_FRS_v2.INI import ini,rename
from fuzzywuzzy import fuzz, process

ta = ini.time_bot_vrem
PUT = ini.PUT

class NEW_DATA_sd:
    def reserv(self):
        try:
            replacements = pd.read_excel("https://docs.google.com/spreadsheets/d/1SfuC2zKUFt6PQOYhB8EEivRjy4Dz-o4WDL-IR7CT3Eg/export?exportFormat=xlsx")
            replacements.to_excel(PUT + "Справочники\\Найти_заменить\\Замена адресов.xlsx", index=False)


            spravka = pd.read_excel("https://docs.google.com/spreadsheets/d/1qXyD0hr1sOzoMKvMyUBpfTXDwLkh0RwLcNLuiNbWmSM/export?exportFormat=xlsx")
            spravka.to_excel(PUT + "Справочники\\Магазины\\Справочник ТТ.xlsx")
            spravka = spravka.loc[spravka["Менеджер"].notnull()]
            spravka = spravka.loc[spravka["Менеджер"]!= "нет магазина"]
            spravka = spravka.loc[spravka["Менеджер"] != "Отдел торговой сети"]
            spravka = spravka.loc[spravka["Менеджер"] != "Не назначен(ТТ еще не открыто)"]

            # Получаем уникальные значения менеджеров
            unique_managers = spravka["Менеджер"].unique()
            # Сортируем уникальные значения по алфавиту
            unique_managers_sorted = sorted(unique_managers)
            # Создаем DataFrame с уникальными менеджерами и их нумерацией
            unique_managers = pd.DataFrame(
                {'Менеджер': unique_managers_sorted, 'Нумерация': range(1, len(unique_managers_sorted) + 1)})

            unique_managers["Мененджер коротко"] = unique_managers ["Менеджер"]

            Ln_tip = {'Турова Анна Сергеевна': 'Турова А.С',
                      'Баранова Лариса Викторовна': 'Баранова Л.В',
                      'Геровский Иван Владимирович': 'Геровский И.В',
                      'Изотов Вадим Валентинович': 'Изотов В.В',
                      'Томск': 'Томск',
                      'Павлова Анна Александровна': 'Павлова А.А',
                      'Вакансия': 'Вакансия',
                      'Сергеев Алексей Сергеевич': 'Сергеев А.С',
                      'Карпова Екатерина Эдуардовна': 'Карпова Е.Э'}

            unique_managers["Мененджер коротко"] = unique_managers["Мененджер коротко"].map(Ln_tip)
            print(unique_managers)
            unique_managers.to_csv(PUT + "Справочники\\Магазины\\unique_managers.csv",index=True)
            BOT.BOT().bot_mes_html(mes="✅ Справочники магазинов(резерв)", silka=0)
        except:
            BOT.BOT().bot_mes_html(mes="📛 Справочники магазинов(резерв) - Ошибка", silka=0)
            print("Справочники не обновлены")
    def setevoy(self):
            put_zip = r'\\rtlfranch3\Данные из 1С\Для Дашборда\Себестоимость'
            put_zip_end = PUT + "\\Selenium\\Сетевой диск\\"
            put_zip_extract =  PUT+ "Selenium\\Сетевой диск\\Распаковка_штрихкод_сибестоемость_проверка\\"
            put_sebes = PUT + "NEW\\Сибестоемость\\"
            put_proverca = PUT + "NEW\\ОБРАБОТКА ОШИБОК\\Продажи 1с по магазинам для проверки\\"
            put_spravka = PUT + "Справочники\\"

            # Получение списка файлов в заданной директории
            files = os.listdir(put_zip)
            # Фильтрация списка файлов для получения только ZIP-архивов
            zip_files = [file for file in files if file.endswith('.zip')]
            # Создание списка пар (время изменения, имя файла)
            file_times = [(os.path.getmtime(os.path.join(put_zip, file)), file) for file in zip_files]
            # Сортировка списка пар по времени изменения (последний измененный файл будет первым)
            file_times.sort(reverse=True)
            # Получение пути к последнему измененному ZIP-архиву
            last_modified_zip = os.path.join(put_zip, file_times[0][1])
            # Имя файла
            name_fail = os.path.basename(last_modified_zip)
            # Копирование ZIP-файла в указанный путь
            shutil.copy(last_modified_zip, put_zip_end)
            # Распаковка файла
            zip_files = os.path.join(put_zip_end ,name_fail)

            with zipfile.ZipFile(zip_files, 'r') as zip_ref:
                zip_ref.extractall(put_zip_extract)

            put_sebes_extract = os.path.join(put_zip_extract, 'Финрез лебедев (TXT).txt')
            print("Получение: Финрез лебедев (TXT).txt")
            BOT.BOT().bot_mes_html(mes="✅ Себестоемость", silka=0)
            BOT.BOT().bot_mes_html(mes="✅ Вес", silka=0)
            if os.path.isfile(put_sebes_extract):
                shutil.copy(put_sebes_extract, put_sebes)

                # удалить файл после преноса
                if os.path.isfile(put_sebes_extract):
                    os.remove(put_sebes_extract)
                else:
                    print("Файл не найден:", put_sebes_extract)
            else:
                print("Файл не найден:", os.path.basename(put_sebes_extract))
            # лог #####################################################################################################


            put_proverca_extract = os.path.join(put_zip_extract, 'Финрез лебедев ПРоверка (TXT).txt')
            print("Получение: Финрез лебедев ПРоверка (TXT).txt")
            BOT.BOT().bot_mes_html(mes="✅ Продажи",silka=0)
            if os.path.isfile(put_proverca_extract):
                shutil.copy(put_proverca_extract, put_proverca)

                # удалить файл после преноса
                if os.path.isfile(put_proverca_extract):
                    os.remove(put_proverca_extract)
                else:
                    print("Файл не найден:", put_proverca_extract)
            else:
                print("Файл не найден:", os.path.basename(put_proverca_extract))
            # лог #####################################################################################################

            put_spravka_extract = os.path.join(put_zip_extract, 'Штрихкоды (TXT).txt')
            print("Получение: Штрихкоды (TXT).txt")

            BOT.BOT().bot_mes_html(mes="✅ Штрихкода(НСИ)", silka=0)
            if os.path.isfile(put_spravka_extract):
                shutil.copy(put_spravka_extract, put_spravka)

                spravka =pd.read_csv(os.path.join(put_spravka, 'Штрихкоды (TXT).txt'), sep="\t", encoding="utf-8")
                spravka.rename(columns={'Срок годности': 'Срок годности (Справочник "Номенклатура")',
                                        "Классификатор для infovizion": "Классификатор для infovizion (Справочник \"Номенклатура\")"}, inplace=True)

                spravka.to_csv(PUT + "Справочники\\номенклатура\\Справочник номеклатуры.txt", sep="\t",
                               encoding="utf-8", index=False)

                # удалить файл после преноса
                if os.path.isfile(put_spravka_extract):
                    os.remove(put_spravka_extract)
                else:
                    print("Файл не найден:", put_spravka_extract)

            else:
                print("Файл не найден:", os.path.basename(put_spravka_extract))
            # лог #####################################################################################################

            # удалить файл после преноса
            if os.path.isfile(zip_files):
                os.remove(zip_files)
            else:
                print("Файл не найден:", zip_files)
            return
    def setevoy_spisania(self):
        # Пути к файлам и папкам
        print("Получение: Списания")
        source_file = r'\\rtlfranch3\Данные из 1С\Для Дашборда\Списания\Списания тек.м..zip'
        #source_file = r'\\rtlfranch3\Данные из 1С\Для Дашборда\Списания\Списания мес..zip'
        destination_folder = PUT + 'NEW\\Списания\\'

        if os.path.isfile(source_file):
            # Копирование файла в папку назначения
            shutil.copy2(source_file, destination_folder)
            # Получение пути к скопированному файлу
            copied_file = os.path.join(destination_folder, os.path.basename(source_file))
            # Разархивирование файла
            with zipfile.ZipFile(copied_file, 'r') as zip_ref:
                zip_ref.extractall(destination_folder)
            # Удаление архива
            os.remove(copied_file)
            BOT.BOT().bot_mes_html(mes="✅ Списание обновление последних 7 дней", silka=0)

        else:
            source_file = r"\\rtlfranch3\Данные из 1С\Для Дашборда\Списания\Списания мес..zip"
            # Копирование файла в папку назначения
            shutil.copy2(source_file, destination_folder)
            # Получение пути к скопированному файлу
            copied_file = os.path.join(destination_folder, os.path.basename(source_file))
            # Разархивирование файла
            with zipfile.ZipFile(copied_file, 'r') as zip_ref:
                zip_ref.extractall(destination_folder)
            # Удаление архива
            os.remove(copied_file)
            BOT.BOT().bot_mes_html(mes="✅ Списание обновление месяца", silka=0)

    def setevoy_degustacia(self):
        # Пути к файлам и папкам
        BOT.BOT().bot_mes_html(mes="✅ дегустации", silka=0)
        print("Получение: дегустации")
        source_file = r'\\rtlfranch3\Данные из 1С\Для Дашборда\Дегустации\Дегустации прошлая неделя.zip'
        destination_folder =  PUT +  'NEW\\Дегустации\\'

        if os.path.isfile(source_file):
            shutil.copy2(source_file, destination_folder)
            copied_file = os.path.join(destination_folder, os.path.basename(source_file))
            with zipfile.ZipFile(copied_file, 'r') as zip_ref:
                zip_ref.extractall(destination_folder)
            os.remove(copied_file)

        else:
            BOT.BOT().bot_mes_html(mes="❗Нет файла дегустации", silka=0)
    def Nmenklatura(self, rows=None):
        # Пути к файлам и папкам
        print("Получение: Справочников")
        ot = r"\\rtlfranch3\Данные из 1С\Для Дашборда\SKU и Номенклатура"
        to = r"C:\Users\lebedevvv\Desktop\FRS\Dashbord_new\Справочники\номенклатура"
        for filename in os.listdir(ot):
            filename = filename[:-4]
            pabl = os.path.join(ot, filename + ".txt")
            save = os.path.join(to, filename+ "_new.txt")
            shutil.copy2(pabl, save)
            if filename == "GROUPS":
                spravka = pd.read_csv(
                    r"C:\Users\lebedevvv\Desktop\FRS\Dashbord_new\Справочники\номенклатура\GROUPS_new.txt",
                    sep="\t", encoding="utf-8")
                komanda = pd.read_excel(
                    "https://docs.google.com/spreadsheets/d/1dNt8qpZL_ST8aF_iBqV7oVQvH1tsExMd6uLCiC_UtfQ/export?exportFormat=xlsx")
                spravka = spravka.merge(komanda, on=['Входит в группу'], how="left")
                spravka.to_csv(PUT + "Справочники\\номенклатура\\GROUPS.txt", sep="\t", encoding="utf-8")
        spravk_sku = pd.read_csv(
            r"C:\Users\lebedevvv\Desktop\FRS\Dashbord_new\Справочники\номенклатура\Список_new.txt",
            sep="\t", encoding="utf-8")
        spravk_sku.loc[spravk_sku["Номенклатура"] == "Не исп Эклер СХ смородиновый, 50г", "Номенклатура"] = "Бедрышко цыпленка-бройлера (в подложке), охл"
        spravk_sku.to_csv(PUT + "Справочники\\номенклатура\\Список.txt", sep="\t", encoding="utf-8")
        os.remove(r"C:\Users\lebedevvv\Desktop\FRS\Dashbord_new\Справочники\номенклатура\GROUPS_new.txt")
        os.remove(r"C:\Users\lebedevvv\Desktop\FRS\Dashbord_new\Справочники\номенклатура\Список_new.txt")
        BOT.BOT().bot_mes_html(mes="✅ Справоники обновлены", silka=0)
    def jalob(self):
        start = r"\\rtlfranch3\Данные из 1С\Для Дашборда\Жалобы"
        end = r"C:\Users\lebedevvv\Desktop\FRS\Dashbord_new\Жалобы\Исходники"
        # Создаем временную папку
        tmp_folder = r'C:\Users\lebedevvv\Desktop\FRS\Dashbord_new\Жалобы\tmp'
        os.makedirs(tmp_folder, exist_ok=True)
        for filename in os.listdir(start):

            PUT_File_start = os.path.join(start, filename)
            PUT_File_end = os.path.join(end, filename)
            # Копирование файла в папку назначения
            shutil.copy2(PUT_File_start, PUT_File_end)
            # Получение пути к скопированному файлу
            new_file = PUT_File_end
            # Путь к вашему исходному файлу .xlsx
            xlsx_file_path = new_file

            # Распаковываем excel как zip в нашу временную папку
            with zipfile.ZipFile(xlsx_file_path) as excel_container:
                excel_container.extractall(tmp_folder)

            # Переименовываем файл с неверным названием
            wrong_file_path = os.path.join(tmp_folder, 'xl', 'SharedStrings.xml')
            correct_file_path = os.path.join(tmp_folder, 'xl', 'sharedStrings.xml')

            os.rename(wrong_file_path, correct_file_path)
            # Запаковываем excel обратно в zip и переименовываем в исходный файл
            shutil.make_archive(xlsx_file_path, 'zip', tmp_folder)
            os.remove(xlsx_file_path)
            os.rename(f'{xlsx_file_path}.zip', xlsx_file_path)
            shutil.rmtree(tmp_folder)
        df_grup = pd.DataFrame()
        for filename in os.listdir(end):
            end_file = os.path.join(end, filename)
            df = pd.read_excel(end_file,skiprows=4)
            df = df.loc[df["Виновное подразделение.Вышестоящее подразделение"]!= "Итого"]
            df = df.drop(columns=["Виновное подразделение.Вышестоящее подразделение","Unnamed: 1","Unnamed: 2"])

            df_grup = pd.concat([df_grup, df],axis=0)
        df_grup["Участники.Партнер_Проверка"] =  df_grup["Участники.Партнер"]

        rename.RENAME().Rread(name_data=df_grup,name_col="Участники.Партнер")
        df_grup_nik = df_grup[["Участники.Партнер","Участники.Партнер_Проверка"]]
        df_grup_nik = df_grup_nik.drop_duplicates().reset_index(drop=True)
        df_grup_nik.to_excel(
            r"C:\Users\lebedevvv\Desktop\FRS\Dashbord_new\Жалобы\Уникальные магазины\уникальные магазины.xlsx", index=False)
        df_grup =  df_grup.drop(columns=["Участники.Партнер_Проверка",'Виновное подразделение','Итог',"Клиент"])
        del df_grup_nik
        #в формат даты
        df_grup['Дата регистрации'] = pd.to_datetime(df_grup['Дата регистрации'], format='%d.%m.%Y %H:%M:%S')
        # только дату
        df_grup['Дата регистрации'] = df_grup['Дата регистрации'].dt.date
        # доавление ТУ
        TY, ty_open_magaz = rename.RENAME().TY_Spravochnik()

        TY = TY.loc[TY["Менеджер"].notnull()]
        df_grup  = df_grup.rename(columns={'Участники.Партнер':"магазин"})
        df_grup = df_grup.merge(TY, on=["магазин"], how="left").reset_index(drop=True)
        df_grup  = df_grup.loc[df_grup ["Менеджер"].notnull()]
        df_grup['Дата регистрации'] = pd.to_datetime(df_grup['Дата регистрации'], format='%Y-%m-%d')

        # Выполните группировку по менеджерам, наименованию и посчитайте количество жалоб и благодарностей для каждой группы
        result = df_grup.groupby(['Дата регистрации',"магазин",'Менеджер','Наименование'])['Дата регистрации'].count().unstack(fill_value=0).reset_index()
        # Выведите результат
        new_columns_order = [
            "Менеджер",
            'Наименование',
            'Дата регистрации',
            "магазин",
            'Номенклатура.Группа.Наименование',
            'Номенклатура',
            'Причина возникновения',
            'Результаты отработки',
            'Дата окончания',
            'Статус',
            'Дата изготовления',
            'Канал связи',
            'Категория обращения',
            'Производитель',
            'Группа связи',
            'Снята с продажи вся партия',
            'Описание претензии']
        # Переупорядочите столбцы в исходном датафрейме
        df_grup = df_grup[new_columns_order]
        df_grup.to_excel(
            r"C:\Users\lebedevvv\Desktop\FRS\Dashbord_new\Жалобы\Для_дашборда(Жалобы).xlsx",
            index=False)
        result.to_excel(
            r"C:\Users\lebedevvv\Desktop\FRS\Dashbord_new\Жалобы\Для_дашборда(Жалобы)_сгрупированные.xlsx",
            index=False)
        BOT.BOT().bot_mes_html(mes="✅ Жалобы обновлены", silka=0)

def run_NEW_DATA_sd():
    if ini.time_seychas < ini.time_bot_vrem:
        # вставить йенкцию проверки доступности
        try:
            NEW_DATA_sd().reserv()
        except:
            BOT.BOT().bot_mes_html(mes="📛 ошибка копирования справочников", silka=0)
        try:
            NEW_DATA_sd().setevoy()
        except:
            BOT.BOT().bot_mes_html(mes="📛 Не получена себестоемость", silka=0)
        try:
            NEW_DATA_sd().setevoy_spisania()
        except:
            BOT.BOT().bot_mes_html(mes="📛 Не получены списания", silka=0)
        try:
            NEW_DATA_sd().setevoy_degustacia()
        except:
            BOT.BOT().bot_mes_html(mes="📛 Не получены дегустации шашлыка", silka=0)
        try:
            NEW_DATA_sd().Nmenklatura()
        except:
            BOT.BOT().bot_mes_html(mes="📛 Не оновлена номенклатура", silka=0)
        try:
            NEW_DATA_sd().jalob()
        except:
            BOT.BOT().bot_mes_html(mes="📛 Не обновлены жалобы", silka=0)
    else:
        print("Время: ", ini.time_seychas, "Ограничение: ", ini.time_bot_vrem)



if __name__ == '__main__':
    NEW_DATA_sd().jalob()
    #NEW_DATA_sd().reserv()