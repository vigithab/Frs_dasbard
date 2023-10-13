import shutil

import datetime
from datetime import date
import os
from Bot_FRS_v2.GooGL_TBL import Google as g
import numpy as np
import pandas as pd
from Bot_FRS_v2.INI import ini, rename

pd.set_option("expand_frame_repr", False)
pd.set_option('display.max_colwidth', None)


class reting_franshiza():

    def __init__(self):
        self.df = pd.read_csv(ini.PUT + "♀Вычисляемые_таблицы\\Нарастающие итоги.csv", sep="\t", encoding="utf-8",
                              decimal=".", low_memory=False)
        # планов продаж
        plan = pd.read_excel(ini.PUT + "♀Планы\\Планы ДЛЯ ДАШБОРДА.xlsx")
        plan['дата'] = pd.to_datetime(plan['дата'], format='%d.%m.%Y')
        plan.loc[plan["Показатель"] == "Выручка", "план_выручка"] = plan["ПЛАН"].round(0)
        plan.loc[plan["Показатель"] == "Средний чек", "план_cредний_чек"] = plan["ПЛАН"].round(0)
        plan.loc[plan["Показатель"] == "Кол чеков", "план_кол_чеков"] = plan["ПЛАН"].round(0)
        plan = plan.drop(["ПЛАН", "Показатель","Проверка"], axis=1)
        plan = plan.groupby(["магазин", "дата"]).sum().reset_index()
        self.plan = plan

    def run_2(self):
        df = self.df
        plan = self.plan

        def audit():
            start = r'P:\Фирменная розница\ФРС\Аналитический отдел ФРС\аудиты_Петров_выгрузка.xlsx'
            #start = r'C:\Рабочие документы\Python\Франшиза\аудиты_Петров_выгрузка.xlsx'
            #end = r'C:\Рабочие документы\Python\Франшиза\Аудиты'
            end = r'C:\Users\lebedevvv\Desktop\FRS\Dashbord_new\Аудиты'

            shutil.copy2(start,end)

            # Путь к директории с файлами
            p_palic = r"C:\Users\lebedevvv\Desktop\FRS\Dashbord_new\Аудиты"
            # Создаем пустой список для хранения имен файлов, которые содержат "Отчёт"
            report_files = []
            # Проходим через все файлы в указанной директории
            for filename in os.listdir(p_palic):

                if "аудиты" in filename and "~$" not in filename:
                    report_files.append(filename)

            df = pd.DataFrame()
            for filename in report_files:
                full_path = os.path.join(p_palic, filename)

                df = pd.read_excel(full_path, sheet_name="Таблица3")
                print(df)
                rename.RENAME().Rread(name_data=df, name_col="Проверяемый объект")

                df = df.rename(columns={"Название":"дата","Проверяемый объект":"магазин","Прогресс в %":"Прогресс"})
                df =df.loc[df['дата'].notnull()]
                df['дата'] = pd.to_datetime(df['дата'], format='%d.%m.%Y')

                # Группировка данных и выбор показателя по максимальной дате
                df = df.sort_values(by='дата').groupby(['магазин',"дата"]).last().reset_index()
                # Замените формат на ваш
                df['месяц'] = df['дата'].dt.month

                df = df.loc[df["дата"] >= "2023-01-01"]


                month_dict = {
                    1: "2023-01-01",
                    2: "2023-02-01",
                    3: "2023-03-01",
                    4: "2023-04-01",
                    5: "2023-05-01",
                    6: "2023-06-01",
                    7: "2023-07-01",
                    8: "2023-08-01",
                    9: "2023-09-01",
                    10: "2023-10-01",
                    11: "2023-11-01",
                    12: "2023-12-01"}
                df['месяц'] = df['месяц'].map(month_dict)
                df['месяц'] = pd.to_datetime(df['месяц'], format='%Y-%m-%d')
                df = df.drop(columns=["дата"])
                df = df.rename(columns={"месяц": "дата"})
                df.loc[df["КУО / нет"] == "Нет", "Прогресс"] = 0
                df = df[["магазин", "Прогресс", "дата"]]
                df = df.drop_duplicates()

                # Прошлый месяц
                df_last_month = df.loc[df["дата"] == (df["дата"].max()) - pd.DateOffset(months=1)]
                df_last_month = df_last_month[["магазин", "Прогресс", "дата"]]

                # максимальный месяц
                df_max_month = df.loc[df["дата"] == df["дата"].max()]
                df_max_month = df_max_month[["магазин", "Прогресс","дата"]]

                # Создайте список уникальных магазинов в df_max_month
                unique_max_month_stores = df_max_month['магазин'].unique()

                # Найдите магазины, которые отсутствуют в df_max_month
                missing_stores = df_last_month[~df_last_month['магазин'].isin(unique_max_month_stores)]
                df_max_mes = df["дата"].max()
                df_max_mes_add = (df["дата"].max()) + pd.DateOffset(months=1)
                missing_stores = missing_stores.drop(columns=["дата"])
                missing_stores["дата"] = df_max_mes
                df = pd.concat([df, missing_stores], axis=0)

                # максимальный месяц
                df_add = df.loc[df["дата"] == df["дата"].max()]
                df_add = df_add[["магазин", "Прогресс", "дата"]]

                df_add = df_add.drop(columns=["дата"])
                df_add["дата"] = df_max_mes_add

                df = pd.concat([df,  df_add], axis=0)

                # Сохранение обновленного DataFrame обратно в файл
                #df.to_excel('updated_file.xlsx', index=False)
            return df

