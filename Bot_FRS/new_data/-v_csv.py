import os
import csv
import pandas as pd

# Функция для конвертации файла Excel в CSV
def convert_excel_to_csv(excel_file, csv_file):
    df = pd.read_excel(excel_file)  # Чтение файла Excel с помощью Pandas
    df.to_csv(csv_file,sep="\t", encoding="ANSI")  # Сохранение данных в формате CSV

# Функция для конвертации текстового файла в CSV
def convert_txt_to_csv(txt_file, csv_file):
    with open(txt_file, 'r') as file:
        lines = file.readlines()  # Чтение всех строк из текстового файла
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows([line.strip().split('\t') for line in lines])  # Запись данных в CSV

# Путь к исходной папке
source_directory = r'C:\Users\lebedevvv\Desktop\Дашборд_бот\♀Продажи'

# Путь к целевой папке
target_directory = r'C:\Users\lebedevvv\Desktop\Дашборд_бот\♀Продажи_csv'

# Рекурсивно обходим все файлы и подпапки в исходной папке
for root, dirs, files in os.walk(source_directory):
    for file in files:
        file_path = os.path.join(root, file)
        file_name, file_extension = os.path.splitext(file)

        # Проверяем расширение файла
        if file_extension.lower() == '.xls' or file_extension.lower() == '.xlsx':
            csv_file_path = os.path.join(target_directory, file_name + '.csv')
            convert_excel_to_csv(file_path, csv_file_path)
        elif file_extension.lower() == '.txt':
            csv_file_path = os.path.join(target_directory, file_name + '.csv')
            convert_txt_to_csv(file_path, csv_file_path)