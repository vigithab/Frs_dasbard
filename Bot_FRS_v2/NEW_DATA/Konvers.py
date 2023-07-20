import datetime
import os
import pandas as pd
from Bot_FRS_v2.INI import ini, Float

pd.set_option("expand_frame_repr", False)
pd.set_option('display.max_colwidth', None)


class konvers():
    def __init__(self):
        pass


    def Chek(self):
        for root, dirs, files in os.walk(ini.PUT + "Selenium\\исходники\\"):
            for file in files:
                if "2023" in file:
                    dat = os.path.basename(file)[:-5]
                    dat = datetime.datetime.strptime(dat, "%d.%m.%Y")

                    print(dat)
                    file_path = os.path.join(root, file)
                    print("Фаил: ", os.path.basename(file_path)[:-5], " / Начат: ",
                          str(datetime.datetime.now())[:-10], )
                    df = pd.read_excel(file_path)
                    df = df.loc[df["Магазин"].notnull()]
                    df["Дата/Время чека"] = pd.to_datetime(df["Дата/Время чека"],
                                                                       format="%d.%m.%Y %H:%M:%S").dt.date
                    df["Касса"] = df["Касса"].astype(str)
                    print(df)
                    df = df.loc[
                        ~((df["Магазин"] == "Таврическая 37") & (df["Касса"] == "4.0"))]
                    sp = ["Касса"]
                    Float.FLOAT().float_colms(name_data=df, name_col=sp)
                    df["Касса"] = df["Касса"].astype(str)
                    df["ID_Chek"] = df["Магазин"].astype(int).astype(str) + \
                                                df["Касса"].astype(str) + \
                                                df["Чек"].astype(int).astype(
                                                    str) + df["Дата/Время чека"].astype(str) + \
                                                df["Смена"].astype(str)

                    print(df)

if __name__ == '__main__':
    s = konvers()
    s.Chek()
