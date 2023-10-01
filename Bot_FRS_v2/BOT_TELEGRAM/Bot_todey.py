import sys
sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON\venv\Lib\site-packages")
sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON")

import holidays
from datetime import datetime, timedelta, time, date
import datetime
import time as t
import os

import numpy as np
import pandas as pd
from Bot_FRS_v2.INI import Float
from Bot_FRS_v2.GooGL_TBL import Google as g
from Bot_FRS_v2.INI import ini
from Bot_FRS_v2.INI import rename
from Bot_FRS_v2.BOT_TELEGRAM import BOT

pd.set_option("expand_frame_repr", False)
pd.set_option('display.max_colwidth', None)

TY_GROP =  ini.TY_GROP
TEST_BOT = ini.TEST_BOT
PUT = ini.PUT

class CustomRusHolidays(holidays.RU):
    def _populate(self, year,):
        super()._populate(year)
        # Добавляем в наш пользовательский набор праздников все официальные выходные дни.
        self[date(year, 5, 6)] = "День Воинской славы России"
        self[date(year, 5, 7)] = "День Воинской славы России"
        self[date(year, 5, 8)] = "День Победы"
        self[date(year, 5, 9)] = "День Победы"
        # Коректировка выходных дней
class bot_mesege:
    def __init__(self):
        self.days_in_month, self.days_last, self.days_ostatok = ini.prognoz()
        def tabl_bot_date():
            # определение рабочего дня или выходного
            def is_workday(date):
                ru_holidays = CustomRusHolidays()
                if date.weekday() >= 5:  # Если это суббота или воскресенье, то это выходной день.
                    return False
                elif date in ru_holidays:  # Если это праздничный день, то это выходной день.
                    return False
                else:
                    return True  # Иначе это рабочий день.

            def save_date(date_list, name):
                with open(PUT + "BOT\\Temp\\даты_файлов\\" + name + '.txt', 'w') as f:
                    f.write(str(date_list))

            # Чтение даты из файла
            with open(PUT + 'NEW\\дата обновления.txt', 'r') as f:
                date_str = f.readline().strip()
            format_date_str = '%d.%m.%Y'
            # тестовая дата скрыть ели боевой режим
            date_str = "2023-08-01 10:00:36.001115"
            # Дата обновления
            MAX_DATE = datetime.datetime.strptime(date_str[:10], '%Y-%m-%d').date()

            TODEY = [MAX_DATE.strftime(format_date_str)]
            LAST_DATE = MAX_DATE - datetime.timedelta(days=1)
            # print("Дата в файле\n", MAX_DATE)

            # тестовая
            test = 0
            if test == 1:
                MAX_DATE = datetime.datetime.strptime("2023-05-10", '%Y-%m-%d').date()
                LAST_DATE = MAX_DATE - datetime.timedelta(days=1)

            # region ФОРМИРОВАНИЕ СПИСКА ВЧЕРАШНЕЙ ДАТЫ
            priznzk = ""
            VCHERA = []
            if is_workday(MAX_DATE):
                if is_workday(LAST_DATE):
                    priznzk = 'середина недели'
                    VCHERA.append(LAST_DATE.strftime(format_date_str))
                else:
                    priznzk = "начало недели"
                    while not is_workday(LAST_DATE):
                        VCHERA.append(LAST_DATE.strftime(format_date_str))
                        LAST_DATE -= datetime.timedelta(days=1)
                    VCHERA.append(LAST_DATE.strftime(format_date_str))
            else:
                priznzk = "выходной день"
                VCHERA.append(LAST_DATE.strftime(format_date_str))
            # Преобразование дат в списке TODEY в объект datetime
            todey_date = datetime.datetime.strptime(TODEY[0], '%d.%m.%Y')
            # Фильтрация списка VCHERA
            fil_vchera = []
            for date_str in VCHERA:
                date = datetime.datetime.strptime(date_str, '%d.%m.%Y')
                if date.month == todey_date.month:
                    fil_vchera.append(date_str)

            VCHERA = fil_vchera

            # region ТЕКУШИЙ МЕСЯЦ
            TODEY_month_min_day = MAX_DATE.replace(day=1)
            # список дат
            TODEY_month = pd.date_range(start=TODEY_month_min_day, end=MAX_DATE - datetime.timedelta(days=1),
                                        freq='D').strftime(format_date_str).tolist()

            # если конец месяца
            MAX_DATE_TODEY_month_itog = datetime.datetime.strptime("2023-08-31", '%Y-%m-%d').date()
            TODEY_month_itog = pd.date_range(start=TODEY_month_min_day, end=MAX_DATE, freq='D').strftime(format_date_str).tolist()
            # print("Текущий месяц\n",TODEY_month)
            # endregion

            # region ПРОШЛЫЙ МЕСЯЦ
            LAST_month_min_day = TODEY_month_min_day - pd.offsets.MonthBegin(1)
            # Определяем последний день прошлого месяца
            LAST_month_max_day = TODEY_month_min_day - pd.offsets.Day(1)
            # Создаем список дат прошлого месяца
            LAST_month = pd.date_range(start=LAST_month_min_day, end=LAST_month_max_day, freq='D').strftime(
                format_date_str).tolist()
            # Определяем количество дней в каждом месяце
            days_in_today_month = len(TODEY_month)
            days_in_last_month = len(LAST_month)
            # Если количество дней в прошлом месяце больше, отфильтруем его, чтобы было равное количество дней
            if days_in_last_month > days_in_today_month:
                LAST_month = LAST_month[:days_in_today_month]
            # print("Прошлый месяц\n",LAST_month)

            # endregion
            # region ЕРЕМЕННАЯ НАЧАЛО МЕСЯЦА
            # Получаем текущую дату
            t_date = datetime.datetime.now()
            # Проверяем, является ли сегодня первым днем месяца
            if t_date.day == 1:
                # Если да, то устанавливаем значение переменной "Начало месяца"
                new_month = "Начало месяца"
            else:
                # Если нет, то устанавливаем значение переменной "нет"
                new_month = "нет"
            # endregion
            save_date(priznzk, "priznzk")
            save_date(TODEY, "TODEY")
            save_date(VCHERA, "VCHERA")
            save_date(TODEY_month, "TODEY_month")
            save_date(LAST_month, "LAST_month")
            save_date(new_month, "new_month")
            return TODEY, VCHERA, TODEY_month, LAST_month, priznzk, new_month

        def tabl_bot_new_month():
            # определение рабочего дня или выходного
            def is_workday(date):
                ru_holidays = CustomRusHolidays()
                if date.weekday() >= 5:  # Если это суббота или воскресенье, то это выходной день.
                    return False
                elif date in ru_holidays:  # Если это праздничный день, то это выходной день.
                    return False
                else:
                    return True  # Иначе это рабочий день.

            def save_date(date_list, name):
                with open(PUT + "BOT\\Temp\\даты_файлов\\" + name + '.txt', 'w') as f:
                    f.write(str(date_list))

            # Чтение даты из файла
            with open(PUT + 'NEW\\дата обновления.txt', 'r') as f:
                date_str = f.readline().strip()
            format_date_str = '%d.%m.%Y'
            # тестовая дата скрыть ели боевой режим
            date_str = "2023-08-01 10:00:36.001115"
            # Дата обновления
            MAX_DATE = datetime.datetime.strptime(date_str[:10], '%Y-%m-%d').date()

            TODEY = [MAX_DATE.strftime(format_date_str)]
            LAST_DATE = MAX_DATE - datetime.timedelta(days=1)
            # print("Дата в файле\n", MAX_DATE)

            # тестовая
            test = 0
            if test == 1:
                MAX_DATE = datetime.datetime.strptime("2023-05-10", '%Y-%m-%d').date()
                LAST_DATE = MAX_DATE - datetime.timedelta(days=1)

            # region ФОРМИРОВАНИЕ СПИСКА ВЧЕРАШНЕЙ ДАТЫ
            priznzk = ""
            VCHERA = []
            if is_workday(MAX_DATE):
                if is_workday(LAST_DATE):
                    priznzk = 'середина недели'
                    VCHERA.append(LAST_DATE.strftime(format_date_str))
                else:
                    priznzk = "начало недели"
                    while not is_workday(LAST_DATE):
                        VCHERA.append(LAST_DATE.strftime(format_date_str))
                        LAST_DATE -= datetime.timedelta(days=1)
                    VCHERA.append(LAST_DATE.strftime(format_date_str))
            else:
                priznzk = "выходной день"
                VCHERA.append(LAST_DATE.strftime(format_date_str))
            # Преобразование дат в списке TODEY в объект datetime
            todey_date = datetime.datetime.strptime(TODEY[0], '%d.%m.%Y')
            # Фильтрация списка VCHERA
            fil_vchera = []
            for date_str in VCHERA:
                date = datetime.datetime.strptime(date_str, '%d.%m.%Y')
                if date.month == todey_date.month:
                    fil_vchera.append(date_str)

            VCHERA = fil_vchera

            # region ТЕКУШИЙ МЕСЯЦ
            TODEY_month_min_day = MAX_DATE.replace(day=1)
            # список дат
            TODEY_month = pd.date_range(start=TODEY_month_min_day, end=MAX_DATE - datetime.timedelta(days=1),
                                        freq='D').strftime(format_date_str).tolist()

            # если конец месяца
            MAX_DATE_TODEY_month_itog = datetime.datetime.strptime("2023-08-31", '%Y-%m-%d').date()
            TODEY_month_itog = pd.date_range(start=TODEY_month_min_day, end=MAX_DATE, freq='D').strftime(format_date_str).tolist()
            # print("Текущий месяц\n",TODEY_month)
            # endregion

            # region ПРОШЛЫЙ МЕСЯЦ
            LAST_month_min_day = TODEY_month_min_day - pd.offsets.MonthBegin(1)
            # Определяем последний день прошлого месяца
            LAST_month_max_day = TODEY_month_min_day - pd.offsets.Day(1)
            # Создаем список дат прошлого месяца
            LAST_month = pd.date_range(start=LAST_month_min_day, end=LAST_month_max_day, freq='D').strftime(
                format_date_str).tolist()
            # Определяем количество дней в каждом месяце
            days_in_today_month = len(TODEY_month)
            days_in_last_month = len(LAST_month)
            # Если количество дней в прошлом месяце больше, отфильтруем его, чтобы было равное количество дней
            if days_in_last_month > days_in_today_month:
                LAST_month = LAST_month[:days_in_today_month]
            # print("Прошлый месяц\n",LAST_month)

            # endregion
            # region ЕРЕМЕННАЯ НАЧАЛО МЕСЯЦА
            # Получаем текущую дату
            t_date = datetime.datetime.now()
            # Проверяем, является ли сегодня первым днем месяца
            if t_date.day == 1:
                # Если да, то устанавливаем значение переменной "Начало месяца"
                new_month = "Начало месяца"
            else:
                # Если нет, то устанавливаем значение переменной "нет"
                new_month = "нет"
            # endregion
            save_date(priznzk, "priznzk")
            save_date(TODEY, "TODEY")
            save_date(VCHERA, "VCHERA")
            save_date(TODEY_month, "TODEY_month")
            save_date(LAST_month, "LAST_month")
            save_date(new_month, "new_month")
            return TODEY, VCHERA, TODEY_month, LAST_month, priznzk, new_month

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

        # Чтение даты из файла
        with open(PUT + 'NEW\\дата обновления.txt', 'r') as f:
            self.date_str = f.readline().strip()
        self.format_date_str = '%d.%m.%Y'

        # Формирование списка дат
        TODEY, VCHERA, TODEY_month, LAST_month, priznzk, new_month = tabl_bot_date()
        # Преобразование формата даты
        self.VCHERA_mes = VCHERA.copy()
        self.TODEY = [datetime.datetime.strptime(date, '%d.%m.%Y').strftime('%Y-%m-%d') for date in TODEY]
        self.VCHERA = [datetime.datetime.strptime(date, '%d.%m.%Y').strftime('%Y-%m-%d') for date in VCHERA]
        self.TODEY_month = [datetime.datetime.strptime(date, '%d.%m.%Y').strftime('%Y-%m-%d') for date in TODEY_month]
        self.LAST_month = [datetime.datetime.strptime(date, '%d.%m.%Y').strftime('%Y-%m-%d') for date in LAST_month]
        self.LAST_year = []
        for i  in TODEY_month:
            i = i.replace('2023', '2022')
            self.LAST_year.append(i)

        self.LAST_year = [datetime.datetime.strptime(date, '%d.%m.%Y').strftime('%Y-%m-%d') for date in self.LAST_year]
        print("*Список дат прошлого года: ", self.TODEY_month)
        print("*Список дат прошлого года: ", self.LAST_year)
        # список для фолрмирование даты в сообщении.
        self.VCHERA_date_info = VCHERA
        # загрзка таблиц, формирование списка ТУ
        self.tabl = pd.read_csv(PUT + "♀Вычисляемые_таблицы\\Нарастающие итоги.csv", sep="\t", encoding="utf-8",
                           parse_dates=['дата'], date_format='%Y-%m-%d',
                           dtype={'магазин': str, 'LFL': str},low_memory=False)
        # Получение списка всех столбцов, исключая ['магазин', 'LFL', 'дата']
        All_colms = list(set(self.tabl.columns) - {'магазин', 'LFL', 'дата'})
        Float.FLOAT().float_colms(name_data=self.tabl,name_col=All_colms)
        self.ty_list, self.tabl = ty(name_df=self.tabl)

        folder = PUT + "♀Чеки\\Чеки текущий день\\"
        # Получение списка всех файлов в папках и подпапках
        all_files = []
        df_today = pd.DataFrame()
        for root, dirs, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root, file)
                all_files.append(file_path)
        for file_path in all_files:
            df_today = pd.read_csv(file_path, sep=";", encoding="utf-8")
            df_today = df_today.drop(columns=["ID", "количество товаров в чеке",
                                              "количество уникальных товаров в чеке", "дата",
                                              "Количество чеков_возврат"])
            df_today = df_today.rename(columns={'!МАГАЗИН!':'магазин'})
        All_colms = list(set(df_today.columns) - {'магазин','Менеджер'})
        Float.FLOAT().float_colms(name_data=df_today, name_col=All_colms)
        ty_list, self.df_today = ty(name_df=df_today)
    def ff(self):
        print("Сегодняшняя дата: ", self.TODEY)
        print("Вчерашняя дата: ", self.VCHERA)
        print("Даты текущего месяца: ", self.TODEY_month)
        print("Даты прошлого месяца: ", self.LAST_month)
        print("Список дат прошлого года: ", self.LAST_year)
        print("Список территориалов: ", self.ty_list)
    # формирование сообщений вчерашнего дня
    def vchera(self):
        if ini.time_seychas < ini.time_bot_vrem:
            # форматирование числа
            def fn(i):
                return '{:,.0f}'.format(i).replace(',', ' ')
            # фрматирование процента
            def fp(i, ndigits):
                return "{:.{ndigits}%}".format(i, ndigits=ndigits)
            # ормирование соощение даты
            def __date():
                # VCHERA = ['02.05.2023', '03.05.2023']
                VCHERA_date = ""
                self.kol_day = len(self.VCHERA)
                self.min_date = ""
                self.max_date = ""
                self.date = ""
                if self.kol_day == 1:
                    print(self.VCHERA)
                    self.date = min(self.VCHERA_date_info)
                    VCHERA_date = f'🕙 Результаты вчерашнего дня:\n'
                    VCHERA_date += f' •\u200E {self.date}\n'
                else:
                    print(self.VCHERA_date_info)
                    self.min_date = min(self.VCHERA_date_info)
                    self.max_date = max(self.VCHERA_date_info)

                    VCHERA_date = f"🕙 Результаты за выходные:\n"
                    VCHERA_date += f" •{self.min_date} - {self.max_date}\n"
                return VCHERA_date
            # результаты за вчера
            VCHERA_tabl = self.tabl[self.tabl['дата'].isin(self.VCHERA)]
            VCHERA_tabl = VCHERA_tabl.groupby(["магазин", "Менеджер"],
                                                        as_index=False).agg(
                                    {"выручка": "sum", "Количество чеков": "sum", "дневной_план_выручка": "sum",
                                     "дневной_план_кол_чеков": "sum",
                                     "списания_оказатель":"sum","списания_хозы":"sum"}) \
                                    .reset_index(drop=True)
            # Результаты за месяц
            TODEY_month_tabl = self.tabl[self.tabl['дата'].isin(self.TODEY_month)]
            TODEY_month_tabl = TODEY_month_tabl.groupby(["магазин", "Менеджер"],as_index=False).agg(
                                    {"выручка":"sum","Количество чеков":"sum","план_выручка": "mean",
                                     "план_кол_чеков": "mean","план_cредний_чек":"mean",
                                     "списания_оказатель":"sum","списания_хозы":"sum"}) \
                                    .reset_index(drop=True)

            # Результаты за прошлый год
            Last_year = self.tabl[self.tabl['дата'].isin(self.LAST_year)]

            Last_year.to_excel(r'C:\Users\lebedevvv\Desktop\FRS\Dashbord_new\BOT\Т.xlsx', index=False)

            Last_year = Last_year.groupby(["магазин"], as_index=False).agg(
                {"выручка": "sum", "Количество чеков": "sum",
                 "списания_оказатель": "sum", "списания_хозы": "sum"}) \
                .reset_index(drop=True)
            Last_year = Last_year.rename(
                columns={"выручка": "выручка прошлый год", "Количество чеков": "Количество чеков, прошлый год",
                         "списания_оказатель": "списания_оказатель прошлый год",
                         "списания_хозы": "списания_хозы прошлый год"})

            # Результаты за прошлый месяц
            Last_nonth = self.tabl[self.tabl['дата'].isin(self.LAST_month)]
            Last_nonth = Last_nonth.groupby(["магазин"], as_index=False).agg(
                {"выручка": "sum", "Количество чеков": "sum",
                 "списания_оказатель": "sum", "списания_хозы": "sum"}) \
                .reset_index(drop=True)
            Last_nonth = Last_nonth.rename(columns={"выручка":"выручка прошлый месяц","Количество чеков": "Количество чеков месяц",
                                                    "списания_оказатель":"списания_оказатель прошлый месяц", "списания_хозы":"списания_хозы прошлый месяц"})

            TODEY_month_tabl["-осталось дней"] = self.days_ostatok
            TODEY_month_tabl["-прошло дней"] = self.days_last
            TODEY_month_tabl["Прогноз выручка"] =\
                ((TODEY_month_tabl["выручка"] / TODEY_month_tabl["-прошло дней"] *
                  TODEY_month_tabl["-осталось дней"]) + TODEY_month_tabl["выручка"]).round(2)

            TODEY_month_tabl["Прогноз Количество чеков"] = \
                ((TODEY_month_tabl["Количество чеков"] / TODEY_month_tabl["-прошло дней"] *
                  TODEY_month_tabl["-осталось дней"]) + TODEY_month_tabl["Количество чеков"]).round(2)
            TODEY_month_tabl = TODEY_month_tabl.drop(columns={"-осталось дней", "-прошло дней"})
            seve_totalitog = pd.DataFrame()
            for i in self.ty_list:
                # выруча за месяц
                manager_data_total = TODEY_month_tabl.loc[TODEY_month_tabl["Менеджер"] == i]

                manager_data_total = manager_data_total.merge(Last_nonth,
                                                         on=["магазин"], how="left").reset_index(drop=True)
                manager_data_total = manager_data_total.merge(Last_year,
                                                              on=["магазин"], how="left").reset_index(drop=True)

                sales_total = manager_data_total["выручка"].sum()
                sales_total_plan = manager_data_total["план_выручка"].sum()
                sales_total_itog = sales_total / sales_total_plan
                sales_total_prognoz = manager_data_total["Прогноз выручка"].sum()
                sales_total_prognoz_itog = sales_total_prognoz / sales_total_plan

                # чеки  за месяц
                check_total = manager_data_total["Количество чеков"].sum()
                check_total_plan = manager_data_total["план_кол_чеков"].sum()
                check_total_itog = check_total/ check_total_plan
                check_total_prognoz = manager_data_total["Прогноз Количество чеков"].sum()
                check_total_prognoz_itog = check_total_prognoz / check_total_plan
                # Средний чек  за месяц
                aver_chek_total = sales_total/ check_total

                aver_chek_total_plan = sales_total_plan / check_total_plan
                    #manager_data_total["план_cредний_чек"].mean()
                aver_chek_total_itog = aver_chek_total/aver_chek_total_plan
                aver_total_prognoz = sales_total_prognoz / check_total_prognoz

                aver_total_prognoz_itog = aver_total_prognoz / aver_chek_total_plan

                # Списания  за месяц
                spis_total = manager_data_total["списания_оказатель"].sum()
                hoz_total = manager_data_total["списания_хозы"].sum()
                spis_day_total_itog = spis_total / sales_total
                hoz_day_total_itog = hoz_total / sales_total

                # дневные показатели Выручка
                manager_data_day = VCHERA_tabl.loc[VCHERA_tabl["Менеджер"] == i]
                sales_day = manager_data_day["выручка"].sum()
                plan_sales_day = manager_data_day["дневной_план_выручка"].sum()
                plan_sales_itog = sales_day / plan_sales_day

                # дневные показатели Чеки
                check_day = manager_data_day["Количество чеков"].sum()
                plan_check_day = manager_data_day["дневной_план_кол_чеков"].sum()
                plan_check_itog = check_day / plan_check_day

                # план дневного среднего чека
                aver_chek_day = sales_day / check_day
                aver_chek_plan_day = plan_sales_day / plan_check_day
                aver_chek_itog_day = aver_chek_day / aver_chek_plan_day
                # дневные показатели средний чек
                spis_day = manager_data_day["списания_оказатель"].sum()
                hoz_day = manager_data_day["списания_хозы"].sum()
                spis_day_itog = spis_day / sales_day
                hoz_day_itog = hoz_day / sales_day

                # формирование сообщений выручка
                def __sales():
                    s = 0
                    if sales_total<sales_total_plan:
                        s = sales_total_plan - sales_total

                        print(f'{i} - "До плана дневных продаж" {fn(s)}')
                        mes_sales = \
                            f'<b> 👨‍💼 {i}:</b>\n\n' \
                            f' {__date()}\n' \
                            f'<b>Выручка:\n</b>' \
                            f'• План(дневной): {fn(i=plan_sales_day)}\n' \
                            f'• Факт: {fn(i=sales_day)} ({fp(i=plan_sales_itog, ndigits=1)})\n'

                    else:
                        mes_sales = \
                            f'<b> 👨‍💼 {i}:</b>\n\n' \
                            f' {__date()}\n' \
                            f'<b>Выручка:\n</b>' \
                            f'• План(дневной): "Выполнен"\n'


                    mes_sales_total =\
                        f'<b>\n📆 Результаты текущего месяца: \n</b>' \
                        f'<b>Выручка:\n</b>' \
                        f'• План(месяц): {fn(i=sales_total_plan)}\n' \
                        f'• Факт: {fn(i=sales_total)} ({fp(i=sales_total_itog, ndigits=1)})\n'\
                        f'• Прогноз: {fn(i=sales_total_prognoz)} ({fp(i=sales_total_prognoz_itog, ndigits=1)})\n'

                    return  mes_sales, mes_sales_total

                # формирование сообщений чеки
                def __check():
                    s = 0
                    if check_total<check_total_plan:
                        s = check_total_plan - check_total
                        print(f'{i} - "До плана чеки" {fn(s)}')
                        mes_check = f'<b>Кол.чеков:\n</b>' \
                                         f'• План(дневной): {fn(i=plan_check_day)}\n' \
                                         f'• Факт: {fn(i=check_day)} ({fp(i=plan_check_itog, ndigits=1)})\n'
                    else:
                        mes_check = f'<b>Кол.чеков:\n</b>' \
                                         f'• План(дневной): "Выполнен"\n'\

                    mes_check_total = \
                        f'<b>Кол.чеков:\n</b>' \
                        f'• План(месяц): {fn(i=check_total_plan)}\n' \
                        f'• Факт: {fn(i=check_total)} ({fp(i=check_total_itog, ndigits=1)})\n'\
                        f'• Прогноз: {fn(i=check_total_prognoz)} ({fp(i=check_total_prognoz_itog, ndigits=1)})\n'

                    return  mes_check, mes_check_total

                # формирование сообщений средний чек
                def aver_chek():
                    mes_aver_chek = f'<b>Средний чек:\n</b>' \
                                f'• План(дневной): {fn(i=aver_chek_plan_day)}\n' \
                                f'• Факт: {fn(i=aver_chek_day)} ({fp(i=aver_chek_itog_day, ndigits=1)})\n'
                    mes_aver_chek_total = \
                        f'<b>Средний чек:\n</b>' \
                        f'• План(месяц): {fn(i=aver_chek_total_plan)}\n' \
                        f'• Факт/Прогноз: {fn(i=aver_total_prognoz)} ({fp(i=aver_total_prognoz_itog, ndigits=1)})\n'

                    return mes_aver_chek, mes_aver_chek_total

                # формирование сообщений списания
                def spisania():
                    signal_spisania = ""
                    if spis_day_total_itog>0.025:
                        signal_spisania = "⚠️"
                    mes_spisania_day =\
                        f'<b>Списания:\n</b>' \
                        f'• Показатель: {fn(i=spis_day)} ({fp(i=spis_day_itog, ndigits=1)})\n'\
                        f'• Хозы: {fn(i=hoz_day)} ({fp(i=hoz_day_itog, ndigits=1)})\n'
                    mes_spisania_total =\
                        f'<b>Списания:\n</b>' \
                        f'• Показатель: {fn(i=spis_total)} ({fp(i=spis_day_total_itog, ndigits=1)}){signal_spisania}\n'\
                        f'• Хозы: {fn(i=hoz_total)} ({fp(i=hoz_day_total_itog, ndigits=1)})\n'

                    return mes_spisania_day, mes_spisania_total

                mes_sales, mes_sales_total = __sales()
                mes_check, mes_check_total = __check()
                mes_aver_chek, mes_aver_chek_total = aver_chek()
                mes_spisania_day, mes_spisania_total = spisania()
                self.i = i
                g = google_tabl(self)
                # отправка на создание гугл таблицы за день
                g.last_day_googl_tbl(df=manager_data_day)
                t.sleep(3)

                # отправка на создание гугл таблицы за месяц
                url_month = g.vchera_googl_tbl(df=manager_data_total)
                seve_totalitog = pd.concat([seve_totalitog ,manager_data_total],axis=0)
                url = f'<b>\n 📎 <a href="{url_month}">Ссылка Google таблицу</a></b>'
                print(ini.TY_id)
                #BOT().__del_lost(priznak_grup="TY")
                BOT.BOT().bot_mes_html_TY(mes=mes_sales + mes_check+ mes_aver_chek + mes_spisania_day +
                    mes_sales_total+mes_check_total + mes_aver_chek_total + mes_spisania_total + url, silka=0)
                t.sleep(10)

            seve_totalitog.to_csv(r"C:\Users\lebedevvv\Desktop\FRS\Dashbord_new\BOT\Расчет_гуглтаблиц.csv",sep="\t",encoding="utf-8",index=False)
    # формирование таблиц дневных
    def to_day(self):
        for i in self.ty_list:
            manager_data = self.df_today.loc[self.df_today["Менеджер"] == i]
            sales_day = manager_data["выручка"].sum()
            print( i , " ", sales_day)