# ФРС старт
        def g_2023(df):
            df = df.loc[df["план_выручка"].notnull()]
            maxdate = df["дата"].max()
            df = df.rename(columns={"дата":"отработано_дней"})
            df = df.groupby(["магазин", "год","месяц"],
                                  as_index=False).agg(
                {"выручка": "sum", "Количество чеков": "sum",
                 "списания_оказатель": "sum", "списания_хозы": "sum","отработано_дней":"count"}).reset_index(drop=True)
            month_dict = {
                1: "2023-01-01",
                2: "2023-02-01",
                3: "2023-03-01",
                4: "2023-04-01",
                5: "2023-05-01",
                6: "2023-06-01",
                7: "2023-07-01",
                8: "2023-08-01",
                9: "2023-09-01",
                10: "2023-10-01",
                11: "2023-11-01",
                12: "2023-12-01"}
            df['месяц'] = df['месяц'].map(month_dict)
            df['месяц'] = pd.to_datetime(df['месяц'], format='%Y-%m-%d')
            df = df.rename(columns={"месяц":"дата"})
    
            # Создание столбца с общим количеством дней в месяце
            df['дней в месяце'] = df["дата"].dt.daysinmonth
            # Создание столбца с количеством оставшихся дней до конца месяца
            df['осталось дней'] = df["дней в месяце"] - df["отработано_дней"]
    
            current_date = datetime.datetime.now()
            # Форматирование текущей даты в нужный формат (год-месяц-01)
            formatted_date = current_date.strftime("%Y-%m-01")
            df.loc[df["дата"]!=formatted_date,"осталось дней"]= 0
            df = pd.merge(df, plan, on=['магазин', "дата"], how='left')
    
    
            spqr, sprav_magaz, open_mag = rename.RENAME().magazin_info()
            sprav_magaz = sprav_magaz.loc[sprav_magaz["Менеджер"].notnull()]
            sprav_magaz = sprav_magaz.rename(columns={"!МАГАЗИН!": "магазин"})
            sprav_magaz = sprav_magaz[["магазин","Менеджер","Канал"]]
            df = pd.merge(df, sprav_magaz, on=["магазин"], how="left").reset_index(drop=True)
    
            # прогноз выручка
            df["прогноз_выручка"] = ((df["выручка"]/df["отработано_дней"]* df["осталось дней"])+df["выручка"])
            # прогноз чеки
            df["прогноз_количество_чеков"] = ((df["Количество чеков"] / df["отработано_дней"] * df["осталось дней"]) + df["Количество чеков"])
            # прогноз средний чек
            df["прогноз_Средний_чек"] = (df["прогноз_выручка"] / df["прогноз_количество_чеков"])
    
            # выполнение выручка
            df["прогноз_выручка"] = (df["прогноз_выручка"]  / df["план_выручка"])*100
            # ыполнение кол клиентов
            df["прогноз_количество_чеков"] =  (df["Количество чеков"] / df["план_кол_чеков"])*100
            # ыполнение средний чек
            df["прогноз_Средний_чек"] = (df["прогноз_Средний_чек"] / df["план_cредний_чек"])*100
            # процент списаняи
            df["Процент списания"] = (df["списания_оказатель"] / df["выручка"])*100
            df["средний_чек"] = df["выручка"] / df["Количество чеков"]
            #p(col="прогноз_количество_чеков")
            df["Месяц"] = df["дата"].dt.month
            df = df[["Менеджер","магазин","Канал", "дата", "Месяц", "выручка","прогноз_выручка", "Количество чеков","прогноз_количество_чеков","средний_чек","прогноз_Средний_чек", "Процент списания"]]
            ln = ["выручка", "прогноз_выручка", "Количество чеков", "прогноз_количество_чеков", "средний_чек", "прогноз_Средний_чек", "Процент списания"]
            for i in ln:
                df =df.rename(columns={i:f"{i}_2023"})
            return df,maxdate

        def g_2022(df,maxdate):
            maxdate = maxdate.replace("2023", "2022")
            df = df.loc[df["год"] == 2022]
            df = df.loc[df["дата"] <= maxdate]
            df = df.rename(columns={"дата": "отработано_дней"})
            df = df.groupby(["магазин", "год", "месяц"],
                            as_index=False).agg(
                {"выручка": "sum", "Количество чеков": "sum",
                 "списания_оказатель": "sum", "списания_хозы": "sum", "отработано_дней": "count"}).reset_index(
                drop=True)
            month_dict = {
                1: "2022-01-01",
                2: "2022-02-01",
                3: "2022-03-01",
                4: "2022-04-01",
                5: "2022-05-01",
                6: "2022-06-01",
                7: "2022-07-01",
                8: "2022-08-01",
                9: "2022-09-01",
                10: "2022-10-01",
                11: "2022-11-01",
                12: "2022-12-01"}
            df['месяц'] = df['месяц'].map(month_dict)
            df['месяц'] = pd.to_datetime(df['месяц'], format='%Y-%m-%d')
            df = df.rename(columns={"месяц": "дата"})

            # Создание столбца с общим количеством дней в месяце
            df['дней в месяце'] = df["дата"].dt.daysinmonth
            # Создание столбца с количеством оставшихся дней до конца месяца
            df['осталось дней'] = df["дней в месяце"] - df["отработано_дней"]

            current_date = datetime.datetime.now()
            # Форматирование текущей даты в нужный формат (год-месяц-01)
            formatted_date = current_date.strftime("%Y-%m-01")
            df.loc[df["дата"] != formatted_date, "осталось дней"] = 0
            df = pd.merge(df, plan, on=['магазин', "дата"], how='left')

            spqr, sprav_magaz, open_mag = rename.RENAME().magazin_info()
            sprav_magaz = sprav_magaz.loc[sprav_magaz["Менеджер"].notnull()]
            sprav_magaz = sprav_magaz.rename(columns={"!МАГАЗИН!": "магазин"})
            sprav_magaz = sprav_magaz[["магазин", "Менеджер"]]
            df = pd.merge(df, sprav_magaz, on=["магазин"], how="left").reset_index(drop=True)

            # прогноз выручка
            df["прогноз_выручка"] = ((df["выручка"] / df["отработано_дней"] * df["осталось дней"]) + df["выручка"])
            # прогноз чеки
            df["прогноз_количество_чеков"] = (
                        (df["Количество чеков"] / df["отработано_дней"] * df["осталось дней"]) + df["Количество чеков"])
            # прогноз средний чек
            df["прогноз_Средний_чек"] = (df["прогноз_выручка"] / df["прогноз_количество_чеков"])

            """df = df.groupby(["Менеджер", "дата", "год"],
                            as_index=False).agg(
                {"выручка": "sum", "прогноз_выручка": "sum", "план_выручка": "sum", "Количество чеков": "sum",
                 "план_кол_чеков": "sum",
                 "прогноз_Средний_чек": "mean", "план_cредний_чек": "mean", "списания_оказатель": "sum"}).reset_index(
                drop=True)"""

            # ыполнение выручка
            df["прогноз_выручка"] = (df["прогноз_выручка"] / df["план_выручка"])
            # ыполнение кол клиентов
            df["прогноз_количество_чеков"] = df["Количество чеков"] / df["план_кол_чеков"]
            # ыполнение средний чек
            df["прогноз_Средний_чек"] = df["прогноз_Средний_чек"] / df["план_cредний_чек"]
            # процент списаняи
            df["Процент списания"] = (df["списания_оказатель"] / df["выручка"])*100
            # p(col="прогноз_количество_чеков")
            df["Месяц"] = df["дата"].dt.month
            df["средний_чек"] = df["выручка"] / df["Количество чеков"]
            df = df[["Менеджер","магазин","Месяц","выручка","Количество чеков","Процент списания","средний_чек"]]
            ln = ["выручка","Количество чеков","Процент списания","средний_чек"]
            for i in ln:
                df =df.rename(columns={i:f"{i}_2022"})
            return df

        def personal():
            df_personal = pd.read_excel(
                "https://docs.google.com/spreadsheets/d/13tsxHb82mRcyQiYn78EGh7uV_6sUiq1zcAW3mo2aIFQ/export?exportFormat=xlsx",
                skiprows=1)
            df_personal["Укомплектованность %"] = (
                        df_personal["Фактическая численность"] / df_personal["Плановая численность"] * 100).round(2)

            df_shop = pd.read_excel(
                "https://docs.google.com/spreadsheets/d/1qXyD0hr1sOzoMKvMyUBpfTXDwLkh0RwLcNLuiNbWmSM/export?exportFormat=xlsx")

            df_personal = pd.merge(df_personal, df_shop[["МАГАЗИН", "!МАГАЗИН!"]], on=["МАГАЗИН"], how="left").reset_index(drop=True)
            df_personal = df_personal.loc[:, ["Ответственный за персонал", "!МАГАЗИН!", "Плановая численность", "Фактическая численность", "Укомплектованность %"]]
            df_personal = df_personal.rename(columns={"!МАГАЗИН!": "магазин"})

            today = date.today()
            df_personal["дата"] = today.strftime("%Y-%m") + "-" + "01"
            df_personal['дата'] = pd.to_datetime(df_personal['дата'], format='%Y-%m-%d')
            df_personal = df_personal[["Ответственный за персонал","магазин","дата","Плановая численность",
                                       "Фактическая численность","Укомплектованность %"]]
            return df_personal

        def turnover():
            df_turnover = pd.read_excel(
                "https://docs.google.com/spreadsheets/d/1cHRLQFBJ7_xuuuQ287nZ6sAJeG18WVm6o0Zk6Yb2rWA/export?exportFormat=xlsx")

            df_turnover["Текучесть"] = (df_turnover["Текучесть"] * 100).round(2)
            #df_turnover.fillna('', inplace=True)

            month_dict = {
                "Январь": "2023-01-01",
                "Февраль": "2023-02-01",
                "Март": "2023-03-01",
                "Апрель": "2023-04-01",
                "Май": "2023-05-01",
                "Июнь": "2023-06-01",
                "Июль": "2023-07-01",
                "Август": "2023-08-01",
                "Сентябрь": "2023-09-01",
                "Октябрь": "2023-10-01",
                "Ноябрь": "2023-11-01",
                "Декабрь": "2023-12-01"}
            df_turnover['Месяц'] = df_turnover['Месяц'].map(month_dict)
            df_turnover['Месяц'] = pd.to_datetime(df_turnover['Месяц'], format='%Y-%m-%d')
            df_turnover = df_turnover.rename(columns={"Адрес": "магазин", "Месяц": "дата"})
            df_turnover = df_turnover.dropna(subset=["ССЧ"])

            # Заполнение текущего месяца, если он пустой
            # Прошлый месяц
            df_turnover_last_month = df_turnover.loc[df_turnover["дата"] == (df_turnover["дата"].max()) - pd.DateOffset(months=1)]
            df_turnover_last_month = df_turnover_last_month[["Партнер", "магазин", "дата", "ССЧ", "Кол-во уволенных", "Текучесть"]]

            # максимальный месяц
            df_turnover_max_month = df_turnover.loc[df_turnover["дата"] == df_turnover["дата"].max()]
            df_turnover_max_month = df_turnover_max_month[["Партнер", "магазин", "дата", "ССЧ", "Кол-во уволенных", "Текучесть"]]

            # Создайте список уникальных магазинов в df_max_month
            unique_max_month_stores = df_turnover_max_month['магазин'].unique()

            # Код для пропуска текущего пустого месяца??
            # Найдите магазины, которые отсутствуют в df_max_month
            missing_stores = df_turnover_last_month[~df_turnover_last_month['магазин'].isin(unique_max_month_stores)]
            df_turnover_max_mes = df_turnover["дата"].max()
            df_turnover_max_mes_add = (df_turnover["дата"].max()) + pd.DateOffset(months=1)
            missing_stores = missing_stores.drop(columns=["дата"])
            missing_stores["дата"] = df_turnover_max_mes
            df_turnover = pd.concat([df_turnover, missing_stores], axis=0)

            # максимальный месяц
            df_turnover_add = df_turnover.loc[df_turnover["дата"] == df_turnover["дата"].max()]
            df_turnover_add = df_turnover_add[["Партнер", "магазин", "дата", "ССЧ", "Кол-во уволенных", "Текучесть"]]

            df_turnover_add = df_turnover_add.drop(columns=["дата"])
            df_turnover_add["дата"] = df_turnover_max_mes_add

            df_turnover = pd.concat([df_turnover, df_turnover_add], axis=0)

            #print(df_turnover)
            #df_turnover.to_excel("df_turnover.xlsx", index=False)
            return df_turnover

        def loyalty():
            path = r'P:\Фирменная розница\ФРС\Данные из SetRetail\Лояльность\Планы\Планы по проникновению(Раситанные).xlsx'
            df_loyalty = pd.read_excel(path, sheet_name="Sheet1")

            df_loyalty = df_loyalty.melt(id_vars="!МАГАЗИН!", var_name="дата", value_name="Лояльность")
            df_loyalty["Лояльность"] = (df_loyalty["Лояльность"] * 100).round(2)
            df_loyalty['дата'] = pd.to_datetime(df_loyalty['дата'], format='%Y-%m-%d')
            df_loyalty = df_loyalty.rename(columns={"!МАГАЗИН!": "магазин"})

            #print(df_loyalty)
            # df_loyalty.to_excel("loyalty.xlsx", index=False)
            return df_loyalty

        def education():
            path = r'C:\Users\lebedevvv\Desktop\FRS\Dashbord_new\Обученность\Матрица обучения.xlsx'
            df_education = pd.read_excel(path, sheet_name="Пользователи", skiprows=3)
            df_education = df_education.loc[:, ["Отдел", "Итого - процент прохождения"]]

            today = date.today()
            df_education["дата"] = today.strftime("%Y-%m") + "-" + "01"
            df_education['дата'] = pd.to_datetime(df_education['дата'], format='%Y-%m-%d')

            df_education = df_education.rename(columns={"Отдел": "магазин", "Итого - процент прохождения": "Обученность"})
            df_education = df_education[["магазин", "дата", "Обученность"]]

            df_education = df_education.groupby(["магазин", "дата"], as_index=False).agg(
                {"Обученность": "mean"}) \
                .reset_index(drop=True)
            df_education["Обученность"] = df_education["Обученность"].round(2)

            rename.RENAME().Rread(name_data=df_education, name_col="магазин")

            #print(df_education)
            #df_education.to_excel("df_education.xlsx", index=False)
            return df_education

