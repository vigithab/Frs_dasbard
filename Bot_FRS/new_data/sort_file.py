import os
import shutil
import datetime
from Bot_FRS.inf import NASTROYKA as setting
PUT = setting.PUT

def sort_file():
    print("запуск сортировки")
    def sales():
        print("запуск сортировки продаж")
        # Путь до папки текущего месяца
        month_folder_path = PUT + "♀Продажи\\текущий месяц\\"
        # Путь до папки текущего дня
        day_folder_path = PUT + "♀Продажи\\текущий день\\"
        # Получение текущей даты в формате "dd.mm.yyyy"
        current_date = datetime.datetime.now().strftime("%d.%m.%Y")
        # Перемещение файлов из папки текущего месяца в папку текущего дня, если такие файлы существуют
        for filename in os.listdir(month_folder_path):
            if current_date in filename:
                # Файл содержит текущую дату, перемещаем его в папку текущего дня
                src = os.path.join(month_folder_path, filename)
                dst = os.path.join(day_folder_path, filename)
                shutil.move(src, dst)
        # Перемещение файлов из папки текущего дня в папку текущего месяца, если такие файлы существуют
        for filename in os.listdir(day_folder_path):
            if current_date not in filename:
                # Файл не содержит текущую дату, перемещаем его в папку текущего месяца
                src = os.path.join(day_folder_path, filename)
                dst = os.path.join(month_folder_path, filename)
                shutil.move(src, dst)
        for filename in os.listdir(month_folder_path):
            if "2022" in filename:
                file_path = os.path.join(month_folder_path, filename)
                os.remove(file_path)
        return
    def check():
        # Путь до папки текущего месяца
        month_folder_path = PUT + "♀Чеки\\2023\\"
        # Путь до папки текущего дня
        day_folder_path = PUT + "♀Чеки\\Чеки текущий день\\"
        # Получение текущей даты в формате "dd.mm.yyyy"
        current_date = datetime.datetime.now().strftime("%d.%m.%Y")
        # Перемещение файлов из папки текущего месяца в папку текущего дня, если такие файлы существуют
        for filename in os.listdir(month_folder_path):
            if current_date in filename:
                # Файл содержит текущую дату, перемещаем его в папку текущего дня
                src = os.path.join(month_folder_path, filename)
                dst = os.path.join(day_folder_path, filename)
                shutil.move(src, dst)
        # Перемещение файлов из папки текущего дня в папку текущего месяца, если такие файлы существуют
        for filename in os.listdir(day_folder_path):
            if current_date not in filename:
                # Файл не содержит текущую дату, перемещаем его в папку текущего месяца
                src = os.path.join(day_folder_path, filename)
                dst = os.path.join(month_folder_path, filename)
                shutil.move(src, dst)
        for filename in os.listdir(month_folder_path):
            if "2022" in filename:
                file_path = os.path.join(month_folder_path, filename)
                os.remove(file_path)
        return
    def spipsania():
        # Путь до папки истории
        month_folder_path = PUT + "♀Списания\\История\\"
        # Путь до папки месяца
        day_folder_path = PUT + "♀Списания\\Текущий месяц\\"
        # Получение текущей даты в формате "dd.mm.yyyy"
        current_date = datetime.datetime.now()
        # Извлечение номера текущего месяца и года
        month_year = current_date.strftime("%m.%Y")
        # Перемещение файлов из папки текущего месяца в папку текущего дня, если такие файлы существуют
        for filename in os.listdir(month_folder_path):
            if month_year in filename:
                # Файл содержит текущую дату, перемещаем его в папку месяца
                src = os.path.join(month_folder_path, filename)
                dst = os.path.join(day_folder_path, filename)
                shutil.move(src, dst)

        # Получение текущей даты в формате "dd.mm.yyyy"
        current_date = datetime.datetime.now()
        # Извлечение номера текущего дня, месяца и года
        day_month_year = current_date.strftime("%d.%m.%Y")

        # Удаление файлов с текущей датой в названии и расширением .txt из папки day_folder_path
        for filename in os.listdir(day_folder_path):
            if filename.endswith('.txt') and day_month_year in filename:
                file_path = os.path.join(day_folder_path, filename)
                os.remove(file_path)
        return
    def original():
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
                print(f"Файл {filename} скопирован в {copy_files_path}")
        return
    spipsania()
    sales()
    check()
    original()
# сортировка файлов