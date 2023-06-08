import os
import pandas as pd
pd.set_option("expand_frame_repr", False)
pd.set_option('display.max_colwidth', None)
# Путь к папке, в которой находятся исходные файлы
folder_path = r'C:\Users\lebedevvv\Desktop\Дашборд_бот\NEW\ОБРАБОТКА ОШИБОК\разница сумм'

# Путь к папке, в которую будут сохраняться файлы, удовлетворяющие условиям
output_folder_path = r'C:\Users\lebedevvv\Desktop\Дашборд_бот\NEW\ОБРАБОТКА ОШИБОК'

# Создаем пустой DataFrame, в который будут добавляться данные из файлов
combined_df = pd.DataFrame()

# Проходимся по всем файлам в папке
for file_name in os.listdir(folder_path):
    if file_name.endswith('.xlsx'):
        file_path = os.path.join(folder_path, file_name)


        # Читаем данные из файла
        df = pd.read_excel(file_path)
        print(df)
        # Оставляем только строки, удовлетворяющие условиям
        mask = ((df['Разница DSH/1 с'].abs() > 10) | (df['Разница DSH/1 с'].abs() < -10))\
               | ((df['Разница DSH/Инфовижен(к)'].abs() > 10)
                | (df['Разница DSH/Инфовижен(к)'].abs() < -10)) | \
               ((df['1 с / Инфовижен(к)'].abs() > 10) | (df['1 с / Инфовижен(к)'].abs() < -10))
        filtered_df = df.loc[mask]

        # Добавляем данные в объединенный DataFrame
        combined_df = pd.concat([combined_df, filtered_df])

        # Сохраняем файл, если есть хотя бы одна строка, удовлетворяющая условиям
        if not filtered_df.empty:
            output_file_name = os.path.splitext(file_name)[0] + '_filtered.xlsx'
            output_file_path = os.path.join(output_folder_path, output_file_name)
            filtered_df.to_excel(output_file_path, index=False)

# Сохраняем объединенный DataFrame в файл
combined_file_path = os.path.join(output_folder_path, 'combined_filtered.xlsx')
combined_df.to_excel(combined_file_path, index=False)