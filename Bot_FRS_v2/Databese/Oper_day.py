import sys
sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON\venv\Lib\site-packages")
sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON")
from Bot_FRS_v2.INI import ini
import datetime
import locale
import os
from sistem.conect import dostup
import pandas as pd
from sqlalchemy import create_engine
import gc



# инициализация
class BaseClass:
    def __init__(self):
        print("запус обновления с базы данных")
        dostu = dostup()
        dostu.size()
        self.password, self.user, self.database_set_operday, self.database_set_loyal, self.database_set, \
            self.port, self.host, self.history, self.klient, self.balans, self.balans_uniun = dostu.read()
        self.put= r'C:\Users\Lebedevvv\Desktop\FRS\Dashbord_new'
        self.put_client = "P:\\Фирменная розница\\ФРС\\Данные из 1 С\\☼ База данных SetReteyl\\Справочник_Клиентов\\База_клиентов.csv"

        # путь сохранения чеков сторно
        self.put_storno_sales = r"P:\Фирменная розница\ФРС\Данные из SetRetail\Cторно\Чеки_Обьедененные"
        #self.put_storno = r"P:\Фирменная розница\ФРС\Данные из SetRetail\Cторно\Чеки_сторно"

        # путь сохранения лояльности
        self.put_loyal_total = r"P:\Фирменная розница\ФРС\Данные из SetRetail\Лояльность\Чеки с номенклатурой"
        self.put_loyal = r"P:\Фирменная розница\ФРС\Данные из SetRetail\Лояльность\Чеки без номенклатуры"
        # путь сохранения базы клиентов
        self.put_loyal_klient =  r"P:\Фирменная розница\ФРС\Данные из SetRetail\Лояльность\Клиенты\База_клиентов.csv"


        # название базы данных операцонный день
        self.database_name1 = 1
        # название базы данных вся база
        self.database_name2 = 2
        # название базы данных база лояльности
        self.database_name3 = 3

# сохранение файлов
class save_data():
    def save(self, put,date,df):
        date_obj = date
        date_obj = datetime.datetime.strptime(date_obj, "%Y-%m-%d").date()

        year = str(date_obj.year)  # Получение года в виде строки
        old_locale = locale.getlocale(locale.LC_TIME)
        locale.setlocale(locale.LC_TIME, 'ru_RU')
        # Получить текущий месяц и год в формате строки
        month = date_obj.strftime('%B')
        # вернуть локаль
        locale.setlocale(locale.LC_TIME, old_locale)

        base_dir = put

        # Сочетание года и месяца в одной строке, разделенной символом '/'
        year_month_dir = os.path.join(base_dir, f"{year}\\{month}\\")

        # Проверка наличия папки года-месяца и создание при необходимости
        if not os.path.exists(year_month_dir):
            os.makedirs(year_month_dir)
        df.to_csv(year_month_dir + f"{str(date)}.csv", index=False)

# запрос к базе данных
class Database(BaseClass):
    def __init__(self, database_name=None):
        super().__init__()
        if database_name == 1:
            self.database_name = self.database_set_operday
        if database_name == 2:
            self.database_name = self.database_set
        if database_name == 3:
            self.database_name = self.database_set_loyal
        else:
            pass
        self.password = self.password
        self.user = self.user
        self.port = self.port
        self.host = self.host
        self.engine = None

    def __enter__(self):
        db_url = f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database_name}'
        self.engine = create_engine(db_url)
        print("Соединение успешно установлено")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.engine:
            self.engine.dispose()
            print("Соединение закрыто")

