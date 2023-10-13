import sys
sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON\venv\Lib\site-packages")
sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON")
from datetime import datetime, timedelta, time, date
import datetime
import holidays
import pandas as pd

pd.set_option("expand_frame_repr", False)
pd.set_option('display.max_colwidth', None)

class CustomRusHolidays(holidays.RU):
    def _populate(self, year,):
        super()._populate(year)
        # Добавляем в наш пользовательский набор праздников все официальные выходные дни.
        self[date(year, 5, 6)] = "День Воинской славы России"
        self[date(year, 5, 7)] = "День Воинской славы России"
        self[date(year, 5, 8)] = "День Победы"
        self[date(year, 5, 9)] = "День Победы"
        # Коректировка выходных дней

class BaseClass():
    def __init__(self):
        # текущаяя дата
        self.new_month = None
        date_now = datetime.datetime.now().date()
        date_now = datetime.datetime.strptime("2023-09-04", '%Y-%m-%d').date()
        last_day = date_now - datetime.timedelta(days=1)
        self.PUT = "C:\\Users\\Lebedevvv\\Desktop\\FRS\\Dashbord_new\\"
        # определение выходных дней
        def is_workday(date):
            ru_holidays = CustomRusHolidays()
            if date.weekday() >= 5:  # Если это суббота или воскресенье, то это выходной день.
                return False
            elif date in ru_holidays:  # Если это праздничный день, то это выходной день.
                return False
            else:
                return True  # Иначе это рабочий день.

        # список отставшихся и прошедштх дней
        def count_dey():
            # Текущая дата
            current_date = datetime.date.today()
            # Определяем первый день текущего месяца
            first_day = current_date.replace(day=1)
            # Определяем первый день следующего месяца
            next_month = first_day.replace(month=first_day.month + 1)
            # Определяем последний день текущего месяца
            last_day = next_month - datetime.timedelta(days=1)
            # Вычисляем количество дней в текущем месяце
            days_in_month = last_day.day
            # Вычисляем количество прошедших дней в текущем месяце
            days_last = current_date.day - 1
            # Вычисляем количество оставшихся дней до конца месяца
            days_ostatok = days_in_month - days_last

            return days_in_month, days_last, days_ostatok
        self.days_in_month, self.days_last, self.days_ostatok = count_dey()

        # являится ли первым днем месяца
        def start_month(spis_VCHERA):
            new_month = any(datetime.datetime.strptime(date, '%Y-%m-%d').day == 1 for date in spis_VCHERA)
            if new_month:
                new_month = True
            else:
                new_month = False
            return new_month

        # ФОРМИРОВАНИЕ СПИСКА ВЧЕРАШНЕЙ ДАТЫ
        def Spis_vchera(date_now, last_day):
            VCHERA = []
            if is_workday(date_now):
                if is_workday(last_day):
                    priznzk = 'середина недели'
                    VCHERA.append(last_day.strftime('%Y-%m-%d'))
                else:
                    priznzk = "начало недели"
                    while not is_workday(last_day):
                        VCHERA.append(last_day.strftime('%Y-%m-%d'))
                        last_day -= datetime.timedelta(days=1)
                    VCHERA.append(last_day.strftime('%Y-%m-%d'))
            else:
                priznzk = "выходной день"
                VCHERA.append(last_day.strftime('%Y-%m-%d'))

            self.new_month = start_month(spis_VCHERA=VCHERA)

            return priznzk,VCHERA, self.new_month

        # узнаем список вчерашнего дня, является ли ервый день, и признак дня недели.
        priznzk,VCHERA,new_month = Spis_vchera(date_now=date_now,last_day=last_day)

        # Подготовка данных для первого дня меяца
        def New_mount(date_now):
            # Первый день текущего месяца
            start_day = date_now.replace(day=1)
            # Первый день прошлого месяца
            start_last_month = start_day - datetime.timedelta(days=1)
            start_last_month = start_last_month.replace(day=1)

            # Первый день позапрошлого месяца
            start_previous_month = start_last_month - datetime.timedelta(days=1)
            start_previous_month = start_previous_month.replace(day=1)

            # Последний день прошлого месяца
            end_last_month = start_day - datetime.timedelta(days=1)

            # список дат прошлого месяца
            self.new_month_todey = [str(start_last_month + datetime.timedelta(days=i)) for i in
                                    range((end_last_month - start_last_month).days + 1)]

            # список дат позапрошлого месяца
            self.new_month_last = [str(start_previous_month + datetime.timedelta(days=i)) for i in
                                             range((start_last_month - start_previous_month).days)]

            self.new_month_last_year = []
            for i in self.new_month_todey:
                i = i.replace('2023', '2022')
                self.new_month_last_year.append(i)

            return self.new_month_last_year, self.new_month_last, self.new_month_todey

        self.new_month_last_year, self.new_month_last, self.new_month_todey = New_mount(date_now)

class FLOAT:
    def float_colms(self, name_data, name_col):
        for i in name_col:
            name_data.loc[:, i] = (name_data[i].astype(str)
                                              .str.replace("\xa0", "")
                                              .str.replace(",", ".")
                                              .fillna(0)
                                              .astype("float")
                                              .round(2))
        return name_data
    """Для нескольких столбцов"""
    def float_colm(self, name_data, name_col):

        name_data.loc[:,  name_col] = (name_data[name_col].astype(str)
                                          .str.replace("\xa0", "")
                                          .str.replace(",", ".")
                                          .fillna(0)
                                          .astype("float")
                                          .round(2))
        return name_data
    """для одного столбца"""

