import datetime
import os
from Bot_FRS_v2.GooGL_TBL import Google as g
import numpy as np
import pandas as pd
from Bot_FRS_v2.INI import ini, rename
import reprlib

pd.set_option("expand_frame_repr", False)
pd.set_option('display.max_colwidth', None)


class reting():

    def __init__(self):
        PUT = ini.PUT
        self.df = pd.read_csv(PUT + "♀Вычисляемые_таблицы\\Нарастающие итоги.csv", sep="\t", encoding="utf-8",
                              decimal=".")
        # панов прдаж
        plan = pd.read_excel(PUT + "♀Планы\\Планы ДЛЯ ДАШБОРДА.xlsx")
        plan['дата'] = pd.to_datetime(plan['дата'], format='%d.%m.%Y')
        plan.loc[plan["Показатель"] == "Выручка", "план_выручка"] = plan["ПЛАН"].round(0)
        plan.loc[plan["Показатель"] == "Средний чек", "план_cредний_чек"] = plan["ПЛАН"].round(0)
        plan.loc[plan["Показатель"] == "Кол чеков", "план_кол_чеков"] = plan["ПЛАН"].round(0)
        plan = plan.drop(["ПЛАН", "Показатель","Проверка"], axis=1)
        plan = plan.groupby(["магазин", "дата"]).sum().reset_index()
        self.plan = plan


    def run(self):
        df = self.df
        plan = self.plan
        df = df.loc[df["план_выручка"].notnull()]
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
        sprav_magaz = sprav_magaz[["магазин","Менеджер"]]
        df = pd.merge(df, sprav_magaz, on=["магазин"], how="left").reset_index(drop=True)

        # прогноз выручка
        df["прогноз_выручка"] = ((df["выручка"]/df["отработано_дней"]* df["осталось дней"])+df["выручка"])
        # прогноз чеки
        df["прогноз_количество_чеков"] = ((df["Количество чеков"] / df["отработано_дней"] * df["осталось дней"]) + df["Количество чеков"])
        # прогноз средний чек
        df["прогноз_Средний_чек"] = (df["прогноз_выручка"] / df["прогноз_количество_чеков"])

        df = df.groupby(["Менеджер", "дата", "год"],
                        as_index=False).agg(
            {"выручка":"sum","прогноз_выручка": "sum", "план_выручка": "sum", "Количество чеков": "sum", "план_кол_чеков": "sum",
             "прогноз_Средний_чек": "mean", "план_cредний_чек": "mean","списания_оказатель":"sum" }).reset_index(drop=True)

        # ыполнение выручка
        df["прогноз_выручка"] = (df["прогноз_выручка"] / df["план_выручка"])
        # ыполнение кол клиентов
        df["прогноз_количество_чеков"] =  df["Количество чеков"] / df["план_кол_чеков"]
        # ыполнение средний чек
        df["прогноз_Средний_чек"] = df["прогноз_Средний_чек"] / df["план_cредний_чек"]
        # процент списаняи
        df["Процент списания"] = df["списания_оказатель"] / df["выручка"]
        #p(col="прогноз_количество_чеков")
        print(df)


        # Преобразуем столбец 'Дата' в формат даты и добавляем столбец 'Месяц'
        df['дата'] = pd.to_datetime(df['дата'])
        df['Месяц'] = df['дата'].dt.to_period('M')

        # Рассчитываем Балллы для каждого показателя
        max_score = 100

        df['Баллл выручки'] = max_score * df['прогноз_выручка']
        df['Баллл чеков'] = max_score * df['прогноз_количество_чеков']
        df['Баллл среднего чека'] = max_score * df['прогноз_Средний_чек']

        # Баллл списания будет рассчитываться иначе из-за влияния на Балллы
        for index, row in df.iterrows():
            if row['Процент списания'] > 0.025:
                df.at[index, 'Баллл списания'] = max_score - (max_score * row['Процент списания'])
            else:
                df.at[index, 'Баллл списания'] = max_score + (max_score * row['Процент списания'] * 2)

        # Рассчитываем общий Баллл с учетом весов
        weights = {
            'Баллл выручки': 0.6,
            'Баллл чеков': 0.2,
            'Баллл среднего чека': 0.1,
            'Баллл списания': 0.1
        }
        df['Общий Баллл'] = (df[list(weights.keys())] * pd.Series(weights)).sum(axis=1)

        step = 0.1
        # Округляем Балллы до ближайшего меньшего числа, кратного шагу
        for col in ['Баллл выручки', 'Баллл чеков', 'Баллл среднего чека', 'Баллл списания', 'Общий Баллл']:
            df[col] = (df[col] // step) * step

        df = df[["Менеджер","дата","год","выручка","Количество чеков","Процент списания","Общий Баллл","Баллл выручки","Баллл чеков","Баллл среднего чека","Баллл списания"]]
        print(df[:50])
        df.to_excel(r"C:\Users\lebedevvv\Desktop\FRS\Dashbord_new\♀Планы\Показатели для расчета рейтинга.xlsx",index=False)

    def run_2(self):
        df = self.df
        plan = self.plan

        def audit():
            # Путь к директории с файлами
            p_palic = r"C:\Users\lebedevvv\Desktop\FRS\Dashbord_new\Аудиты"
            # Создаем пустой список для хранения имен файлов, которые содержат "Отчёт"
            report_files = []
            # Проходим через все файлы в указанной директории
            for filename in os.listdir(p_palic):

                if "Отчёт" in filename and "~$" not in filename:
                    report_files.append(filename)


            df = pd.DataFrame()
            for filename in report_files:
                full_path = os.path.join(p_palic, filename)

                df = pd.read_excel(full_path, sheet_name="1) общая оценка")
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
                #№№№
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


                print(df)
                # Сохранение обновленного DataFrame обратно в файл
                df.to_excel('updated_file.xlsx', index=False)

            return df


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
    
            """df = df.groupby(["Менеджер", "дата", "год"],
                            as_index=False).agg(
                {"выручка":"sum","прогноз_выручка": "sum", "план_выручка": "sum", "Количество чеков": "sum", "план_кол_чеков": "sum",
                 "прогноз_Средний_чек": "mean", "план_cредний_чек": "mean","списания_оказатель":"sum" }).reset_index(drop=True)"""
    
            # ыполнение выручка
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
            df = df.loc[df["год"]==2022]
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


        df_2023, maxdate = g_2023(df)

        audit =  audit()


        df = pd.merge(df_2023, g_2022(df,maxdate), on=["Менеджер","Месяц","магазин"], how="left").reset_index(drop=True)
        print("dd", df[:50])

        df.fillna(0, inplace=True)
        df = pd.merge(df, audit[["дата","магазин","Прогресс"]], on=["магазин",'дата'], how="left").reset_index(drop=True)
        df.to_excel("1.xlsx", index=False)

        df["YoY_sales"] = ((df["выручка_2023"] -df["выручка_2022"])/df["выручка_2022"])*100
        df["YoY_check"] = ((df["Количество чеков_2023"] - df["Количество чеков_2022"])/ df["Количество чеков_2022"])*100
        df["YoY_aver_check"] = ((df["средний_чек_2023"] - df["средний_чек_2022"]) / df["средний_чек_2022"])*100
        df["YoY_drop_sales"] = (df["Процент списания_2023"] - df["Процент списания_2022"])
        df = df.loc[df["YoY_sales"] != np.inf]
        df = df.loc[df["магазин"] != "Барнаул Энтузиастов, 14"]
        df = df.drop(columns=["выручка_2023","Количество чеков_2023","средний_чек_2023","выручка_2022","Количество чеков_2022","средний_чек_2022","Месяц"])

        """df_reting = pd.read_excel("https://docs.google.com/spreadsheets/d/1WuM9yLaSHvf32q_nQvQM_e8ivfWnc8Kq4ZbrfytjJQA/export?exportFormat=xlsx",skiprows=1)
        print(df_reting)
        forecast_FRS = df_reting.loc[df_reting['Канал'] == 'ФРС', 'Прогноз выполнения выручка'].values[0]
        print("Максимальный Балл FRS", forecast_FRS)"""

        def prognoz_sales(yoy_sales, max_points):
            if yoy_sales < 80:
                return 0
            elif yoy_sales >= 99:
                return max_points
            else:
                normalized_value = (yoy_sales - 80) / 19  # Приведение к интервалу [0, 1]
                points = (float(normalized_value * max_points)).__round__(1) # Пропорциональное распределение Балллов
                return points

        def YoY(yoy_sales, max_points):
            if yoy_sales < 0:
                return 0
            elif yoy_sales >= 15:
                return max_points
            else:
                normalized_value = yoy_sales / 15  # Приведение к интервалу [0, 1]
                points = (float(normalized_value * max_points)).__round__(1)  # Пропорциональное распределение Балллов
                return points

        def calculate_points(percent, max_points):
            if percent <= 0:
                return max_points
            elif percent >= 5:
                return 0
            else:
                normalized_value = (5 - percent) / 5  # Приведение к интервалу [0, 1]
                points = (float(normalized_value * max_points)).__round__(1)    # Пропорциональное распределение Балллов
                return points

        def Total(d):
            mask_frs = (df["Канал"] == "ФРС") | (df["Канал"] == "Франшиза инвестиционнная") | (df["Канал"] == "Франшиза в аренду")
            #mask_frs = df
            max_points = 25
            df.loc[mask_frs, "Балл факт(прогноз) выручка"] = df[mask_frs]["прогноз_выручка_2023"].apply(prognoz_sales,                                                                                   args=(max_points,))
            max_points = 5
            df.loc[mask_frs, "Балл факт(прогноз) Кол.чеков"] = df[mask_frs]["прогноз_количество_чеков_2023"].apply(
                prognoz_sales, args=(max_points,))
            max_points = 10
            df.loc[mask_frs, "Балл факт(прогноз) Ср.чек"] = df[mask_frs]["прогноз_Средний_чек_2023"].apply(prognoz_sales,
                                                                                                            args=(
                                                                                                            max_points,))
            max_points_yoy = 25
            df.loc[mask_frs, "Балл изменение к прошлому году выручка"] = df[mask_frs]["YoY_sales"].apply(YoY, args=(max_points_yoy,))
            max_points_yoy = 5
            df.loc[mask_frs, "Балл изменение к прошлому году Кол.чеков"] = df[mask_frs]["YoY_check"].apply(YoY, args=(max_points_yoy,))
            max_points_yoy = 10
            df.loc[mask_frs, "Балл изменение к прошлому году Ср.чек"] = df[mask_frs]["YoY_aver_check"].apply(YoY, args=(max_points_yoy,))

            max_points = 10  # Максимальное значение Балллов
            df.loc[mask_frs, "Балл_Процент_списания"] = df[mask_frs]["Процент списания_2023"].apply(calculate_points, args=(max_points,))

            max_points = 10  # Максимальное значение Балллов
            df.loc[mask_frs, "Балл_Аудиты"] = df[mask_frs]["Прогресс"].apply(prognoz_sales,args=(max_points,))
            return df

        def franshiza(d):
            mask_frs = d["Канал"] == "Франшиза инвестиционнная"
            min_not_sales = 1

            max_points_yoy = 30
            d.loc[mask_frs, "Балл изменение к прошлому году выручка"] = d[mask_frs]["YoY_sales"].apply(YoY, args=(max_points_yoy,))
            d["Балл изменение к прошлому году выручка"] = d["Балл изменение к прошлому году выручка"].replace(np.inf, min_not_sales)

            max_points_yoy = 10
            d.loc[mask_frs, "Балл изменение к прошлому году Кол.чеков"] = d[mask_frs]["YoY_check"].apply(YoY, args=(max_points_yoy,))
            d["Балл изменение к прошлому году Кол.чеков"] = d["Балл изменение к прошлому году Кол.чеков"].replace(np.inf, min_not_sales)

            max_points_yoy = 20
            d.loc[mask_frs, "Балл изменение к прошлому году Ср.чек"] = d[mask_frs]["YoY_aver_check"].apply(YoY, args=(max_points_yoy,))
            d["Балл изменение к прошлому году Ср.чек"] = d["Балл изменение к прошлому году Ср.чек"].replace(np.inf, min_not_sales)

            max_points_yoy = 40
            d.loc[mask_frs, "Балл_Аудиты"] = d[mask_frs]["Прогресс"].apply(prognoz_sales, args=(max_points_yoy,))



            mask_frs = d["Канал"] == "Франшиза в аренду"
            min_not_sales = 1

            max_points_yoy = 30
            d.loc[mask_frs, "Балл изменение к прошлому году выручка"] = d[mask_frs]["YoY_sales"].apply(YoY, args=(max_points_yoy,))
            d["Балл изменение к прошлому году выручка"] = d["Балл изменение к прошлому году выручка"].replace(np.inf, min_not_sales)

            max_points_yoy = 10
            d.loc[mask_frs, "Балл изменение к прошлому году Кол.чеков"] = d[mask_frs]["YoY_check"].apply(YoY, args=(max_points_yoy,))
            d["Балл изменение к прошлому году Кол.чеков"] = d["Балл изменение к прошлому году Кол.чеков"].replace(np.inf, min_not_sales)

            max_points_yoy = 20
            d.loc[mask_frs, "Балл изменение к прошлому году Ср.чек"] = d[mask_frs]["YoY_aver_check"].apply(YoY, args=(max_points_yoy,))
            d["Балл изменение к прошлому году Ср.чек"] = d["Балл изменение к прошлому году Ср.чек"].replace(np.inf, min_not_sales)

            max_points_yoy = 40
            d.loc[mask_frs, "Балл_Аудиты"] = d[mask_frs]["Прогресс"].apply(prognoz_sales, args=(max_points_yoy,))
            d = d.loc[d["Канал"] != "ФРС"]
            return d


        def nextd(a, x):
            if x == "TOTAL":
                d = Total(a)
                print("ntotol")
                d.fillna(0, inplace=True)
                d['Общий'] = d["Балл факт(прогноз) выручка"] + \
                             d["Балл факт(прогноз) Кол.чеков"] + \
                             d["Балл факт(прогноз) Ср.чек"] + \
                             d["Балл изменение к прошлому году выручка"] + \
                             d["Балл изменение к прошлому году Кол.чеков"] + \
                             d["Балл изменение к прошлому году Ср.чек"] + \
                             d["Балл_Процент_списания"] + \
                             d["Балл_Аудиты"].fillna(0)

                d = d.rename(columns={"YoY_sales": "2022/2023 выручка",
                                      "YoY_check": "2022/2023 Кол.чеков", "YoY_aver_check": "2022/2023 Ср.чек",
                                      "Прогресс": "Аудиты"})

                d = d[["Менеджер", "магазин", "Канал", "дата",
                       "прогноз_выручка_2023", "Балл факт(прогноз) выручка",
                       "прогноз_количество_чеков_2023", "Балл факт(прогноз) Кол.чеков",
                       "прогноз_Средний_чек_2023", "Балл факт(прогноз) Ср.чек",
                       "2022/2023 выручка", "Балл изменение к прошлому году выручка", "2022/2023 Кол.чеков",
                       "Балл изменение к прошлому году Кол.чеков",
                       "2022/2023 Ср.чек", "Балл изменение к прошлому году Ср.чек", "Процент списания_2023",
                       "Балл_Процент_списания", "Аудиты", "Балл_Аудиты", 'Общий']]

                df = d.loc[d["дата"] >= "2023-01-01"]

                print(df[:50])
            else:
                print("franshiz")
                d = franshiza(a)

                d.fillna(0, inplace=True)
                d['Общий'] =  d[ "Балл изменение к прошлому году выручка"] + \
                              d["Балл изменение к прошлому году Кол.чеков"] + \
                              d["Балл изменение к прошлому году Ср.чек"] + \
                              d["Балл_Аудиты"].fillna(0)

                d = d.rename(columns={"YoY_sales":"2022/2023 выручка",
                                        "YoY_check":"2022/2023 Кол.чеков","YoY_aver_check":"2022/2023 Ср.чек",
                                        "Прогресс":"Аудиты"})

                d = d[["Менеджер","магазин","Канал","дата",
                         "2022/2023 выручка","Балл изменение к прошлому году выручка","2022/2023 Кол.чеков",
                       "Балл изменение к прошлому году Кол.чеков",
                         "2022/2023 Ср.чек","Балл изменение к прошлому году Ср.чек","Аудиты","Балл_Аудиты",'Общий']]

                df = d.loc[d["дата"]>="2023-01-01"]

                print(df[:50])
            return df


        df_t = df.copy()
        df_f = df.copy()
        TOTAL = nextd( a = df_t, x="TOTAL")

        TOTAL.to_excel(r"C:\Users\lebedevvv\Desktop\FRS\Dashbord_new\♀Планы\Показатели для расчета рейтинга_2.xlsx",
                    index=False)
        # Оставляем статические столбцы
        static_columns = ["Менеджер", "магазин", "Канал", "дата"]
        # df = df.drop(columns=['Общий_Балл'])
        # Метод melt для переворачивания исходной таблицы
        melted_df = TOTAL.melt(id_vars=static_columns, var_name="Показатель", value_name="Значение")
        # Замена значений "inf" на 0
        melted_df["Значение"] = melted_df["Значение"].replace(np.inf, 0)
        # Вывод результата

        # Создание столбца "Баллловой показатель"
        melted_df["Балловой показатель"] = melted_df["Показатель"].apply(
            lambda x: 1 if "Балл" in x else 2 if 'Общий' in x else 0)
        #print(melted_df[:50])
        melted_df.to_excel(r"C:\Users\lebedevvv\Desktop\FRS\Dashbord_new\♀Планы\Показатели для расчета рейтинга.xlsx",
                           index=False)

        Franshiza = nextd(a = df_f, x="Franshiza")
        df = df.drop(columns=["Менеджер"])
        spqr, sprav_magaz, open_mag = rename.RENAME().magazin_info()

        sprav_magaz = sprav_magaz[["!МАГАЗИН!", "Юр. лицо"]]
        sprav_magaz = sprav_magaz.rename(columns={"!МАГАЗИН!": "магазин","Юр. лицо":"Партнер"})
        Franshiza = Franshiza.merge(sprav_magaz, on=["магазин"], how="left").reset_index(drop=True)


        Franshiza = Franshiza[["Партнер", "магазин", "Канал", "дата",
               "2022/2023 выручка", "Балл изменение к прошлому году выручка", "2022/2023 Кол.чеков",
               "Балл изменение к прошлому году Кол.чеков",
               "2022/2023 Ср.чек", "Балл изменение к прошлому году Ср.чек", "Аудиты", "Балл_Аудиты", 'Общий']]

        #Franshiza["2022/2023 выручка"] = Franshiza["2022/2023 выручка"].apply(reprlib.repr)
        Franshiza .replace([np.inf, -np.inf], np.nan, inplace=True)
        Franshiza .fillna('', inplace=True)
        Franshiza["дата"] = Franshiza["дата"].astype(str)

        g.tbl_bot().svodniy_itog(name_tbl="Франшиза_балы", df=Franshiza,
                                 sheet_name="Франшиза_по магазинам")

        Franshiza =  Franshiza.groupby(["Партнер","Канал","дата"], as_index=False).agg(
            {"Балл изменение к прошлому году выручка": "mean",
             "Балл изменение к прошлому году Кол.чеков": "mean",
             "Балл изменение к прошлому году Ср.чек": "mean",
             "Балл_Аудиты": "mean",
             'Общий':"mean"}) \
            .reset_index(drop=True)

        Franshiza.replace([np.inf, -np.inf], np.nan, inplace=True)
        Franshiza.fillna('', inplace=True)
        Franshiza["дата"] = Franshiza["дата"].astype(str)

        g.tbl_bot().svodniy_itog(name_tbl="Франшиза_балы", df=Franshiza,
                                 sheet_name="Франшиза_по_партнерам")
        return




if __name__ == '__main__':
    dat = reting()
    raschet = dat.run_2()