# обработка
class obrabotka(BaseClass):
    def __init__(self, database_instance):
        super().__init__()
        self.database_instance = database_instance

    # деление
    def sum(self, df, col_name, delen):
        df[col_name] = df[col_name] / delen
        print(col_name, delen)
        return df

    # запрос к базе данных - продажи
    def od_position(self, date):
        query = f"""
                SELECT 
                    p.id AS id_Чек, 
                    p.datecommit AS "Дата/Время чека", 
                    p.id_shift, 
                    p.numberfield AS Чек,
                    p.checkstatus AS Статус, 
                    p.checksumend AS "Сумма чека", 
                    p.operationtype AS Тип, 
                    p.discountvaluetotal AS "Сумма скидки чека", 
                    p.hasloytransaction AS "Признак лояльности",
                    s.id AS shift_id,
                    s.id_sessionstart AS "id_сессии",
                    s.operday, 
                    s.shopindex AS Магазин, 
                    s.numshift AS Смена, 
                    s.cashnum AS Касса,
                    pos.id AS position_id,
                    pos.qnty AS Количество,
                    pos.number_in_original AS "при отмене",
                    pos.numberfield AS "№ п/п в чеке",
                    pos.sumfield AS "Стоимость позиции",
                    pos.sumdiscount AS "Сумма скидки",
                    pos.datecommit AS "Время позиции",
                    prod.name AS "Наименование товара",
                    prod.item AS "Код товара",
                    ss.id_user AS "id_касира",
                    use.firstname,
                    use.lastname
                FROM od_position pos
                LEFT JOIN od_purchase p ON p.id = pos.id_purchase
                LEFT JOIN od_shift s  ON p.id_shift = s.id
                LEFT JOIN od_session AS ss ON s.id_sessionstart = ss.id
                LEFT JOIN od_user AS use ON  ss.id_user = use.tabnum  AND ss.shopnum = use.shop
                LEFT JOIN od_product prod ON pos.product_hash = prod.hash
                WHERE p.datecommit >= '{date} 00:00:00.000000' AND p.datecommit <= '{date} 23:59:59.999999'
                ORDER BY p.id DESC;
            """
        print("переданная дата" , date)
        od_position = pd.read_sql_query(query, self.database_instance.engine)
        # переименование типов
        status = {True: "Продажа", False: "Возврат"}
        od_position['Тип'] = od_position['Тип'].map(status)
        # переименование Статусов
        status = {0: "Зарегистрирован", 1: "Аннулирован", 2: "Отложен", 3: "Нефискальный"}
        od_position["Статус"] = od_position["Статус"].map(status)
        # перевод в рубли или килограммы
        col_list = ["Стоимость позиции", "Сумма скидки","Сумма скидки чека", "Сумма чека", "Количество"]
        for i in col_list:
            d = 100
            if i == "Было" or i == "Стало" or i == "Количество":
                d = 1000
            obrabotka(database_instance=None).sum(df=od_position, col_name=i, delen=d)
        # если возврат то отнять
        maska = od_position["Тип"] == "Возврат"
        od_position.loc[maska, "Стоимость позиции"] = od_position["Стоимость позиции"] * -1

        df_chek = od_position.loc[(od_position["Статус"] == 'Зарегистрирован')]

        df_id_chek_total = od_position["id_Чек"].unique().tolist()
        del od_position
        gc.collect()
        # список чеков
        df_id_chek = df_chek["id_Чек"].unique().tolist()

        # справочник магазинов
        def spr():
            print("Загрузка справочника магазинов...")
            df = pd.read_excel(
                "https://docs.google.com/spreadsheets/d/1qXyD0hr1sOzoMKvMyUBpfTXDwLkh0RwLcNLuiNbWmSM/export?exportFormat=xlsx")
            sp = df.loc[df["Работают или нет"] == "Действующие"]
            sp = sp["ID"].unique().tolist()
            df_sp = df[["!МАГАЗИН!", "ID"]]
            return sp, df_sp

        sp, df_sp = spr()
        # выбрать только магазины фрс
        df_chek = df_chek.loc[df_chek["Магазин"].isin(sp)]
        # добавить столбец с название магазинов
        df_chek = pd.merge(df_chek, df_sp, left_on="Магазин", right_on="ID", how="left")

        del sp,df_sp
        gc.collect()

        df_chek = df_chek.drop(columns=["ID"])
        # убрать тестовую кассу
        df_chek = df_chek.loc[
            ~((df_chek["Магазин"] == 42002) & (df_chek["Касса"] == 4))]

        # убрать подарочные карты
        PODAROK = ["Подарочная карта КМ 500р+ конверт", "Подарочная карта КМ 1000р+ конверт",
                   "подарочная карта КМ 500 НОВАЯ",
                   "подарочная карта КМ 1000 НОВАЯ"]
        df_chek = df_chek[~df_chek['Наименование товара'].isin(PODAROK)]
        # добавление id чека
        df_chek["id_chek"] = date + \
                             df_chek["Магазин"].astype(str) + \
                             df_chek["Смена"].astype(str) + \
                             df_chek["Касса"].astype(str) + \
                             df_chek["Чек"].astype(str)
        df_chek["id_chek"] = df_chek["id_chek"].str.split(".", expand=True)[0]


        df_chek = df_chek[["Тип", "Дата/Время чека", "Магазин", "Смена", "Касса", "Чек",
                           "Сумма чека", "Сумма скидки чека", "Время позиции", "Код товара",
                           "Наименование товара",
                           "Количество", "Стоимость позиции", "Сумма скидки", "id_chek", "!МАГАЗИН!"]]

        # Преобразовываем столбец 'Дата/Время' в нужный формат
        print(df_chek)
        df_chek["Дата/Время чека"] = pd.to_datetime(df_chek["Дата/Время чека"], format='%Y-%m-%d %H:%M:%S').dt.strftime('%d.%m.%Y %H:%M:%S')
        df_chek["Время позиции"] = pd.to_datetime(df_chek["Время позиции"], format='%Y-%m-%d %H:%M:%S').dt.strftime(
            '%d.%m.%Y %H:%M:%S')
        print(df_chek)
        print(f"Сумма продаж {date}: \n - {df_chek['Стоимость позиции'].sum():,.0f}".replace(',', ' '))

        return df_chek, df_id_chek