class Tabl(BaseClass):
    def __init__(self):
        super().__init__()

        def Ty_spravochnik():
            try:
                print("Загрузка справочника магазинов...")
                ty = pd.read_excel(
                    "https://docs.google.com/spreadsheets/d/1qXyD0hr1sOzoMKvMyUBpfTXDwLkh0RwLcNLuiNbWmSM/export?exportFormat=xlsx")
                ty.to_excel(self.PUT + "Справочники\\Магазины\\Справочник ТТ.xlsx")

            except:
                print("Не удалось загрузить справочник магазинов, данные с пк")
                ty = pd.read_excel(self.PUT + "Справочники\\Магазины\\Справочник ТТ.xlsx")

            Ln_tip = {'Турова Анна Сергеевна': 'Турова А.С',
                      'Баранова Лариса Викторовна': 'Баранова Л.В',
                      'Геровский Иван Владимирович': 'Геровский И.В',
                      'Качалова Юлия Андреевна': 'Качалова Ю.',
                      'Павлова Анна Александровна': 'Павлова А.А',
                      'Вакансия': 'Вакансия',
                      'Сергеев Алексей Сергеевич': 'Сергеев А.С',
                      'Карпова Екатерина Эдуардовна': 'Карпова Е.Э'}

            ty["Менеджер"] = ty["Менеджер"].map(Ln_tip)
            ty = ty.rename(columns={"!МАГАЗИН!": "магазин"})
            ty_open_magaz = ty.loc[(ty["Старые/Новые"] == "Новые ТТ") |
                                   (ty["Старые/Новые"] == "Релокация") |
                                   (ty["Старые/Новые"] == "Без новых ТТ")]
            ty_open_magaz = ty_open_magaz[["магазин", "Менеджер"]]
            ty = ty[["магазин", "Менеджер"]]
            return ty, ty_open_magaz

        # Формирвание списка ТУ
        def ty(name_df):
            # доавление ТУ
            TY, ty_open_magaz = Ty_spravochnik()
            TY = TY.loc[TY["Менеджер"].notnull()]
            tabl = name_df.merge(TY, on=["магазин"], how="left").reset_index(drop=True)
            # создание списка ТУ
            ty_list = tabl['Менеджер'].unique().tolist()
            # удаление пустых значений и нан  списк ТУ
            ty_list = [value for value in ty_list if value and not isinstance(value, float)]
            return ty_list, tabl


        # загрзка таблиц, формирование списка ТУ
        self.tabl = pd.read_csv(self.PUT + "♀Вычисляемые_таблицы\\Нарастающие итоги.csv", sep="\t", encoding="utf-8",
                                parse_dates=['дата'], date_format='%Y-%m-%d',
                                dtype={'магазин': str, 'LFL': str}, low_memory=False)

        All_colms = list(set(self.tabl.columns) - {'магазин', 'LFL', 'дата'})
        FLOAT().float_colms(name_data=self.tabl, name_col=All_colms)
        self.ty_list, self.tabl = ty(name_df=self.tabl)

    def tabl_new_month(self):
        # позапрошлый месяц
        VCHERA_tabl = self.tabl[self.tabl['дата'].isin(self.new_month_last)]
        self.VCHERA_tabl = VCHERA_tabl.groupby(["магазин", "Менеджер"],
                                          as_index=False).agg(
            {"выручка": "sum", "Количество чеков": "sum", "дневной_план_выручка": "sum",
             "дневной_план_кол_чеков": "sum",
             "списания_оказатель": "sum", "списания_хозы": "sum"}) \
            .reset_index(drop=True)

        # Результаты за месяц
        TODEY_month_tabl = self.tabl[self.tabl['дата'].isin(self.new_month_todey)]
        self.TODEY_month_tabl = TODEY_month_tabl.groupby(["магазин", "Менеджер"], as_index=False).agg(
            {"выручка": "sum", "Количество чеков": "sum", "план_выручка": "mean",
             "план_кол_чеков": "mean", "план_cредний_чек": "mean",
             "списания_оказатель": "sum", "списания_хозы": "sum"}) \
            .reset_index(drop=True)

        # Результаты за прошлый год
        Last_year = self.tabl[self.tabl['дата'].isin(self.new_month_last_year)]
        self.Last_year = Last_year.groupby(["магазин"], as_index=False).agg(
            {"выручка": "sum", "Количество чеков": "sum",
             "списания_оказатель": "sum", "списания_хозы": "sum"}) \
            .reset_index(drop=True)
        self.Last_year = self.Last_year.rename(
            columns={"выручка": "выручка прошлый год", "Количество чеков": "Количество чеков, прошлый год",
                     "списания_оказатель": "списания_оказатель прошлый год",
                     "списания_хозы": "списания_хозы прошлый год"})

        return self.Last_year ,self.TODEY_month_tabl, self.VCHERA_tabl

class Messege_todey(BaseClass):
    def __init__(self):
        super().__init__()

    def bot_messege_todey(self):
        print("сообщение ботом дневное")

    def google_table_todey(self):
        print("Гугл таблица дневное")

class Messege_new_month(BaseClass):
    def __init__(self):
        super().__init__()

    def bot_messege_month(self):
        print("сообщение ботом месяц")

    def google_table_month(self):
        print("Гугл таблица месяц")
    def run(self):
        if self.new_month == True:

            self.Last_year, self.TODEY_month_tabl, self.VCHERA_tabl = Tabl().tabl_new_month()
            print(self.Last_year)
            print(self.TODEY_month_tabl)







if __name__ == '__main__':

    messege_month = Messege_new_month()
    messege_month.run()




