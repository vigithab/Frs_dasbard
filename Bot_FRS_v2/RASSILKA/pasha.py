import numpy as np
from Bot_FRS_v2.GooGL_TBL import Google as g
import pandas as pd
from Bot_FRS_v2.INI import ini


class Pasha:
    # загрузка таблиц
    def __init__(self):
        pd.set_option("expand_frame_repr", False)
        pd.set_option('display.max_colwidth', None)
        self.Put = ini.PUT

    def Petrov(self):

        tabl = pd.read_csv(self.Put + "♀Вычисляемые_таблицы\\Нарастающие итоги.csv", sep="\t", encoding="utf-8",
                           parse_dates=['дата'], date_format='%Y-%m-%d',
                           dtype={'магазин': str, 'LFL': str}, low_memory=False)
        tabl = tabl.loc[tabl["дата"]>="2023-01-01"]
        tabl = tabl[["дата","магазин","выручка","Количество чеков","план_выручка","план_кол_чеков"]]
        tabl["месяц"] = tabl["дата"].dt.strftime('%Y-%m-01')

        tabl = tabl.groupby(["месяц","магазин"],
                      as_index=False).agg(
            {"выручка":"sum","Количество чеков":"sum","план_выручка":"sum","план_кол_чеков":"sum"}).reset_index(drop=True)

        tabl["Cредний чек факт"] = tabl["выручка"] / tabl["Количество чеков"]
        tabl["Cредний чек план"] = tabl["план_выручка"] / tabl["план_кол_чеков"]

        tab = tabl["выручка"].sum() / tabl["Количество чеков"].sum()
        print(tab)
        tab = tabl["план_выручка"].sum() / tabl["план_кол_чеков"].sum()
        print(tab)


        tabl =  tabl[["месяц","магазин","Cредний чек факт","Cредний чек план"]]

        tabl["месяц"] = tabl["месяц"].astype(str)
        tabl.replace([np.inf, -np.inf], np.nan, inplace=True)
        tabl.fillna('', inplace=True)

        g.tbl_bot().svodniy_itog(name_tbl="Средний_чек_Паша", df=tabl,
                                 sheet_name="Средний_чек_Паша")
        print(tabl)
        return


pa = Pasha()
pa.Petrov()

