# групированные данные на начало недели для юли и жени
import os

import numpy as np
import pandas as pd
from Bot_FRS_v2.BOT_TELEGRAM import BOT
from Bot_FRS_v2.INI import ini
from Bot_FRS_v2.INI import Float
from Bot_FRS_v2.INI import rename
import datetime
from Bot_FRS_v2.GooGL_TBL import Google as g

class groups:
    # загрузка таблиц
    def __init__(self):
        self.list_last_year_total = None
        self.list_last_year = None
        self.list_last_month_MTD  = None
        self.list_last_month = None
        self.list_month = None
        self.PUT = ini.PUT
        format_date_str = "%Y-%m-%d"
        self.date_todey = ini.dat_seychas
        print(self.date_todey)
        # нумерация понедельников
        def num_pn():
            date_toodey_str = datetime.date.today().strftime(format_date_str)
            num_pn = ini.num_pn(yea=ini.dat_seychas.year, mon=ini.dat_seychas.month)
            priznak_pn = num_pn.get(date_toodey_str)

            priznak_pn = 1

            return priznak_pn
        # ЗАГРУЗКА ДАННЫХ ФИНРЕЗА И ОРАБОТКА
        def finrez():
            for files in os.listdir(self.PUT + "Финрез\\Исходник\\"):
                FINREZ = pd.read_excel(self.PUT + "Финрез\\Исходник\\" + files, sheet_name="Динамика ТТ исходник")
                FINREZ = FINREZ.rename(columns={"Торговая точка": "магазин", "Дата": "дата",
                                                "Канал": "канал",
                                                "Режим налогообложения": "режим налогообложения",
                                                "Канал на последний закрытый период": "канал на последний закрытый период"})

                FINREZ = FINREZ.loc[FINREZ['дата'] >= "2022-01-01"]
                FINREZ = rename.RENAME().Rread(name_data=FINREZ, name_col="магазин")

                tabl = tabl.merge(
                    FINREZ[['магазин', "дата", "* Прибыль (+) / Убыток (-) (= Т- ОЕ)  БЕЗ РОЯЛТИ ФРС", "Re, %"]],
                    on=["магазин", "дата"], how="left").reset_index(drop=True)
                tabl = tabl.rename(
                    columns={"* Прибыль (+) / Убыток (-) (= Т- ОЕ)  БЕЗ РОЯЛТИ ФРС": "Прибыль (до вычета роялти):",
                             "* Рентабельность БЕЗ РОЯЛТИ ФРС, %": "Re, %"})

                tabl.loc[:, "Re, %"] = tabl["Re, %"].astype(str).replace("-", 0)
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
        # ЗАГРУЗКА СВОДНОЙ ТАБЛИЦЫ
        def svod():
            tabl = pd.read_csv(self.PUT + "♀Вычисляемые_таблицы\\Нарастающие итоги.csv", sep="\t", encoding="utf-8",
                                       parse_dates=['дата'], date_format='%Y-%m-%d',
                                       dtype={'магазин': str, 'LFL': str},low_memory=False)

            return tabl
        # ЗАГРУЗКА КАНАЛОВ
        def kanal():
            spqr, sprav_magaz, open_mag = rename.RENAME().magazin_info()
            open_mag = open_mag[["!МАГАЗИН!","Канал"]]
            kanal = open_mag.rename(columns={"!МАГАЗИН!": "магазин",
                                            "Канал": "канал"})
            # ОЬЕДЕНЕНИЕ  КАНАЛОВ
            tabl = svod().merge(kanal, on=["магазин"], how="left").reset_index(drop=True)
            # выбор столбцов
            tabl = tabl[["дата", "Прошло дней", "осталось дней", "магазин", 'канал', 'выручка', 'Количество чеков',
                         'Средний чек', "вес_продаж", "списания_оказатель"]]
            return tabl
        # формирование список дат [Отчетная неделя]
        def weeck_onchet():
            if num_pn() == 1:
                print("Неделя прочая", num_pn())
                # список дат текущего месяца
                min_date = self.date_todey.replace(day=1)
                # список дат отчетной недели
                self.list_month = pd.date_range(start=min_date, end=self.date_todey - datetime.timedelta(days=1),
                                            freq='D').strftime(format_date_str).tolist()
                print("Отчетна неделя(Период)")
                # список дат прошлой прошлого периода полный месяц
                last_month_min_day = min_date - pd.offsets.MonthBegin(1)
                # Определяем последний день прошлого месяца
                last_month_max_day = min_date - pd.offsets.Day(1)
                # Создаем список дат прошлого месяца
                self.list_last_month = pd.date_range(start=last_month_min_day, end= last_month_max_day, freq='D').strftime(
                    format_date_str).tolist()
                print("Отчетна неделя(Период)")
                # список дат прошлой прошлого периода сопоставимый месяц
                days_in_today_month = len(self.list_month)
                days_in_last_month = len(self.list_last_month)
                # Если количество дней в прошлом месяце больше, отфильтруем его, чтобы было равное количество дней
                if days_in_last_month > days_in_today_month:
                    self.list_last_month_MTD = self.list_last_month[:days_in_today_month]
                print("Отчетна неделя(Период)")
                # список дат прошлого года сопоставимый
                self.list_last_year = [datetime.datetime.strptime(date_str, '%Y-%m-%d').date().replace(year=2022).strftime('%Y-%m-%d') for
                                 date_str in self.list_month]
                print("Отчетна неделя(Период)")


                self.list_last_year_total = []
                today = self.date_todey
                last_year = today.year - 1
                month = today.month
                num_days = (datetime.date(last_year, month + 1, 1) - datetime.date(last_year, month, 1)).days
                dates= [datetime.date(last_year, month, day) for day in range(1, num_days + 1)]
                for date in dates:
                    date = date.strftime('%Y-%m-%d')
                    self.list_last_year_total.append(date)

                print("Отчетна неделя(Период)", self.list_month)
                print("Прошлая неделя(Период)", self.list_last_month)
                print("Прошлая неделя(Период опоставимый)", self.list_last_month_MTD)
                print("Прошлый год сопаставимый", self.list_last_year)
                print("Прошлый год полный", self.list_last_year_total)

            if num_pn() == 0:
                print("нужно взять прошлый месяц")

        tabl = kanal()
        # формирование списка столбцов
        All_colms = list(set(tabl.columns) - {'магазин', 'LFL', 'дата','канал'})
        Float.FLOAT().float_colms(name_data=tabl,name_col=All_colms)
        # добавлние ТУ
        self.ty_list, self.tabl = ty(name_df=tabl)
        # [Отчетная неделя]
        weeck_onchet()

    # обработка таблиц
    def tabls(self,prinak):
        global df_last_year_total
        df =pd.DataFrame()
        if prinak =="Отчетная неделя":
            df = self.tabl[self.tabl['дата'].isin(self.list_month)]
            print(df)
        if prinak == "Прошлая неделя":
            df = self.tabl[self.tabl['дата'].isin(self.list_last_month)]

        if prinak =="Прошлый год":
            df = self.tabl[self.tabl['дата'].isin( self.list_last_year)]
            df_last_year_total = self.tabl[self.tabl['дата'].isin(self.list_last_year_total)]

        sales = df['выручка'].sum().astype(int)
        chek = df['Количество чеков'].sum().astype(int)
        aver_chek = (sales / chek).astype(int)

        if prinak == "Прошлая неделя":
            aver_chek = (sales / chek).astype(int)
            sales = None
            chek = None

        # продажи
        sales_forecast = ((df['выручка'].sum() / df["Прошло дней"].max() *
                  df["осталось дней"].min()) + df['выручка'].sum()).astype(int)
        # чеки
        chek_forecast = ((df['Количество чеков'].sum() / df["Прошло дней"].max() *
                 df["осталось дней"].min()) + df['Количество чеков'].sum()).astype(int)
        # Средний чек
        aver_chek_forecast = (sales_forecast/chek_forecast).astype(int)
        # Счет количество а точек
        count_TT = df[df['выручка'] > 1000]['магазин'].nunique()
        # Списания
        spisania =((df["списания_оказатель"].sum() / df["Прошло дней"].max() *
                 df["осталось дней"].min()) + df["списания_оказатель"].sum()).astype(int)

        # Списания процент
        spisania_P = spisania / sales_forecast
        # вес продаж
        ves_prodaj = df["вес_продаж"].sum().astype(int)

        if prinak == "Прошлый год":
            sales_forecast = df_last_year_total['выручка'].sum().astype(int)
            chek_forecast = df_last_year_total['Количество чеков'].sum().astype(int)
            aver_chek_forecast = (sales / chek).astype(int)
            spisania = df_last_year_total["списания_оказатель"].sum().astype(int)
            spisania_P = spisania / sales_forecast
            ves_prodaj = df_last_year_total["вес_продаж"].sum().astype(int)

        # Список значений
        values = [[f"Выручка за {len(self.list_month)} дней", sales],
                  [f"Чеков за {len(self.list_month)} дней", chek],
                  [f"Средний чек за {len(self.list_month)} дней", aver_chek],
                  ["Проникновение лояльности", "не расчитан"],
                  [''],
                  [f"Выручка", sales_forecast],
                  [f"Чеков", chek_forecast],
                  [f"Средний чек", aver_chek_forecast],
                  ["Списания, %", spisania_P],
                  ["Продажи, кг", ves_prodaj],
                  ["Проникновение лояльности","не расчитан"],
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
                  ["Франшиза инвестиционная"],
                  [''],
                  ["Всего ТТ", count_TT],
                  ["Кол-во убыточных", np.nan],
                  ["", ""]]
        # Создание D из списка значений
        df_total = pd.DataFrame(values, columns=['Показатель'+ prinak, prinak])
        #print(df_total)

        for i in self.ty_list:
                mabager = df.loc[df["Менеджер"] == i]
                # продажи
                sales = ((mabager['выручка'].sum() /mabager["Прошло дней"].max() *
                          mabager["осталось дней"].min()) + mabager['выручка'].sum()).astype(int)
                # чеки
                chek = ((mabager['Количество чеков'].sum() / mabager["Прошло дней"].max() *
                         mabager["осталось дней"].min()) + mabager['Количество чеков'].sum()).astype(int)
                # Средний чек
                aver_chek = mabager['Средний чек'].mean().astype(int)
                # Счет количество а точек
                count_TT = mabager[mabager['выручка'] > 1000]['магазин'].nunique()
                # Списания
                spisania = mabager["списания_оказатель"].sum().astype(int)
                # Списания процент
                spisania_P = spisania / sales
                # вес продаж
                ves_prodaj = mabager["вес_продаж"].sum().astype(int)

                if prinak =="Прошлый год":
                    mabager_total = df_last_year_total.loc[df_last_year_total["Менеджер"] == i]
                    print(mabager_total)
                    sales =  mabager_total['выручка'].sum().astype(int)
                    chek =  mabager_total['Количество чеков'].sum().astype(int)
                    aver_chek = (sales / chek).astype(int)
                    spisania =  mabager_total["списания_оказатель"].sum().astype(int)
                    spisania_P = spisania / sales
                    ves_prodaj =  mabager_total["вес_продаж"].sum().astype(int)

                values = [["Менеджер: "+ i ],
                          ["Выручка", sales],
                          ["Чеков", chek],
                          ["Средний чек", aver_chek],
                          ["Списания, %", spisania_P],
                          ["Продажи, кг", ves_prodaj],
                          ["Проникновение лояльности"],
                          ["Прибыль (до вычета роялти)"],
                          ["Прибыль (до вычета роялти) на 1 ТТ:"],
                          ["Всего ТТ", count_TT],
                          ["", ""]]
                # Создание DataFrame из списка значений
                mabager = pd.DataFrame(values, columns=['Показатель'+ prinak, prinak])
                df_total = pd.concat([df_total, mabager], axis=0)
        return df_total

