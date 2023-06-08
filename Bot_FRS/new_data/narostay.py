from datetime import date, timedelta
import os
import pandas as pd
import gc
import numpy as np
from Bot_FRS.inf import NASTROYKA as setting
from Bot_FRS.inf import memory as memory

pd.set_option("expand_frame_repr", False)
pd.set_option('display.max_colwidth', None)

PUT = setting.PUT


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


previous_data = None  # Переменная для хранения данных предыдущего файла

files = setting.god_todey()  # Список файлов для обработки

for file in files:
    print(file)
    file_p = file + '.xlsx'
    folder1 = PUT + "♀Продажи\\Сводные таблицы\\2023"
    folder2 = PUT + "♀Продажи\\2023\\"

    # folder3 = PUT + "♀Продажи\\История\\"
    for folder in [folder1, folder2]:
        file_path = os.path.join(folder, file_p)
        print(file_path)
        if os.path.exists(file_path):
            x = pd.read_excel(file_path, parse_dates=["Дата/Время чека"], date_format='%Y-%m-%d %H:%M:%S')
            y = x[["Дата/Время чека", "!МАГАЗИН!", "номенклатура_1с", "Стоимость позиции"]]

            del x
            gc.collect()
            # перименование столбцов
            y = y.rename(columns={"!МАГАЗИН!": "магазин", "номенклатура_1с": 'Номенклатура',
                                  "Стоимость позиции": "выручка", "Дата/Время чека": "дата"})
            # перевод во float
            len_float = ["выручка"]
            FLOAT().float_colms(name_data=y, name_col=len_float)
            # группировка таблицы
            y = y.groupby(["магазин", "дата"], as_index=False).agg({"выручка": "sum"}).reset_index(drop=True)

            # Создаем пустой DataFrame для хранения результатов
            result_df = pd.DataFrame(columns=['дата', 'Магазин', 'выручка'])

            # Проходимся по каждому файлу

            # Читаем данные из файла Excel
            df = pd.read_excel(file_path)
            # Получаем дату из имени файла или из нужного столбца в файле
            date = df.iloc[0, 0]  # Предполагается, что дата находится в первой строке и первом столбце
            # Обрабатываем каждую строку с данными
            for _, row in df.iloc[1:].iterrows():
                shop = row['магазин']
                revenue = row['выручка']
                # Добавляем данные в DataFrame
                result_df = result_df.append({'дата': date, 'магазин': shop, 'выручка': revenue}, ignore_index=True)

        # Группируем данные по дате и магазину, а затем суммируем выручку
        result_df['выручка'] = result_df.groupby(['дата', 'магазин'])['выручка'].cumsum()

        # Выводим результат

        memory.MEMORY().mem_total(x=file)

# Сохраните итоговый DataFrame в файл
result.to_csv(PUT + "♀Продажи\\Сводные таблицы\\Нарастающий_итог.csv", encoding="utf-8", sep=';',
                      index=False, decimal='.')