# ФРС финиш
        df_2023, maxdate = g_2023(df)

        audit =  audit()
        df = pd.merge(df_2023, g_2022(df,maxdate), on=["Менеджер","Месяц","магазин"], how="left").reset_index(drop=True)

        df.fillna(0, inplace=True)

        df = pd.merge(df, audit[["дата","магазин","Прогресс"]], on=["магазин",'дата'], how="left").reset_index(drop=True)

        personal = personal()
        #df = pd.merge(df, personal[["дата","магазин", "Укомплектованность %"]], on=["магазин",'дата'], how="left").reset_index(drop=True)
        df = pd.merge(df, personal[["магазин", "Укомплектованность %"]], on=["магазин"], how="left").reset_index(
            drop=True)


        turnover = turnover()
        df = pd.merge(df, turnover[["дата","магазин", "Текучесть"]], on=["магазин",'дата'], how="left").reset_index(drop=True)

        loyalty = loyalty()
        df = pd.merge(df, loyalty[["магазин","дата", "Лояльность"]], on=["магазин", 'дата'], how="left").reset_index(drop=True)

        education = education()
        #df = pd.merge(df, education[["магазин", "дата", "Обученность"]], on=["магазин", 'дата'], how="left").reset_index(drop=True)
        df = pd.merge(df, education[["магазин", "Обученность"]], on=["магазин"], how="left").reset_index(drop=True)

        df["YoY_sales"] = ((df["выручка_2023"] -df["выручка_2022"])/df["выручка_2022"])*100
        df["YoY_check"] = ((df["Количество чеков_2023"] - df["Количество чеков_2022"])/ df["Количество чеков_2022"])*100
        df["YoY_aver_check"] = ((df["средний_чек_2023"] - df["средний_чек_2022"]) / df["средний_чек_2022"])*100
        df["YoY_drop_sales"] = (df["Процент списания_2023"] - df["Процент списания_2022"])
        #df = df.loc[df["YoY_sales"] != np.inf]
        df = df.loc[df["магазин"] != "Барнаул Энтузиастов, 14"]
        df = df.drop(columns=["выручка_2023","Количество чеков_2023","средний_чек_2023","выручка_2022","Количество чеков_2022","средний_чек_2022","Месяц"])

        def prognoz_sales(yoy_sales, max_points): # Расчет баллов для выручки
            if yoy_sales < 80:
                return 0
            elif yoy_sales >= 99:
                return max_points
            else:
                normalized_value = (yoy_sales - 80) / 19  # Приведение к интервалу [0, 1]
                points = (float(normalized_value * max_points)).__round__(1) # Пропорциональное распределение Балллов
                return points

        def YoY(yoy_sales, max_points): # Расчет баллов для отношения год к году
            if yoy_sales < 0:
                return 0
            if yoy_sales == np.inf:
                max_points = max_points/2
                return max_points
            elif yoy_sales >= 15:
                return max_points
            else:
                normalized_value = yoy_sales / 15  # Приведение к интервалу [0, 1]
                points = (float(normalized_value * max_points)).__round__(1)  # Пропорциональное распределение Балллов
                return points

        def points_turnover(percent, max_points): # Расчет баллов для текучести
            if percent <= 0:
                return max_points
            if percent == np.inf:
                max_points = max_points/2
                return max_points
            elif percent >= 30:
                return 0
            else:
                normalized_value = (30 - percent) / 30  # Приведение к интервалу [0, 1]
                points = (float(normalized_value * max_points)).__round__(1)  # Пропорциональное распределение Балллов
                return points

        def points_loyalty(percent, max_points): # Расчет баллов для лояльности
            if percent >= 38:
                return max_points
            if percent == np.inf:
                max_points = max_points/2
                return max_points
            elif percent <= 20:
                return 0
            else:
                normalized_value = (percent - 20) / 18  # Приведение к интервалу [0, 1]
                points = (float(normalized_value * max_points)).__round__(1)  # Пропорциональное распределение Балллов
                return points

        def points_education(yoy_sales, max_points): # Расчет баллов для обученности
            if yoy_sales < 60:
                return 0
            elif yoy_sales >= 100:
                return max_points
            else:
                normalized_value = (yoy_sales - 60) / 40  # Приведение к интервалу [0, 1]
                points = (float(normalized_value * max_points)).__round__(1) # Пропорциональное распределение Балллов
                return points

        # Распределение баллов
        def franshiza(d):
            mask_frs = d["Канал"] == "Франшиза инвестиционнная"
            min_not_sales = 1

            max_points_yoy = 20 # Изменение к прошлому году, выручка
            d.loc[mask_frs, "Балл изменение к прошлому году выручка"] = d[mask_frs]["YoY_sales"].apply(YoY, args=(max_points_yoy,))
            d["Балл изменение к прошлому году выручка"] = d["Балл изменение к прошлому году выручка"].replace(np.inf, min_not_sales)

            max_points_count_receipt = 10 # Кол.чеков
            d.loc[mask_frs, "Балл изменение к прошлому году Кол.чеков"] = d[mask_frs]["YoY_check"].apply(YoY, args=(max_points_count_receipt,))
            d["Балл изменение к прошлому году Кол.чеков"] = d["Балл изменение к прошлому году Кол.чеков"].replace(np.inf, min_not_sales)

            max_points_average_bill = 10 # Ср.чек
            d.loc[mask_frs, "Балл изменение к прошлому году Ср.чек"] = d[mask_frs]["YoY_aver_check"].apply(YoY, args=(max_points_average_bill,))
            d["Балл изменение к прошлому году Ср.чек"] = d["Балл изменение к прошлому году Ср.чек"].replace(np.inf, min_not_sales)

            max_points_audit = 20 # Аудиты
            d.loc[mask_frs, "Балл_Аудиты"] = d[mask_frs]["Прогресс"].apply(prognoz_sales, args=(max_points_audit,))

            max_points_personal = 10 # Укомплектованность
            d.loc[mask_frs, "Балл_Укомплектованность"] = d[mask_frs]["Укомплектованность %"].apply(prognoz_sales, args=(max_points_personal,))

            max_points_turnover = 10  # Текучесть
            d.loc[mask_frs, "Балл_Текучесть"] = d[mask_frs]["Текучесть"].apply(points_turnover, args=(max_points_turnover,))

            max_points_loyalty = 10  # Лояльность
            d.loc[mask_frs, "Балл_Лояльность"] = d[mask_frs]["Лояльность"].apply(points_loyalty, args=(max_points_loyalty,))

            max_points_education = 10  # Обученность
            d.loc[mask_frs, "Балл_Обученность"] = d[mask_frs]["Обученность"].apply(points_education, args=(max_points_education,))


            mask_frs = d["Канал"] == "Франшиза в аренду"
            min_not_sales = 1

            max_points_yoy = 20 # Изменение к прошлому году выручка
            d.loc[mask_frs, "Балл изменение к прошлому году выручка"] = d[mask_frs]["YoY_sales"].apply(YoY, args=(max_points_yoy,))
            d["Балл изменение к прошлому году выручка"] = d["Балл изменение к прошлому году выручка"].replace(np.inf, min_not_sales)

            max_points_count_receipt = 10 # Кол.чеков
            d.loc[mask_frs, "Балл изменение к прошлому году Кол.чеков"] = d[mask_frs]["YoY_check"].apply(YoY, args=(max_points_count_receipt,))
            d["Балл изменение к прошлому году Кол.чеков"] = d["Балл изменение к прошлому году Кол.чеков"].replace(np.inf, min_not_sales)

            max_points_average_bill = 10 # Ср.чек
            d.loc[mask_frs, "Балл изменение к прошлому году Ср.чек"] = d[mask_frs]["YoY_aver_check"].apply(YoY, args=(max_points_average_bill,))
            d["Балл изменение к прошлому году Ср.чек"] = d["Балл изменение к прошлому году Ср.чек"].replace(np.inf, min_not_sales)

            max_points_audit = 20 # Аудиты
            d.loc[mask_frs, "Балл_Аудиты"] = d[mask_frs]["Прогресс"].apply(prognoz_sales, args=(max_points_audit,))
            d = d.loc[d["Канал"] != "ФРС"]

            max_points_personal = 10  # Укомплектованность
            d.loc[mask_frs, "Балл_Укомплектованность"] = d.loc[mask_frs]["Укомплектованность %"].apply(prognoz_sales, args=(max_points_personal,))

            max_points_turnover = 10  # Текучесть
            d.loc[mask_frs, "Балл_Текучесть"] = d.loc[mask_frs]["Текучесть"].apply(points_turnover, args=(max_points_turnover,))

            max_points_loyalty = 10  # Лояльность
            d.loc[mask_frs, "Балл_Лояльность"] = d.loc[mask_frs]["Лояльность"].apply(points_loyalty, args=(max_points_loyalty,))

            max_points_education = 10  # Обученность
            d.loc[mask_frs, "Балл_Обученность"] = d.loc[mask_frs]["Обученность"].apply(points_education,args=(max_points_education,))

            return d

        def nextd(a, x):
            df = franshiza(a)

            df = df.fillna(0)
            df['Общий'] = (df["Балл изменение к прошлому году выручка"] +
                            df["Балл изменение к прошлому году Кол.чеков"] +
                            df["Балл изменение к прошлому году Ср.чек"] +
                            df["Балл_Аудиты"] +
                            df["Балл_Укомплектованность"] +
                            df["Балл_Текучесть"] +
                            df["Балл_Лояльность"] +
                            df["Балл_Обученность"].fillna(0))

            df = df.rename(columns={"YoY_sales":"2022/2023 выручка",
                                        "YoY_check":"2022/2023 Кол.чеков","YoY_aver_check":"2022/2023 Ср.чек",
                                        "Прогресс":"Аудиты"})

            df = df[["Менеджер","магазин","Канал","дата",
                         "2022/2023 выручка","Балл изменение к прошлому году выручка","2022/2023 Кол.чеков",
                       "Балл изменение к прошлому году Кол.чеков",
                         "2022/2023 Ср.чек","Балл изменение к прошлому году Ср.чек","Аудиты","Балл_Аудиты",
                         "Укомплектованность %", "Балл_Укомплектованность", "Текучесть", "Балл_Текучесть",
                         "Лояльность", "Балл_Лояльность", "Обученность", "Балл_Обученность", 'Общий']]

            df = df.loc[df["дата"]>="2023-01-01"]
            return df

        df_f = df.copy()
        Franshiza = nextd(a = df_f, x="Franshiza")
        sprav_magaz = pd.read_excel(r"https://docs.google.com/spreadsheets/d/1CdOvV2uPgSRO06KwHRtqc3f0DbXOAy-gxlAZP1F9lqY/export?exportFormat=xlsx", sheet_name="Справочник партнеров")
        Franshiza = Franshiza.merge(sprav_magaz, on=["магазин"], how="left").reset_index(drop=True)

        Franshiza = Franshiza[["Партнер", "магазин", "Канал", "дата",
               "2022/2023 выручка", "Балл изменение к прошлому году выручка", "2022/2023 Кол.чеков",
               "Балл изменение к прошлому году Кол.чеков",
               "2022/2023 Ср.чек", "Балл изменение к прошлому году Ср.чек", "Аудиты", "Балл_Аудиты",
                "Укомплектованность %", "Балл_Укомплектованность", "Текучесть", "Балл_Текучесть",
                "Лояльность", "Балл_Лояльность", "Обученность", "Балл_Обученность", 'Общий']]

        Franshiza.replace([np.inf, -np.inf], np.nan, inplace=True)
        Franshiza.fillna('', inplace=True)
        Franshiza["дата"] = Franshiza["дата"].astype(str)


        #Franshiza.to_excel("df_Franshiza.xlsx", index=False)

        g.tbl_bot().svodniy_itog(name_tbl="Франшиза_баллы", df=Franshiza,
                                 sheet_name="Франшиза_по магазинам")

        Franshiza =  Franshiza.groupby(["Партнер","Канал","дата"], as_index=False).agg(
            {"Балл изменение к прошлому году выручка": "mean",
             "Балл изменение к прошлому году Кол.чеков": "mean",
             "Балл изменение к прошлому году Ср.чек": "mean",
             "Балл_Аудиты": "mean",
             "Балл_Укомплектованность": "mean",
             "Балл_Текучесть": "mean",
             "Балл_Лояльность": "mean",
             "Балл_Обученность": "mean",
             'Общий':"mean"}) \
            .reset_index(drop=True)

        Franshiza.replace([np.inf, -np.inf], np.nan, inplace=True)
        Franshiza.fillna('', inplace=True)
        Franshiza["дата"] = Franshiza["дата"].astype(str)


        #Franshiza.to_excel("df_Franshiza_group.xlsx", index=False)
        g.tbl_bot().svodniy_itog(name_tbl="Франшиза_баллы", df=Franshiza,
                                 sheet_name="Франшиза_по_партнерам")
        return

def run_reyting():
    dat = reting_franshiza()
    raschet = dat.run_2()
    return raschet

if __name__ == '__main__':
    dat = reting_franshiza()
    raschet = dat.run_2()