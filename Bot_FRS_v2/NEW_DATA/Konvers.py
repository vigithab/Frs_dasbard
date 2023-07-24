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

        pass
    def selenium_day_chek(self):
        for root, dirs, files in os.walk(ini.PUT + "Selenium\\исходники\\"):
            for file in files:
                if "2023" in file:
                    dat = os.path.basename(file)[:-5]
                    dat = datetime.datetime.strptime(dat, "%d.%m.%Y")
                    print(dat)
                    file_path = os.path.join(root, file)
                    print("Фаил: ", os.path.basename(file_path)[:-5], " / Начат: ",
                          str(datetime.datetime.now())[:-10], )
                    name_datafreme = pd.read_excel(file_path)
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
                    spqr, sprav_magaz, open_mag = rename.RENAME().magazin_info()
                    name_datafreme = name_datafreme.rename(columns={"Магазин": 'ID'})
                    name_datafreme = name_datafreme.merge(spqr[['!МАГАЗИН!', 'ID']], on='ID', how="left")
                    name_datafreme = name_datafreme.loc[name_datafreme["!МАГАЗИН!"].notnull()]
                    name_datafreme["Дата/Время чека"] = pd.to_datetime(name_datafreme["Дата/Время чека"],
                                                           format="%d.%m.%Y %H:%M:%S").dt.date

                    memory.MEMORY().mem_total(x="Формирование чеков: ")
                    name_datafreme["Касса"] = name_datafreme["Касса"].astype(str)
                    name_datafreme = name_datafreme.loc[
                        ~((name_datafreme["!МАГАЗИН!"] == "Таврическая 37") & (name_datafreme["Касса"] == "4.0"))]
                    sp = ["Касса"]
                    Float.FLOAT().float_colms(name_data=name_datafreme,name_col=sp)

                    def cnevk_num(tip):
                        df = name_datafreme[["Тип", "!МАГАЗИН!", "ID", "Дата/Время чека", 'номенклатура_1с',"Касса",
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
                        df["ID_Chek"] = df["ID"].astype(int).astype(str) + \
                                                    df["Касса"].astype(int).astype(str) + \
                                                    df["Чек"].astype(int).astype(
                            str) + df["Дата/Время чека"].astype(str) + df["Смена"].astype(str)
                        df = df.drop(["Касса", "Чек","Смена"], axis=1)

                        nom_list = df['номенклатура_1с'].unique().tolist()
                        print(nom_list)
                        df_itog = pd.DataFrame()
                        for i in nom_list:
                            print(i)
                            df_filter = df.loc[df['номенклатура_1с'] == i ]
                            # групировка по магазинам
                            df_filter = df_filter.groupby(["Дата/Время чека", "ID",'номенклатура_1с',"!МАГАЗИН!"],
                                                          as_index=False) \
                                .agg({'ID_Chek': "nunique"}).reset_index(drop=True)
                            if tip =="Продажа":
                                df_filter = df_filter.rename(columns={'ID_Chek':"Встречалось раз в чеках"})
                            else:
                                df_filter = df_filter.rename(columns={'ID_Chek': "Возврат раз в чеках"})
                            df_itog = pd.concat([df_itog,  df_filter], axis=0)


                        return df_itog

                    def cnevk(tip):
                        sales_day_cehk = name_datafreme[["Тип","!МАГАЗИН!", "ID", "Дата/Время чека", "Касса", "Чек",
                                                         "Стоимость позиции", "Код товара","Смена"]]
                        if tip=="Продажа":
                            sales_day_cehk = sales_day_cehk.loc[(sales_day_cehk["Тип"] == tip) | (sales_day_cehk["Тип"] ==
                                                                                                  "Возврат")]
                            sales_day_cehk = sales_day_cehk.drop(["Тип"], axis=1)
                        else:
                            sales_day_cehk = sales_day_cehk.loc[(sales_day_cehk["Тип"] == tip)]
                            sales_day_cehk = sales_day_cehk.drop(["Тип"], axis=1)

                        sales_day_cehk["Дата/Время чека"] = pd.to_datetime(sales_day_cehk["Дата/Время чека"],
                                                                           format="%d.%m.%Y %H:%M:%S").dt.date
                        # Формирование ID Чека
                        sales_day_cehk["ID_Chek"] = sales_day_cehk["ID"].astype(int).astype(str) + \
                                                    sales_day_cehk["Касса"].astype(int).astype(str) + \
                                                    sales_day_cehk["Чек"].astype(int).astype(
                            str) + sales_day_cehk["Дата/Время чека"].astype(str) + sales_day_cehk["Смена"].astype(str)

                        sales_day_cehk = sales_day_cehk.drop(["Касса", "Чек","Смена"], axis=1)
                        # удаление не нужных символов
                        Float.FLOAT().float_colm(name_data=sales_day_cehk, name_col="Стоимость позиции")
                        # Групировки по дням
                        sales_day_cehk = sales_day_cehk.groupby(["!МАГАЗИН!", "ID", "Дата/Время чека", "ID_Chek"],
                                                                as_index=False).agg({
                            "Стоимость позиции": "sum",
                            "Код товара": [("Количество товаров в чеке", "count"), ("Количество уникальных товаров в чеке",
                                                                                    "nunique")]})

                        # переименовываем столбцы
                        sales_day_cehk.columns = ['!МАГАЗИН!', "ID", 'Дата/Время чека', 'ID_Chek', 'Стоимость позиции',
                                                  'Количество товаров в чеке',
                                             'Количество уникальных товаров в чеке']
                        # выбираем нужные столбцы и сортируем по дате/времени чека в порядке убывания
                        sales_day_cehk = sales_day_cehk[
                            ["ID", '!МАГАЗИН!', 'Дата/Время чека', 'ID_Chek', 'Стоимость позиции', 'Количество товаров в чеке',
                             'Количество уникальных товаров в чеке']] \
                            .sort_values('Дата/Время чека', ascending=False) \
                            .reset_index(drop=True)
                        # групировка по магазинам
                        sales_day_cehk = sales_day_cehk.groupby(["ID", "!МАГАЗИН!", "Дата/Время чека"], as_index=False) \
                            .agg({"Стоимость позиции": "sum",
                                  'ID_Chek': "count",
                                  "Количество товаров в чеке": "mean",
                                  "Количество уникальных товаров в чеке": "mean"}) \
                            .sort_values("Дата/Время чека", ascending=False).reset_index(drop=True)

                        # дбавление среднего чека
                        sales_day_cehk["Средний чек"] = sales_day_cehk["Стоимость позиции"] / sales_day_cehk["ID_Chek"]
                        # переименование столбцов
                        sales_day_cehk = sales_day_cehk.rename(columns=
                                                               { "Дата/Время чека": "дата",
                                                                "Стоимость позиции": "выручка",
                                                                "ID_Chek": "Количество чеков",
                                                                "Количество товаров в чеке": "количество товаров в чеке",
                                                                "Количество уникальных товаров в чеке": "количество уникальных товаров в чеке"})
                        # округление
                        sales_day_cehk= sales_day_cehk.round(2)
                        sales_day_cehk['filename'] = dat
                        sales_day_cehk = sales_day_cehk.drop(['дата'], axis=1)
                        sales_day_cehk = sales_day_cehk.rename(columns={'filename': 'дата'})
                        sales_day_cehk["дата"] = pd.to_datetime(sales_day_cehk["дата"], format='%d.%m.%Y')

                        #memory.MEMORY().mem_total(x="Обработан - Фаил чеков: " + str(name_file))
                        return sales_day_cehk

                    df_itog = cnevk_num(tip="Продажа")
                    vozvrat = cnevk_num(tip="Возврат")

                    df_itog = df_itog.merge(vozvrat[["Возврат раз в чеках",'номенклатура_1с',"ID"]],
                                            on=['номенклатура_1с',"ID"], how="left").reset_index(drop=True)

                    df_itog = df_itog[["Дата/Время чека","ID","!МАГАЗИН!","номенклатура_1с","Встречалось раз в чеках",
                                       "Возврат раз в чеках"]]


                    date_obj = dat

                    try:
                        year = str(date_obj.year)  # Получение года в виде строки
                        old_locale = locale.getlocale(locale.LC_TIME)
                        locale.setlocale(locale.LC_TIME, 'ru_RU')
                        # Получить текущий месяц и год в формате строки
                        month = dat.strftime('%B')
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

                        df_itog.to_csv(year_month_dir + f"{str(dat)[:-9]}_num.csv", index=False)
                    except:
                        zx = "Ошибка при обработке конверсии номенклатура"
                        print(zx)
                        BOT.BOT().bot_mes_html(mes=zx, silka=0)

        return

if __name__ == '__main__':
    s = konvers()
    s.selenium_day_chek()