def run_new_data():
    def spisok_dat():
        # region СПИСОК ДАТ
        today = datetime.datetime.now()
        d_str = datetime.datetime.now().strftime('%d.%m.%Y')
        tame_Filter = today.strftime("%H:%M:%S")
        #spisok_d = [datetime.datetime.now().strftime('%d.%m.%Y')]
        # сохранение файла с датой обновления
        with open(ini.PUT + 'NEW\\дата обновления.txt', 'w') as f:
            f.write(str(today))

        # Текущее дата и время #############################
        dat_seychas = datetime.date.today()
        date_seychas = dat_seychas.strftime("%Y-%m-%d")
        time_seychas = datetime.datetime.now()
        time_seychas = time_seychas.strftime("%H:%M:%S")
        month_todey = datetime.datetime.now().month

        if tame_Filter < ini.time_bot_vrem:
            day_1 = today - datetime.timedelta(days=1)
            spisok_d = day_1.strftime('%d.%m.%Y')


            try:
                os.remove(ini.PUT + "♀Чеки\\Чеки текущий день\\" + str(spisok_d)+ ".csv" )
                os.remove(ini.PUT + "♀Продажи\\текущий день\\" + str(spisok_d) + ".csv")
            except:
                print("нет файлов")
            df1 = pd.DataFrame(columns=['!МАГАЗИН!','ID',"Наименование товара","Код товара","Стоимость позиции","Количество","Сумма скидки","номенклатура_1с","Дата/Время чека"])
            df2 = pd.DataFrame(columns=['ID', '!МАГАЗИН!', "выручка", "количество товаров в чеке", "количество уникальных товаров в чеке", "Средний чек",
                 "дата", "Количество чеков_возврат", "Количество чеков"])

            df1.to_csv(ini.PUT + "♀Продажи\\текущий день\\" + d_str + ".csv", encoding="utf-8",
                                      sep=';', index=False,
                                      decimal=",")
            df2.to_csv(ini.PUT + "♀Чеки\\Чеки текущий день\\" +  d_str + ".csv", encoding="utf-8",
                                  sep=';', index=False,
                                  decimal=",")
            spisok_d = [day_1.strftime('%d.%m.%Y')]
            print(spisok_d)
            print(df1)
            print(df2)
        else:
            spisok_d = [datetime.datetime.now().strftime('%d.%m.%Y')]
            # day_2 = today - timedelta(days=2)
            # date_poz_vchera = day_2.strftime('%d.%m.%Y')
            # spisok_d.append(date_poz_vchera)
        """start_date = date(2023, 1, 1)  # начальная дата
        end_date = date(2023, 5, 12)  # конечная дата
        delta = timedelta(days=1)  # шаг даты
    
        dates_list = []
        while start_date < end_date:
            # # преобразование даты в строку в формате 'день.месяц.год' и добавление её в список
            dates_list.append(start_date.strftime('%d.%m.%Y'))
            start_date += delta
            spisok_d = dates_list"""
        #spisok_d = ['12.06.2023']
        #spisok_d = ['01.10.2023','02.10.2023','03.10.2023','04.10.2023','05.10.2023','06.10.2023','07.10.2023','08.10.2023']
        # Преобразование дат в формат '%Y-%m-%d' с помощью генератора списка
        spisok_d = [datetime.datetime.strptime(date, '%d.%m.%Y').strftime('%Y-%m-%d') for date in spisok_d]

        print(spisok_d)
        return spisok_d
    spisok_d = spisok_dat()

    for i in spisok_d:
        # получение чеков
        def _сhek(i):
            database_name = 1
            with Database(database_name) as db1:
                # запрос к бд
                obrabotka_database_set_operday = obrabotka(db1)
                df_chek, df_id_chek = obrabotka_database_set_operday.od_position(i)

                d = str(df_chek['Дата/Время чека'][1])
                #d = d[0:10]
                #d = datetime.datetime.strptime(d, "%Y-%m-%d").strftime("%d.%m.%Y")
                new_filename = d[0:10] + ".xlsx"
                df_chek.to_excel(ini.PUT+ "Selenium\\Оригинальные файлы\\" + new_filename, index=False)
                df_chek.to_excel(r"P:\Фирменная розница\ФРС\Данные из SetRetail\Чеки вся сеть" + "\\"+ new_filename, index=False)
                del df_chek
                gc.collect()
                return
        _сhek(i)
    return

#run_new_data()
