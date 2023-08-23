import datetime

import pandas as pd
from Bot_FRS_v2.INI import ini, rename

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

        # Рассчитываем баллы для каждого показателя
        max_score = 100

        df['Балл выручки'] = max_score * df['прогноз_выручка']
        df['Балл чеков'] = max_score * df['прогноз_количество_чеков']
        df['Балл среднего чека'] = max_score * df['прогноз_Средний_чек']

        # Балл списания будет рассчитываться иначе из-за влияния на баллы
        for index, row in df.iterrows():
            if row['Процент списания'] > 0.025:
                df.at[index, 'Балл списания'] = max_score - (max_score * row['Процент списания'])
            else:
                df.at[index, 'Балл списания'] = max_score + (max_score * row['Процент списания'] * 2)

        # Рассчитываем общий балл с учетом весов
        weights = {
            'Балл выручки': 0.6,
            'Балл чеков': 0.2,
            'Балл среднего чека': 0.1,
            'Балл списания': 0.1
        }

        df['Общий балл'] = (df[list(weights.keys())] * pd.Series(weights)).sum(axis=1)

        step = 0.1
        # Округляем баллы до ближайшего меньшего числа, кратного шагу
        for col in ['Балл выручки', 'Балл чеков', 'Балл среднего чека', 'Балл списания', 'Общий балл']:
            df[col] = (df[col] // step) * step

        df = df[["Менеджер","дата","год","выручка","Количество чеков","Процент списания","Общий балл","Балл выручки","Балл чеков","Балл среднего чека","Балл списания"]]
        print(df[:50])
        df.to_excel(r"C:\Users\lebedevvv\Desktop\FRS\Dashbord_new\♀Планы\Показатели для расчета рейтинга.xlsx",index=False)



dat = reting()
raschet = dat.run()