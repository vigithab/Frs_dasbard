import sys
sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON\venv\Lib\site-packages")
sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON")
import datetime
import locale
import os
import pandas as pd
from Bot_FRS_v2.INI import ini, Float, memory, rename
from Bot_FRS_v2.BOT_TELEGRAM import BOT

pd.set_option("expand_frame_repr", False)
pd.set_option('display.max_colwidth', None)

class konvers():
    def __init__(self):
        print("Оработка конверсии...")
        pd.set_option("expand_frame_repr", False)
        pd.set_option('display.max_colwidth', None)

    def selenium_day_chek(self, name_datafreme, name_file):
        name_datafreme = name_datafreme.rename(columns={"ID": "Магазин"})
        name_datafreme = name_datafreme.loc[name_datafreme["Магазин"].notnull()]
        # ######################################## Загузка названий с 1 с
        spravka_nom = pd.read_csv(ini.PUT + "Справочники\\номенклатура\\Список.txt", sep="\t",
                                  encoding="utf-8")
        spravka_nom = spravka_nom.rename(
            columns={"Номенклатура": "номенклатура_1с", "Код SKU": "Код товара"})
        # единый формат столбца длясоеденения
        Float.FLOAT().float_colm(name_data=name_datafreme, name_col="Код товара")
        name_datafreme["Код товара"] = name_datafreme["Код товара"].astype(int).astype(str)
        Float.FLOAT().float_colm(name_data=spravka_nom, name_col="Код товара")
        spravka_nom["Код товара"] = spravka_nom["Код товара"].astype(int).astype(str)

        name_datafreme = name_datafreme.merge(spravka_nom[['номенклатура_1с', "Код товара"]],
                                                on=["Код товара"], how="left").reset_index(drop=True)

        #####################################################################
        name_datafreme["Дата/Время чека"] = pd.to_datetime(name_datafreme["Дата/Время чека"],
                                               format="%d.%m.%Y %H:%M:%S").dt.date

        memory.MEMORY().mem_total(x="Обработка конверсии:")
        name_datafreme["Касса"] = name_datafreme["Касса"].astype(str)
        name_datafreme = name_datafreme.loc[
            ~((name_datafreme["!МАГАЗИН!"] == "Таврическая 37") & (name_datafreme["Касса"] == "4.0"))]
        sp = ["Касса"]
        Float.FLOAT().float_colms(name_data=name_datafreme,name_col=sp)

        def cnevk_num(tip):
            df = name_datafreme[["Тип", "!МАГАЗИН!","Магазин", "Дата/Время чека", 'номенклатура_1с',"Касса",
                                 "Чек","Стоимость позиции", "Код товара", "Смена",]]

            if tip=="Продажа":
                df = df.loc[(df["Тип"] == tip) | (df["Тип"] =="Возврат")]
                df = df.drop(["Тип"], axis=1)
            else:
                df = df.loc[(df["Тип"] == tip)]
                df = df.drop(["Тип"], axis=1)

            df["Дата/Время чека"] = pd.to_datetime(df["Дата/Время чека"],
                                                               format="%d.%m.%Y %H:%M:%S").dt.date
            # Формирование ID Чека
            df["ID_Chek"] = df["Магазин"].astype(int).astype(str) + \
                                        df["Касса"].astype(int).astype(str) + \
                                        df["Чек"].astype(int).astype(
                str) + df["Дата/Время чека"].astype(str) + df["Смена"].astype(str)
            df = df.drop(["Касса", "Чек","Смена"], axis=1)

            nom_list = df['номенклатура_1с'].unique().tolist()
            df_itog = pd.DataFrame()
            for i in nom_list:
                df_filter = df.loc[df['номенклатура_1с'] == i ]
                # групировка по магазинам
                df_filter = df_filter.groupby(["Дата/Время чека", "Магазин",'номенклатура_1с',"!МАГАЗИН!"],
                                              as_index=False) \
                    .agg({'ID_Chek': "nunique"}).reset_index(drop=True)
                if tip =="Продажа":
                    df_filter = df_filter.rename(columns={'ID_Chek':"Встречалось раз в чеках"})
                else:
                    df_filter = df_filter.rename(columns={'ID_Chek': "Возврат раз в чеках"})
                df_itog = pd.concat([df_itog,  df_filter], axis=0)
            return df_itog


        df_itog = cnevk_num(tip="Продажа")
        vozvrat = cnevk_num(tip="Возврат")

        df_itog = df_itog.merge(vozvrat[["Возврат раз в чеках",'номенклатура_1с',"Магазин"]],
                                on=['номенклатура_1с',"Магазин"], how="left").reset_index(drop=True)
        df_itog  = df_itog .rename(columns={"Магазин": "ID"})
        df_itog = df_itog[["Дата/Время чека","ID","!МАГАЗИН!","номенклатура_1с","Встречалось раз в чеках",
                           "Возврат раз в чеках"]]
        date_obj = name_file[:-5]
        date_obj = datetime.datetime.strptime(date_obj, "%d.%m.%Y").date()

        try:
            year = str(date_obj.year)  # Получение года в виде строки
            old_locale = locale.getlocale(locale.LC_TIME)
            locale.setlocale(locale.LC_TIME, 'ru_RU')
            # Получить текущий месяц и год в формате строки
            month = date_obj.strftime('%B')
            # вернуть локаль
            locale.setlocale(locale.LC_TIME, old_locale)

            base_dir = \
                "P:\\Фирменная розница\\ФРС\\Данные из 1 С\\Чеки_Сгруппированные_конверсия\\" \
                "По_номенклатуре\\"  # Базовый каталог, в котором будут создаваться папки

            # Сочетание года и месяца в одной строке, разделенной символом '/'
            year_month_dir = os.path.join(base_dir, f"{year}\\{month}\\")

            # Проверка наличия папки года-месяца и создание при необходимости
            if not os.path.exists(year_month_dir):
                os.makedirs(year_month_dir)

            df_itog.to_csv(year_month_dir + f"{str(name_file)[:-5]}_num.csv", index=False)
        except:
            zx = "Ошибка при обработке конверсии номенклатура"
            print(zx)
            BOT.BOT().bot_mes_html(mes=zx, silka=0)
        return

