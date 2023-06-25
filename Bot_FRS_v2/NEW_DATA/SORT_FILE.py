import sys
sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON\venv\Lib\site-packages")
sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON")

import os
import shutil
import datetime
from Bot_FRS_v2.INI import ini
PUT = ini.PUT

import os
import shutil
import datetime

class SORT:
    def sort_files_sales(self):
        def move_files(source_folder, destination_folder, date_pattern, d):
            day = datetime.datetime.now().strftime(date_pattern)
            mouth_god = datetime.datetime.now().strftime(date_pattern)[3:]
            god = datetime.datetime.now().strftime(date_pattern)[6:]
            if d == "day":
                for filename in os.listdir(source_folder):
                    file_date = filename[:-4]
                    if file_date == day:
                        src = os.path.join(source_folder, filename)
                        dst = os.path.join(destination_folder, filename)
                        shutil.move(src, dst)
            if d == "month":
                for filename in os.listdir(source_folder):
                    file_date = filename[:-4]

                    if file_date != day:
                        src = os.path.join(source_folder, filename)
                        dst = os.path.join(destination_folder, filename)
                        shutil.move(src, dst)
            if d == "god":
                for filename in os.listdir(source_folder):
                    file_date = filename[3:-4]
                    if file_date != mouth_god:
                        src = os.path.join(source_folder, filename)
                        dst = os.path.join(destination_folder, filename)
                        shutil.move(src, dst)
            if d == "History":
                for filename in os.listdir(source_folder):
                    file_date = filename[6:-4]
                    if file_date != god:
                        src = os.path.join(source_folder, filename)
                        dst = os.path.join(destination_folder, filename)
                        shutil.move(src, dst)
        # Сортировка файлов продаж
        tudey_day = PUT + "♀Продажи\\текущий день\\"
        tudey_month = PUT + "♀Продажи\\текущий месяц\\"
        tudey_year = PUT + "♀Продажи\\2023\\"
        history = PUT + "♀Продажи\\История\\"
        # Перемещение файлов из текущий месяц в текущего дня
        move_files(tudey_month, tudey_day, "%d.%m.%Y", "day")
        # Перемещение файлов из текущий месяц в текущего дня
        move_files(tudey_day, tudey_month, "%d.%m.%Y", "month")
        # Перемещение файлов из текущего месяца в папку 2023
        move_files(tudey_month, tudey_year, "%d.%m.%Y","god")
        # Перемещение файлов из папки 2023 в папку История
        move_files(tudey_year,history, "%d.%m.%Y","History")
    def sort_files_chek(self):
        def move_files(source_folder, destination_folder, date_pattern, d):
            day = datetime.datetime.now().strftime(date_pattern)
            mouth_god = datetime.datetime.now().strftime(date_pattern)[3:]
            god = datetime.datetime.now().strftime(date_pattern)[6:]
            if d == "day":
                for filename in os.listdir(source_folder):
                    file_date = filename[:-4]
                    if file_date == day:
                        src = os.path.join(source_folder, filename)
                        dst = os.path.join(destination_folder, filename)
                        shutil.move(src, dst)
            if d == "month":
                for filename in os.listdir(source_folder):
                    file_date = filename[:-4]
                    if file_date != day:
                        src = os.path.join(source_folder, filename)
                        dst = os.path.join(destination_folder, filename)
                        shutil.move(src, dst)
            if d == "god":
                for filename in os.listdir(source_folder):
                    file_date = filename[3:-4]
                    if file_date != mouth_god:
                        src = os.path.join(source_folder, filename)
                        dst = os.path.join(destination_folder, filename)
                        shutil.move(src, dst)
            if d == "History":
                for filename in os.listdir(source_folder):
                    file_date = filename[6:-4]
                    if file_date != god:
                        src = os.path.join(source_folder, filename)
                        dst = os.path.join(destination_folder, filename)
                        shutil.move(src, dst)
        # Сортировка файлов продаж
        tudey_day = PUT + "♀Чеки\\Чеки текущий день\\"
        tudey_year = PUT + "♀Чеки\\2023\\"
        history = PUT + "♀Чеки\\История\\"
        # Перемещение файлов из текущий месяц в текущего дня
        move_files(tudey_year, tudey_day, "%d.%m.%Y", "day")
        # Перемещение файлов из текущий месяц в текущего дня
        move_files(tudey_day, tudey_year, "%d.%m.%Y", "month")
        # Перемещение файлов из папки 2023 в папку История
        move_files(tudey_year, history, "%d.%m.%Y", "History")
    def sort_files_spis(self):
        def move_files(source_folder, destination_folder, date_pattern, d):
            day = datetime.datetime.now().strftime(date_pattern)
            mouth_god = datetime.datetime.now().strftime(date_pattern)[3:]
            god = datetime.datetime.now().strftime(date_pattern)[6:]
            if d == "month":
                for filename in os.listdir(source_folder):
                    file_date = filename[3:-4]
                    if file_date == mouth_god:
                        src = os.path.join(source_folder, filename)
                        dst = os.path.join(destination_folder, filename)
                        shutil.move(src, dst)
        # Сортировка файлов продаж
        tudey_month = PUT + "♀Списания\\Текущий месяц\\"
        history = PUT + "♀Списания\\История\\"
        # Перемещение файлов из текущий месяц в текущего дня
        move_files(history,tudey_month, "%d.%m.%Y", "month")
        #move_files(history,tudey_month,  "%d.%m.%Y", "month")
    def sort_files_sebes(self):
        def move_files(tudey_month, history, date_pattern, d):
            day = datetime.datetime.now().strftime(date_pattern)
            mouth_god = datetime.datetime.now().strftime(date_pattern)[3:]
            god = datetime.datetime.now().strftime(date_pattern)[6:]

            if d == "month":
                for filename in os.listdir(tudey_month):
                    file_date = filename[3:-4]

                    if file_date != mouth_god:
                        src = os.path.join(tudey_month, filename)
                        dst = os.path.join(history, filename)
                        shutil.move(src, dst)
            """if d == "history":
                for filename in os.listdir(source_folder):
                    file_date = filename[3:-4]
                    if file_date != mouth_god:
                        src = os.path.join(source_folder, filename)
                        dst = os.path.join(destination_folder, filename)
                        shutil.move(src, dst)"""
        # Сортировка файлов продаж
        tudey_month = PUT + "♀Сибестоемость\\Текущий месяц\\"
        history = PUT + "♀Сибестоемость\\Архив\\"
        # Перемещение файлов из текущий месяц в текущего дня
        move_files(tudey_month, history, "%d.%m.%Y", "month")
        #move_files(history,tudey_month, "%d.%m.%Y", "history")
    def original(self):
        # Путь до папки с оригинальными файлами
        original_files_path = PUT + "Selenium\\Оригинальные файлы\\"

        # Путь до папки, в которую копировать файлы
        copy_files_path = PUT + "Selenium\\исходники\\"

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
    def sashl_sezn(self):
        if ini.time_seychas < ini.time_bot_vrem:
            print("перемещение шашлычного файда")
            p_palic = "P:\\Фирменная розница\\ФРС\\Данные из 1 С\\Шашлык\\"
            p_local = r"C:\Users\Lebedevvv\Desktop\FRS\Шашлычный"
            for filename in os.listdir(p_palic):
                pabl = os.path.join(p_palic, filename)
                local = os.path.join(p_local, filename)
                shutil.copy(pabl, local)

#SORT().sashl_sezn()
