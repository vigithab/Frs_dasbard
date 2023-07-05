# групированные данные на начало недели для юли и жени
import numpy as np
import pandas as pd
from Bot_FRS_v2.BOT_TELEGRAM import BOT
from Bot_FRS_v2.INI import ini
from Bot_FRS_v2.INI import Float
from Bot_FRS_v2.INI import rename
import datetime




class groups:
    def __init__(self):
        self.end_mount = None
        self.PUT = ini.PUT
        # Формирвание списка ТУ
        def ty(name_df):
            # доавление ТУ
            TY, ty_open_magaz = rename.RENAME().TY_Spravochnik()
            TY = TY.loc[TY["Менеджер"].notnull()]
            tabl = name_df.merge(TY, on=["магазин"], how="left").reset_index(drop=True)
            # создание списка ТУ
            ty_list = tabl['Менеджер'].unique().tolist()
            # удаление пустых значений и нан  списк ТУ
            ty_list = [value for value in ty_list if value and not isinstance(value, float)]
            return ty_list, tabl

        self.tabl = pd.read_csv(self.PUT + "♀Вычисляемые_таблицы\\Нарастающие итоги.csv", sep="\t", encoding="utf-8",
                                   parse_dates=['дата'], date_format='%Y-%m-%d',
                                   dtype={'магазин': str, 'LFL': str},low_memory=False)
        # Получение списка всех столбцов, исключая ['магазин', 'LFL', 'дата']
        All_colms = list(set(self.tabl.columns) - {'магазин', 'LFL', 'дата'})
        Float.FLOAT().float_colms(name_data=self.tabl,name_col=All_colms)
        self.ty_list, self.tabl = ty(name_df=self.tabl)
        self.otchet_week_max = max(ini.date_last_week())
        self._otchet_week_min = min(ini.date_last_week())

        self.date_list = ini.date_last_week()

    def tabls(self):
        print(self.ty_list)
        print(self.tabl)
        tabl =self.tabl
        print(self.otchet_week_max)
        print(self._otchet_week_min)
        def otcetnaya_weeck():
            today= datetime.datetime.strptime(self._otchet_week_min, "%Y-%m-%d")
            start_mount = today.replace(day=1)
            next_month = start_mount.replace(month=start_mount.month + 1)
            # Определяем дату конца текущего месяца
            end_mount = next_month - datetime.timedelta(days=1)
            # Вывод результата
            print("Дата конца текущего месяца:",end_mount.strftime("%Y-%m-%d"))

            print(start_mount)
            print(end_mount)
            # тчетная неделя
            tabl_otchetnaya = tabl.loc[(tabl["дата"] >= start_mount ) & (tabl["дата"] <= end_mount)]

            return tabl_otchetnaya, start_mount

        def last_weeck(start):
            otchet_week_max=datetime.datetime.strptime(self.otchet_week_max, "%Y-%m-%d")
            end_last_weeck =  otchet_week_max - datetime.timedelta(days=7)
            last_otchtnaya = tabl.loc[(tabl["дата"]>=start) & (tabl["дата"]<=end_last_weeck)]
            print(last_otchtnaya)

            sales = ((last_otchtnaya['выручка'].sum() / last_otchtnaya["Прошло дней"].max() *
                                   last_otchtnaya["осталось дней"].min() ) + last_otchtnaya['выручка'].sum() ).astype(int)

            chek  =
            aver_chek = last_otchtnaya['Средний чек'].mean().astype(int)
            count_TT = last_otchtnaya[last_otchtnaya['выручка'] > 1000]['магазин'].nunique()



            # Список значений
            values = [['Выручка',sales],

                      ['Средний чек', aver_chek],
                      ["Проникновение лояльности", np.nan],
                      [''],
                      ["Всего ТТ",count_TT],
                      ["Кол-во убыточных", np.nan],
                      ["Чеков",last_otchtnaya["Количество чеков"].sum().astype(int)],
                      ["Списания, %"],
                      ["Продажи, кг"],
                      ["Выручка"],
                      ["Прибыль (до вычета роялти)"],
                      ["Re, %"],
                      [''],
                      ["Прибыль (до вычета роялти):"],
                      ["ФРС"],
                      ["Франшиза в аренду"],
                      ["Франшиза инвестиционная"],
                      [''],
                      ["Re, %:"],
                      ["ФРС"],
                      ["Франшиза в аренду"],
                      ["Франшиза инвестиционная"]]

            # Создание DataFrame из списка значений
            last_otchtnaya = pd.DataFrame(values, columns=['Показатель', 'Прошлая неделя'])



            return last_otchtnaya
        # тчетная неделя
        tabl_otchetnaya, start_mount = otcetnaya_weeck()

        # прошлая неделя
        last_otchtnaya = last_weeck(start_mount)
        print(last_otchtnaya)














groups = groups()
groups.tabls()