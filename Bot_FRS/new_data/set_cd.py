from datetime import datetime, timedelta, time, date
import datetime
import os
import shutil
import zipfile
import pandas as pd
import sys
from Bot_FRS.bot_telegram import Bot as bot
from Bot_FRS.inf import NASTROYKA as setting


ta = setting.time_bot_vrem
PUT = setting.PUT

class NEW_DATA:
    def setevoy(self):
        today = datetime.datetime.now()
        tame_Filter = today.strftime("%H:%M:%S")
        if tame_Filter <ta:
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
            bot.BOT().bot_mes_html(mes="- Себестоемость", silka=0)
            bot.BOT().bot_mes_html(mes="- Вес", silka=0)
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
            bot.BOT().bot_mes_html(mes="- Продажи",silka=0)
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

            bot.BOT().bot_mes_html(mes="- Штрихкода(НСИ)", silka=0)
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
    #
    def setevoy_spisania(self):
        today = datetime.datetime.now()
        tame_Filter = today.strftime("%H:%M:%S")
        if tame_Filter < ta:
            # Пути к файлам и папкам
            bot.BOT().bot_mes_html(mes="- Списания", silka=0)
            print("Получение: Списания")
            source_file = r'\\rtlfranch3\Данные из 1С\Для Дашборда\Списания\Списания тек.м..zip'
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

            else:
                bot.BOT().bot_mes_html(mes="- списания ОТСУТСТВУЕТ", silka=0)
    def setevoy_degustacia(self):
        today = datetime.datetime.now()
        tame_Filter = today.strftime("%H:%M:%S")
        if tame_Filter < ta:
            # Пути к файлам и папкам
            bot.BOT().bot_mes_html(mes="- дегустации", silka=0)
            print("Получение: дегустации")
            source_file = r'\\rtlfranch3\Данные из 1С\Для Дашборда\Дегустации\Дегустации прошлая неделя.zip'
            destination_folder = PUT +  'NEW\\Дегустации\\'

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

            else:
                bot.BOT().bot_mes_html(mes="❗Нет файла дегустации", silka=0)
    # получение данных  сетевого диска