class google_tabl():
    def __init__(self,self_bot):
        self.bot = self_bot
    # формирование таблиц вчерашнего дня
    def vchera_googl_tbl(self, df):




        df = df.rename(columns={"магазин":'Магазин',
                            "выручка":'Выручка Факт',
                            "план_выручка": "Выручка План",
                            "Количество чеков": "Кол.чеков Факт",
                            "план_кол_чеков": "Кол.чеков План",
                            "Прогноз Количество чеков":"Кол.чеков Прогноз",
                            "списания_оказатель":"Списание (Показатель)",
                            "списания_хозы":"Списание (Хозы)"})
        # gпрошле периоды
        df = df.rename(columns={"выручка прошлый месяц": "Выручка прошлый месяц",
                                "Количество чеков месяц": "Кол.чеков прошлый месяц",
                                "списания_оказатель прошлый месяц": "Списание (Показатель) прошлый месяц",
                                "списания_хозы прошлый месяц": "Списание (Хозы) прошлый месяц",
                                "выручка прошлый год": "Выручка прошлый год",
                                "Количество чеков, прошлый год": "Кол.чеков прошлый год",
                                "списания_оказатель прошлый год": "Списание (Показатель) прошлый год",
                                "списания_хозы прошлый год": "Списание (Хозы) прошлый год"})

        df["Выручка изменение к прошлому месяцу %"] = df["Выручка Факт"] / df["Выручка прошлый месяц"]-1
        df["Выручка изменение к прошлому месяцу"] = df["Выручка Факт"] - df["Выручка прошлый месяц"]

        df["Выручка изменение к прошлому году %"] = df["Выручка Факт"] / df["Выручка прошлый год"]-1
        df["Выручка изменение к прошлому году"] = df["Выручка Факт"] - df["Выручка прошлый год"]

        df["Кол.чеков изменение к прошлому месяцу %"] = df["Кол.чеков Факт"] / df["Кол.чеков прошлый месяц"]-1
        df["Кол.чеков изменение к прошлому месяцу"] = df["Кол.чеков Факт"] - df["Кол.чеков прошлый месяц"]

        df["Кол.чеков изменение к прошлому году %"] = df["Кол.чеков Факт"] / df["Кол.чеков прошлый год"]-1
        df["Кол.чеков изменение к прошлому году"] = df["Кол.чеков Факт"] - df["Кол.чеков прошлый год"]


        df["Прогноз выручка %"] = df["Прогноз выручка"] / df["Выручка План"]
        df["Кол.чеков Прогноз %"] = df["Кол.чеков Прогноз"] / df["Кол.чеков План"]
        df["Средний чек Факт"] = df["Выручка Факт"] / df["Кол.чеков Факт"]
        df["Средний чек План"] = df["Выручка План"] / df["Кол.чеков План"]
        df["Средний чек Прогноз"] = df["Прогноз выручка"] / df["Кол.чеков Прогноз"]
        df["Средний чек Прогноз %"] = df["Средний чек Прогноз"] / df["Средний чек План"]
        df["Списание (Показатель) %"] = df["Списание (Показатель)"] / df["Выручка Факт"]
        df["Списание (Хозы) %"] = df["Списание (Хозы)"] / df["Выручка Факт"]

        df["Списание (Показатель) прошлый год %"] = df["Списание (Показатель) прошлый год"] / df["Выручка прошлый год"]
        df["Списание (Показатель) прошлый месяц %"] = df["Списание (Показатель) прошлый месяц"] / df["Выручка прошлый месяц"]
        df["Списание (Показатель) изменение к прошлому месяцу %"] =  df["Списание (Показатель) %"] - df["Списание (Показатель) прошлый месяц %"]
        df["Списание (Показатель) изменение к прошлому году %"] = df["Списание (Показатель) %"] - df["Списание (Показатель) прошлый год %"]

        df["Списание (Хозы) прошлый год %"] = df["Списание (Хозы) прошлый год"] / df["Выручка прошлый год"]
        df["Списание (Хозы) прошлый месяц %"] = df[ "Списание (Хозы) прошлый месяц"] / df["Выручка прошлый месяц"]
        df["Списание (Хозы) изменение к прошлому месяцу %"] = df["Списание (Хозы) %"] - df["Списание (Хозы) прошлый месяц %"]
        df["Списание (Хозы) изменение к прошлому году %"] = df["Списание (Хозы) %"] - df["Списание (Хозы) прошлый год %"]

        df["Средний чек прошлый месяц"] = df["Выручка прошлый месяц"] / df["Кол.чеков прошлый месяц"]
        df["Средний чек прошлый год"] = df["Выручка прошлый год"] / df["Кол.чеков прошлый год"]

        df["Средний чек изменение к прошлому месяцу %"] = df["Средний чек Факт"] / df["Средний чек прошлый месяц"]-1
        df["Средний чек изменение к прошлому месяцу"] = df["Средний чек Факт"] - df["Средний чек прошлый месяц"]

        df["Средний чек изменение к прошлому году %"] = df["Средний чек Факт"] / df["Средний чек прошлый год"]-1
        df["Средний чек изменение к прошлому году"] = df["Средний чек Факт"] - df["Средний чек прошлый год"]

        df = df[['Магазин',
                 'Выручка Факт',
                 "Выручка План",
                 "Прогноз выручка",
                 "Прогноз выручка %",
                 "Выручка прошлый месяц",
                 "Выручка изменение к прошлому месяцу",
                 "Выручка изменение к прошлому месяцу %",
                 "Выручка прошлый год",
                 "Выручка изменение к прошлому году",
                 "Выручка изменение к прошлому году %",
                 "Кол.чеков Факт",
                 "Кол.чеков План",
                 "Кол.чеков Прогноз",
                 "Кол.чеков Прогноз %",
                 "Кол.чеков прошлый месяц",
                 "Кол.чеков изменение к прошлому месяцу",
                 "Кол.чеков изменение к прошлому месяцу %",
                 "Кол.чеков прошлый год",
                 "Кол.чеков изменение к прошлому году",
                 "Кол.чеков изменение к прошлому году %",
                 "Средний чек Факт",
                 "Средний чек План",
                 "Средний чек Прогноз %",
                 "Средний чек прошлый месяц",
                 "Средний чек изменение к прошлому месяцу",
                 "Средний чек изменение к прошлому месяцу %",
                 "Средний чек прошлый год",
                 "Средний чек изменение к прошлому году",
                 "Средний чек изменение к прошлому году %",
                 "Списание (Показатель)",
                 "Списание (Показатель) %",
                 "Списание (Показатель) прошлый месяц",
                 "Списание (Показатель) прошлый месяц %",
                 "Списание (Показатель) изменение к прошлому месяцу %",
                 "Списание (Показатель) прошлый год",
                 "Списание (Показатель) прошлый год %",
                 "Списание (Показатель) изменение к прошлому году %",
                 "Списание (Хозы)",
                 "Списание (Хозы) %",
                 "Списание (Хозы) прошлый месяц",
                 "Списание (Хозы) прошлый месяц %",
                 "Списание (Хозы) изменение к прошлому месяцу %",
                 "Списание (Хозы) прошлый год",
                 "Списание (Хозы) прошлый год %",
                 "Списание (Хозы) изменение к прошлому году %"
                 ]]
        total_row = pd.DataFrame({
            'Магазин': ['Итог'],
            'Выручка Факт': [df['Выручка Факт'].sum()],
            'Выручка План': [df['Выручка План'].sum()],
            'Прогноз выручка': [df['Прогноз выручка'].sum()],
            'Прогноз выручка %': [df['Прогноз выручка'].sum() / df['Выручка План'].sum()],
            "Выручка прошлый месяц": [df['Выручка прошлый месяц'].sum()],
            "Выручка изменение к прошлому месяцу": [df["Выручка изменение к прошлому месяцу"].sum()],
            "Выручка изменение к прошлому месяцу %": [df["Выручка Факт"].sum() / df["Выручка прошлый месяц"].sum()-1],
            "Выручка прошлый год": [df['Выручка прошлый год'].sum()],
            "Выручка изменение к прошлому году": [df['Выручка изменение к прошлому году'].sum()],
            "Выручка изменение к прошлому году %" :  [df["Выручка Факт"].sum() / df["Выручка прошлый год"].sum()-1],
            'Кол.чеков Факт': [df['Кол.чеков Факт'].sum()],
            'Кол.чеков План': [df['Кол.чеков План'].sum()],
            'Кол.чеков Прогноз': [df['Кол.чеков Прогноз'].sum()],
            'Кол.чеков Прогноз %': [df["Кол.чеков Прогноз"].sum() / df["Кол.чеков План"].sum()],
            "Кол.чеков прошлый месяц":  [df['Кол.чеков прошлый месяц'].sum()],
            "Кол.чеков изменение к прошлому месяцу": [df['Кол.чеков изменение к прошлому месяцу'].sum()],
            "Кол.чеков изменение к прошлому месяцу %": [df["Кол.чеков Факт"].sum() / df["Кол.чеков прошлый месяц"].sum()-1],
            "Кол.чеков прошлый год":  [df['Кол.чеков прошлый год'].sum()],
            "Кол.чеков изменение к прошлому году":  [df['Кол.чеков изменение к прошлому году'].sum()],
            "Кол.чеков изменение к прошлому году %": [df["Кол.чеков Факт"].sum() / df["Кол.чеков прошлый год"].sum()-1],

            'Средний чек Факт': [df['Средний чек Факт'].mean()],
            'Средний чек План': [df['Средний чек План'].mean()],
            "Средний чек Прогноз %": [df["Средний чек Факт"].sum() / df["Средний чек План"].sum()],
            "Средний чек прошлый месяц":[df['Средний чек прошлый месяц'].mean()],
            "Средний чек изменение к прошлому месяцу":[df['Средний чек изменение к прошлому месяцу'].mean()],
            "Средний чек изменение к прошлому месяцу %": [df["Средний чек Факт"].sum() / df["Средний чек прошлый месяц"].sum()-1],
            "Средний чек прошлый год": [df['Средний чек прошлый год'].mean()],
            "Средний чек изменение к прошлому году": [df['Средний чек изменение к прошлому году'].mean()],
            "Средний чек изменение к прошлому году %":[df["Средний чек Факт"].sum() / df["Средний чек прошлый год"].sum()-1],
            "Списание (Показатель)" : [df['Списание (Показатель)'].sum()],
            "Списание (Показатель) %": [df["Списание (Показатель)"].sum() / df["Выручка Факт"].sum()],
            "Списание (Показатель) прошлый месяц": [df['Списание (Показатель) прошлый месяц'].sum()],
            "Списание (Показатель) прошлый месяц %": [df["Списание (Показатель) прошлый месяц"].sum() / df["Выручка прошлый месяц"].sum()],
            "Списание (Показатель) изменение к прошлому месяцу %": [df["Списание (Показатель) %"].sum() - df["Списание (Показатель) прошлый месяц %"].sum()],
            "Списание (Показатель) прошлый год":[df['Списание (Показатель) прошлый год'].sum()],
            "Списание (Показатель) прошлый год %": [df["Списание (Показатель) прошлый год"].sum() / df["Выручка прошлый год"].sum()],
            "Списание (Показатель) изменение к прошлому году %":[df["Списание (Показатель) %"].sum() - df["Списание (Показатель) прошлый год %"].sum()],
            "Списание (Хозы)": [df['Списание (Хозы)'].sum()],
            "Списание (Хозы) %":[df["Списание (Хозы)"].sum() / df["Выручка Факт"].sum()],
            "Списание (Хозы) прошлый месяц": [df['Списание (Хозы) прошлый месяц'].sum()],
            "Списание (Хозы) прошлый месяц %":[df[ "Списание (Хозы) прошлый месяц"].sum() / df["Выручка прошлый месяц"].sum()],
            "Списание (Хозы) изменение к прошлому месяцу %":[df["Списание (Хозы) %"].mean() - df["Списание (Хозы) прошлый месяц %"].mean()],
            "Списание (Хозы) прошлый год": [df["Списание (Хозы) прошлый год"].sum()],
            "Списание (Хозы) прошлый год %":[df["Списание (Хозы) прошлый год"].sum() / df["Выручка прошлый год"].sum()],
            "Списание (Хозы) изменение к прошлому году %":[df["Списание (Хозы) %"].mean() - df["Списание (Хозы) прошлый год %"].mean()],
            })
        df = pd.concat([df, total_row], ignore_index=True)
        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        df.fillna('', inplace=True)
        zagolovok_name = f'Результаты текущего месяца: {ini.month_and_god()}'
        url = g.tbl_bot().sheet(name_tbl=self.bot.i,df=df,sheet_name="Результаты текущего месяца",
                                one_stroka=zagolovok_name)
        return url
    # формирование таблиц дневных
    def last_day_googl_tbl(self,df):
        df = df.drop(columns=["Менеджер"])
        df = df.rename(columns={"магазин": 'Магазин',
                                "выручка": 'Выручка Факт', "дневной_план_выручка": "Выручка План",
                                "Количество чеков": "Кол.чеков Факт", "дневной_план_кол_чеков": "Кол.чеков План",
                                "списания_оказатель": "Списание (Показатель)", "списания_хозы": "Списание (Хозы)"})

        df["Выполнение Выручка %"] = df['Выручка Факт'] / df["Выручка План"]
        df["Выполнение Кол.чеков %"] = df["Кол.чеков Факт"] / df["Кол.чеков План"]
        df["Средний чек Факт"] = df["Выручка Факт"] / df["Кол.чеков Факт"]
        df["Средний чек План"] = df["Выручка План"] / df["Кол.чеков План"]
        df["Выполнение Средний чек %"] = df["Средний чек Факт"] / df["Средний чек План"]
        df["Списание (Показатель) %"] = df["Списание (Показатель)"] / df["Выручка Факт"]
        df["Списание (Хозы) %"] = df["Списание (Хозы)"] / df["Выручка Факт"]

        df = df[['Магазин', 'Выручка Факт', "Выручка План", "Выполнение Выручка %",
                 "Кол.чеков Факт", "Кол.чеков План", "Выполнение Кол.чеков %",
                 "Средний чек Факт", "Средний чек План","Выполнение Средний чек %",
                 "Списание (Показатель)", "Списание (Показатель) %", "Списание (Хозы)", "Списание (Хозы) %"]]

        total_row = pd.DataFrame({
            'Магазин': ['Итог'],
            'Выручка Факт': [df['Выручка Факт'].sum()],
            'Выручка План': [df['Выручка План'].sum()],
            "Выполнение Выручка %": [df['Выручка Факт'].sum() / df['Выручка План'].sum()],
            'Кол.чеков Факт': [df['Кол.чеков Факт'].sum()],
            'Кол.чеков План': [df['Кол.чеков План'].sum()],
            "Выполнение Кол.чеков %": [df['Кол.чеков Факт'].sum() / df['Кол.чеков План'].sum()],
            'Средний чек Факт': [df['Средний чек Факт'].mean()],
            'Средний чек План': [df['Средний чек План'].mean()],
            "Выполнение Средний чек %": [df['Средний чек Факт'].sum() / df["Средний чек План"].sum()],
            'Списание (Показатель)': [df['Списание (Показатель)'].sum()],
            'Списание (Показатель) %': [df['Списание (Показатель)'].sum() / df['Выручка Факт'].sum()],
            'Списание (Хозы)': [df['Списание (Хозы)'].sum()],
            'Списание (Хозы) %': [df['Списание (Хозы)'].sum() / df['Выручка Факт'].sum()]
        })

        df = pd.concat([df, total_row], ignore_index=True)
        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        df.fillna('', inplace=True)
        zagolovok_name = ""
        if self.bot.kol_day == 1:
            #date = datetime.datetime.strptime(self.bot.date, "%Y-%m-%d").strftime("%d.%m.%Y")
            zagolovok_name = f'Результаты прошедшего дня: {self.bot.date}'
        else:
            date1 = self.bot.min_date
            date2 = self.bot.max_date
            zagolovok_name = f'Результаты прошедших выходных дней: {date1} - {date2}'
        g.tbl_bot().Last_day(name_tbl=self.bot.i, df=df, sheet_name="Результаты прошлого дня", one_stroka=zagolovok_name)

        return
#BOT_rashet().rashet()
if ini.time_seychas<ini.time_bot_vrem:
    bot_mesege = bot_mesege()
    bot_mesege.ff()
    bot_mesege.vchera()

#bot_mesege.last_day()
