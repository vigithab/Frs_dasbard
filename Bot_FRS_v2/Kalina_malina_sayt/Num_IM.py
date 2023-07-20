import os
import datetime

import pandas as pd
from Bot_FRS_v2.INI import Float, log, rename, ini, memory

pd.set_option("expand_frame_repr", False)
pd.set_option('display.max_colwidth', None)

class spr_cl():
    def __init__(self):
        spr = pd.read_csv(r"C:\Users\lebedevvv\Desktop\Список товаров ИМ.txt", sep="\t", encoding="utf-8")
        spr_clous = spr.loc[spr["Входит в группу"] != "Хозы"]
        count = len(spr)
        print("всего", count)

        self.spr_clous = spr.loc[spr["Пометка удаления"] == "Да"]
        count_clous = len(self.spr_clous)
        print("Закрытых всего", count_clous)

        spr_open = spr.loc[spr["Пометка удаления"] == "Нет"]
        spr_open = len(spr_open)
        print("открытых", spr_open)

        self.spr_im = spr.loc[spr["Товар ИМ"] == "Да"]
        count_im_count = len(self.spr_im)
        print("Номенклатура ИМ", count_im_count)

        spr_ii_clous = self.spr_im.loc[self.spr_im["Пометка удаления"] == "Да"]
        spr_ii_clous = len(spr_ii_clous)
        print("Номенклатура ИМ со статусом закрыт", spr_ii_clous)

    def f_1(self):
        unic_nom = pd.DataFrame()
        for root, dirs, files in os.walk(ini.PUT + "Selenium\\исходники\\"):
            for file in files:
                if "2023" in file:
                    dat = os.path.basename(file)[:-5]
                    dat = datetime.datetime.strptime(dat, "%d.%m.%Y")
                    if dat < datetime.datetime.strptime("2023-06-01", "%Y-%m-%d"):
                        print("пропуск", dat)
                        continue
                    else:
                        print("Берем", dat)
                        file_path = os.path.join(root, file)
                        print("Фаил: ", os.path.basename(file_path)[:-5], " / Начат: ",
                              str(datetime.datetime.now())[:-10], )
                        df = pd.read_excel(file_path)
                        df_1 = df[["Наименование товара","Код товара"]]
                        df_1 = df_1.drop_duplicates()
                        df_1 = df_1
                        df_1 = df_1.loc[df_1["Наименование товара"].notnull()]
                        unic_nom = pd.concat([unic_nom,df_1 ],axis=0)
        unic_nom.to_excel(r"C:\Users\lebedevvv\Desktop\1.xlsx", index=False)

        print(unic_nom)
        return unic_nom
    def f_2(self):
        unic_nom = pd.read_excel(r"C:\Users\lebedevvv\Desktop\1.xlsx")
        print(len(unic_nom))
        unic_nom = unic_nom.drop_duplicates()
        print(len(unic_nom))
        print(unic_nom)
        self.spr_im = self.spr_im.rename(columns={"Код SKU": "Код товара"})
        Float.FLOAT().float_colm(name_data=unic_nom, name_col="Код товара")
        Float.FLOAT().float_colm(name_data=self.spr_im, name_col="Код товара")
        unic_nom["Код товара"] = unic_nom["Код товара"].astype(int)
        self.spr_im["Код товара"] = self.spr_im["Код товара"].astype(int)
        unic_nom = pd.merge(unic_nom, self.spr_im, on=["Код товара"], how="left")

        self.spr_clous = self.spr_clous[["Пометка удаления", "Код SKU"]]
        self.spr_clous = self.spr_clous.rename(columns={"Пометка удаления":"Вывод","Код SKU": "Код товара"})
        print(self.spr_clous)
        Float.FLOAT().float_colm(name_data=self.spr_clous, name_col="Код товара")
        unic_nom["Код товара"] = unic_nom["Код товара"].astype(int)
        self.spr_clous["Код товара"] = self.spr_clous["Код товара"].astype(int)
        unic_nom = pd.merge(unic_nom, self.spr_clous, on=["Код товара"], how="left")

        print(unic_nom)
        unic_nom.to_excel(r"C:\Users\lebedevvv\Desktop\Ассортимент_ИМ.xlsx", index=False)



if __name__ == '__main__':
    s = spr_cl()
    s.f_2()