groups_instance = groups()
last_year_tabl = groups_instance.tabls(prinak="Прошлый год")
tabl_otchetnaya = groups_instance.tabls(prinak="Отчетная неделя")
last_tabl_otchtnaya = groups_instance.tabls(prinak="Прошлая неделя")

#itog = pd.concat([last_tabl_otchtnaya, tabl_otchetnaya], axis=1).reset_index(drop=True)
itog = pd.concat([last_tabl_otchtnaya, last_year_tabl,tabl_otchetnaya], axis=1).reset_index(drop=True)
itog = itog.drop(columns=["ПоказательОтчетная неделя"], axis=1)
itog = itog.drop(columns=["ПоказательПрошлый год"], axis=1)



itog  = itog.rename(columns={"ПоказательПрошлая неделя":""})
itog = itog[["","Прошлый год","Прошлая неделя","Отчетная неделя"]]

ln = ["Отчетная неделя","Прошлая неделя","Прошлый год"]
for i in ln:
    itog[i] = pd.to_numeric(itog[i], errors='coerce')

itog["Изменение год к году"] = itog["Отчетная неделя"] - itog["Прошлый год"]
itog["Изменение год к году %"] = itog["Изменение год к году"] / itog["Прошлый год"]

print(itog.info())

zagolovok_name = f'Данные сформированны: {ini.dat_seychas} - {ini.time_seychas}'

itog.to_excel(r"C:\Users\Lebedevvv\Desktop\FRS\Dashbord_new\csv.xlsx", index=False)


itog.replace([np.inf, -np.inf], np.nan, inplace=True)
itog.fillna('', inplace=True)

g.tbl_bot().svodniy_itog(name_tbl="Показатели сети для собрания", df=itog, sheet_name="Показатели сети")


