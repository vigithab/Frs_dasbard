import sys

import numpy as np

sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON\venv\Lib\site-packages")
sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON")

import pandas as pd
from Bot_FRS_v2.INI.ini import PUT
from Bot_FRS_v2.INI import rename
from Bot_FRS_v2.INI import Float
from Bot_FRS_v2.GooGL_TBL import Google as g

pd.set_option("expand_frame_repr", False)
pd.set_option('display.max_colwidth', None)


class tabl_count_tt():
    def __init__(self):
        self.name_month = {
            1: "Январь",
            2: "Февраль",
            3: "Март",
            4: "Апрель",
            5: "Май",
            6: "Июнь",
            7: "Июль",
            8: "Август",
            9: "Сентябрь",
            10: "Октябрь",
            11: "Ноябрь",
            12: "Декабрь"}

        tabl = pd.read_csv(PUT + "♀Вычисляемые_таблицы\\Нарастающие итоги.csv", sep="\t", encoding="utf-8",
                                   parse_dates=['дата'], date_format='%Y-%m-%d',
                                   dtype={'магазин': str, 'LFL': str},low_memory=False)
        print(tabl)
        tabl = tabl.loc[tabl["год"] != 2021]
        Float.FLOAT().float_colm(name_data=tabl,name_col="выручка")
        tabl = tabl.loc[tabl["выручка"] > 5000]
        tabl = tabl[["магазин","год","месяц"]]
        spqr, sprav_magaz, open_mag = rename.RENAME().magazin_info()
        sprav_magaz = sprav_magaz.rename(columns={"!МАГАЗИН!": "магазин"})

        sprav_magaz = sprav_magaz[["магазин","МАГАЗИН","!ГОРОД!","!ОБЛАСТЬ!","Канал"]]
        tabl = tabl.merge(sprav_magaz,on=["магазин"], how="left").reset_index(drop=True)
        self.tabl =tabl.groupby(["!ГОРОД!","год","месяц"],
                                           as_index=False).agg(
            {"магазин": "nunique"}).reset_index(drop=True)



    def tabl_form(self):
        df = self.tabl
        df["месяц_s"] = df["месяц"]
        # Замена значений столбца "месяц" на значения из словаря
        df["месяц"] = df["месяц"].map(self.name_month)

        # Объединение столбцов "год" и "месяц" в один столбец
        df["год_месяц"] = df["год"].astype(str) + "-" + df["месяц"]
        # Преобразование столбца "год_месяц" в столбцы
        df_pivot = df.pivot(index=["год_месяц","месяц_s","год"], columns="!ГОРОД!", values="магазин")

        df_pivot = df_pivot.reset_index()
        df_pivot = df_pivot.sort_values(by=["год", "месяц_s"], ascending=[False, False])
        df_pivot = df_pivot.drop(columns=["месяц_s", "год"])
        df_pivot = df_pivot.rename(columns={"год_месяц": "Месяц и год"})

        df_pivot .replace([np.inf, -np.inf], np.nan, inplace=True)
        df_pivot .fillna('', inplace=True)
        
        
        
        g.tbl_bot().svodniy_itog(name_tbl="Количество магазинов сети", df=df_pivot, sheet_name="Количество магазинов сети")



        """# Получение порядка столбцов на основе ключей словаря
        sorted_columns = [f"{year}-{self.name_month[month]}" for year in df["год"].unique() for month in
                          sorted(self.name_month.keys())]

        # Переупорядочивание столбцов в DataFrame
        df_pivot = df_pivot.reindex(sorted_columns, axis=1)"""


        return df_pivot



if __name__ == '__main__':
    # Запуск асинхронной программы
    run = tabl_count_tt()
    df_pivot = run.tabl_form()
    print(df_pivot)

