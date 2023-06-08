import holidays
from datetime import datetime, timedelta, time, date
import datetime
import time as t
import os
import pandas as pd
import calendar
import gc
import requests
from Bot_FRS_.inf import memory as memory
from Bot_FRS_.inf import NASTROYKA as setting
import json
pd.set_option("expand_frame_repr", False)
pd.set_option('display.max_colwidth', None)

TY_GROP = 1 # setting.TY_GROP
TEST_BOT = 000 #setting.TEST_BOT
PUT = setting.PUT


class CustomRusHolidays(holidays.RU):
    def _populate(self, year,):
        super()._populate(year)
        # Добавляем в наш пользовательский набор праздников все официальные выходные дни.
        self[date(year, 5, 6)] = "День Воинской славы России"
        self[date(year, 5, 7)] = "День Воинской славы России"
        self[date(year, 5, 8)] = "День Победы"
        self[date(year, 5, 9)] = "День Победы"
        # Коректировка выходных дней
class RENAME:
    def Rread(self, name_data, name_col, name):
        print("Загрузка справочника магазинов...")
        while True:
            try:
                replacements = pd.read_excel("https://docs.google.com/spreadsheets/d/1SfuC2zKUFt6PQOYhB8EEivRjy4Dz-o4WDL-IR7CT3Eg/export?exportFormat=xlsx")
                """replacements = pd.read_excel(PUT + "Справочники\\ДЛЯ ЗАМЕНЫ.xlsx",
                                                 sheet_name="Лист1")"""
                rng = len(replacements)
                for i in range(rng):
                    name_data[name_col] = name_data[name_col].replace(replacements["НАЙТИ"][i], replacements["ЗАМЕНИТЬ"][i], regex=False)
                break
            except:
                print("Произошла ошибка при загрузке справочника магазинов. Повторяем попытку...")
        return name_data
    """функция переименование"""
    def magazin_info(self):
        print("Загрузка справочника магазинов...")
        while True:
            try:
                spqr = pd.read_excel("https://docs.google.com/spreadsheets/d/1qXyD0hr1sOzoMKvMyUBpfTXDwLkh0RwLcNLuiNbWmSM/export?exportFormat=xlsx")
                spqr = spqr[['ID', '!МАГАЗИН!']]
                break
            except:
                print("Произошла ошибка при загрузке справочника магазинов. Повторяем попытку...")
        return spqr
    """функция магазины для мердж"""

    def TY(self):
        # загрузка файла справочника териториалов
        ty = pd.read_excel("https://docs.google.com/spreadsheets/d/1rwsBEeK_dLdpJOAXanwtspRF21Z3kWDvruani53JpRY/export?exportFormat=xlsx")

        ty = ty[["Название 1 С (для фин реза)", "Менеджер"]]
        RENAME().Rread(name_data = ty, name_col= "Название 1 С (для фин реза)", name="TY")
        ty = ty.rename(columns={"Название 1 С (для фин реза)": "!МАГАЗИН!"})
        return ty

    def TY_Spravochnik(self):
        ty = pd.read_excel("https://docs.google.com/spreadsheets/d/1qXyD0hr1sOzoMKvMyUBpfTXDwLkh0RwLcNLuiNbWmSM/export?exportFormat=xlsx")
        ty = ty[["!МАГАЗИН!","Менеджер"]]
        Ln_tip = {'Турова Анна Сергеевна': 'Турова А.С',
                  'Баранова Лариса Викторовна': 'Баранова Л.В',
                  'Геровский Иван Владимирович': 'Геровский И.В',
                  'Изотов Вадим Валентинович': 'Изотов В.В',
                  'Томск': 'Томск',
                  'Павлова Анна Александровна': 'Павлова А.А',
                  'Бедарева Наталья Геннадьевна': 'Бедарева Н.Г',
                  'Сергеев Алексей Сергеевич': 'Сергеев А.С',
                  'Карпова Екатерина Эдуардовна': 'Карпова Е.Э'}
        ty["Менеджер"] = ty["Менеджер"].map(Ln_tip)

        #ty  = ty .rename(columns={"!МАГАЗИН!": "магазин"})
        return ty
        # переименование магазинов справочник ТУ
class FLOAT:
    def float_colms(self, name_data, name_col):
        for i in name_col:
            name_data[i] = (name_data[i].astype(str)
                                              .str.replace("\xa0", "")
                                              .str.replace(",", ".")
                                              .fillna("0")
                                              .astype("float")
                                              .round(2))
        return name_data
    """Для нескольких столбцов"""
    def float_colm(self, name_data, name_col):

        name_data[name_col] = (name_data[name_col].astype(str)
                                          .str.replace("\xa0", "")
                                          .str.replace(",", ".")
                                          .fillna("0")
                                          .astype("float")
                                          .round(2))
        return name_data
    """для одного столбца"""
        # перевод в число
class BOT:
    def bot_mes_html_TY(self, mes,silka):
        token = setting.token
        # ключ группы ТУ
        chat_id = setting.TY_id
        file_name = ""
        if TY_GROP == 1:
            if setting.time_seychas < setting.time_bot_vrem:
                file_name = "id_message_TY_last_day"
            else:
                file_name = "id_message_TY_day"

            def send_message(chat_id, text, token, reply_markup=None):
                url = f'https://api.telegram.org/bot{token}/sendMessage'
                data = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
                if reply_markup:
                    data['reply_markup'] = json.dumps(reply_markup, ensure_ascii=False)
                response = requests.post(url, json=data)
                if response.status_code == 200:
                    print('Сообщение отправлено')
                    return response.json().get('result', {}).get('message_id')
                else:
                    print(f'Ошибка при отправке сообщения: {response.status_code}')

            def save_message_id(message_id):
                with open(PUT + 'BOT\\Temp\\ID_messege\\' + file_name + '.txt', 'a') as file:
                    file.write(str(message_id) + '\n')
                with open(PUT + 'BOT\\Temp\\ID_messege\\' + file_name + '_ALL.txt', 'a') as file:
                    file.write(str(message_id) + '\n')
            buttons = [{"text": "Ссылка Google Docs(в разраотке)", "callback_data": "button1", "url": "https://kalina-malina.ru/", "color": "614051"}]
            reply_markup = {"inline_keyboard": [[button] for button in buttons]}
            # фильтр прикрепления ссылок
            if silka == 1:
                message_id = send_message(chat_id, mes, token, reply_markup)
            else:
                message_id = send_message(chat_id, mes, token)

            # Сохранение идентификатора сообщения в файл
            if message_id is not None:
                save_message_id(message_id)
    """отправка сообщений d в формате HTML в группу Т"""

    def bot_mes_html(self, mes,silka):
        token = setting.token
        file_name = ""
        chat_id = ""
        if TEST_BOT == 1:
            # тестовая есть алексей
            chat_id = setting.test_all
            file_name = "id_message_test_all"
        if TEST_BOT == 2:
            # тестовая нет алексея
            chat_id = setting.test_not
            file_name = "id_message_test_not"
        if TEST_BOT == 000:
            return

        def send_message(chat_id, text, token, reply_markup=None):
            url = f'https://api.telegram.org/bot{token}/sendMessage'
            data = {'chat_id': chat_id,'text': text,'parse_mode': 'HTML'}
            if reply_markup:
                data['reply_markup'] = json.dumps(reply_markup, ensure_ascii=False)
            response = requests.post(url, json=data)
            if response.status_code == 200:
                print('Сообщение отправлено')
                return response.json().get('result', {}).get('message_id')
            else:
                print(f'Ошибка при отправке сообщения: {response.status_code}')
                return None
        def save_message_id(message_id):
            with open(PUT + 'BOT\\Temp\\ID_messege\\' + file_name + '.txt', 'a') as file:
                file.write(str(message_id) + '\n')
        buttons = [{"text": "Ссылка Google Docs(в разраотке)", "callback_data": "button1", "url": "https://kalina-malina.ru/","color": "614051"}]
        reply_markup = {"inline_keyboard": [[button] for button in buttons]}
        # фильтр прикрепления ссылок
        if silka == 1:
            message_id = send_message(chat_id, mes, token, reply_markup)
        else:
            message_id = send_message(chat_id, mes, token)

        # Сохранение айд сообщения
        if message_id is not None:
            save_message_id(message_id)
    """отправка сообщений в формате HTML себе"""
    def del_lost(self, priznak_grup):
        token = setting.token
        file_name = ""
        chat_id = ""
        if TY_GROP == 1 and priznak_grup == "TY":
            chat_id = setting.TY_id
            if setting.time_seychas < setting.time_bot_vrem:
                # сообщения на начало дня
                file_name= "id_message_TY_last_day"
                # если это начало дня то дозаписыать в файл дневные сообщения прошлого дня
                with open(PUT + 'BOT\\Temp\\ID_messege\\id_message_TY_last_day.txt', 'a') as file1:
                    with open(PUT + 'BOT\\Temp\\ID_messege\\id_message_TY_day.txt', 'r') as file2:
                        file1.write(file2.read())
            else:
                # сообщения в течении дня
                file_name = "id_message_TY_day"
        if TY_GROP != 1 and priznak_grup == "TY":
            # если передан другой признак или отключен ТУ
            return
        # чтение файлов с айди сообщениями в зависимости от условия
        with open(PUT + 'BOT\\Temp\\ID_messege\\' + file_name + '.txt', 'r') as file:
            message_ids = file.read().splitlines()
        print(message_ids)
        if not message_ids:
            print("прервано")
            return  # Если список пуст, прерываем выполнение функции

        # список сообений не удаленных
        updated_message_ids = []
        for message_id in message_ids:
            delete_url = f'https://api.telegram.org/bot{token}/deleteMessage'
            try:
                delete_data = {'chat_id': chat_id, 'message_id': int(message_id)}
                delete_response = requests.post(delete_url, data=delete_data)
                if delete_response.status_code == 200:
                    print(f'Сообщение с идентификатором {message_id} удалено')
                else:
                    print(f'Ошибка при удалении сообщения {message_id}: {delete_response.status_code}')
            except:
                # Если удаление сообщения не удалось, оставляем его в списке
                updated_message_ids.append(message_id)


        # обновление файла с айди сообщений
        with open(PUT + "BOT\\Temp\\ID_messege\\" + file_name + ".txt", 'w') as file:
            file.write('\n'.join(updated_message_ids))

# отправка сообщений
class BOT_raschet:
    def tabl_bot_date(self):
        # определение рабочего дня или выходного
        def is_workday(date):
            ru_holidays = CustomRusHolidays()
            if date.weekday() >= 5:  # Если это суббота или воскресенье, то это выходной день.
                return False
            elif date in ru_holidays:  # Если это праздничный день, то это выходной день.
                return False
            else:
                return True  # Иначе это рабочий день.
        def save_date(date_list,name):
            with open(PUT + "BOT\\Temp\\даты_файлов\\" + name + '.txt', 'w') as f:
                f.write(str(date_list))

        # Чтение даты из файла
        with open(PUT + 'NEW\\дата обновления.txt', 'r') as f:
            date_str = f.readline().strip()
        format_date_str = '%d.%m.%Y'
        # тестовая дата скрыть ели боевой режим
        #date_str = "2023-05-10 10:00:36.001115"
        # Дата обновления
        MAX_DATE = datetime.datetime.strptime(date_str[:10], '%Y-%m-%d').date()
        TODEY = [MAX_DATE.strftime(format_date_str)]
        LAST_DATE = MAX_DATE - datetime.timedelta(days=1)
        print("Дата в файле\n",TODEY)
        print("Дата в файле\n", LAST_DATE)

        # тестовая
        test = 0
        if test ==1:
            MAX_DATE = datetime.datetime.strptime("2023-05-10", '%Y-%m-%d').date()
            LAST_DATE = MAX_DATE - datetime.timedelta(days=1)

        # region ФОРМИРОВАНИЕ СПИСКА ВЧЕРАШНЕЙ ДАТЫ
        priznzk = ""
        VCHERA= []
        if is_workday(MAX_DATE):
            priznzk = "рабочий день"
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
        print("Прошлый день\n",VCHERA)
        # endregion

        # region ТЕКУШИЙ МЕСЯЦ
        # Определяем первый день текущего месяца
        TODEY_month_min_day = MAX_DATE.replace(day=1)
        # список дат
        TODEY_month = pd.date_range(start=TODEY_month_min_day, end=MAX_DATE  - datetime.timedelta(days=1), freq='D').strftime(format_date_str).tolist()
        print("Текущий месяц\n",TODEY_month)
        # endregion

        # region ПРОШЛЫЙ МЕСЯЦ
        LAST_month_min_day = TODEY_month_min_day - pd.offsets.MonthBegin(1)
        # Определяем последний день прошлого месяца
        LAST_month_max_day = TODEY_month_min_day - pd.offsets.Day(1)
        # Создаем список дат прошлого месяца
        LAST_month = pd.date_range(start=LAST_month_min_day, end=LAST_month_max_day, freq='D').strftime(format_date_str).tolist()

        # Определяем количество дней в каждом месяце
        days_in_today_month = len(TODEY_month)
        days_in_last_month = len(LAST_month)
        # Если количество дней в прошлом месяце больше, отфильтруем его, чтобы было равное количество дней
        if days_in_last_month > days_in_today_month:
            LAST_month = LAST_month[:days_in_today_month]
        print("Прошлый месяц\n",LAST_month)

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
        save_date(TODEY,"TODEY")
        save_date(VCHERA,"VCHERA")
        save_date(TODEY_month,"TODEY_month")
        save_date(LAST_month,"LAST_month")
        save_date(new_month, "new_month")
        return TODEY, VCHERA, TODEY_month, LAST_month, priznzk
    # формирование списка дат
    def tabl_bot_file(self):
        TODEY, VCHERA, TODEY_month, LAST_month, priznzk = BOT_raschet().tabl_bot_date()
        Bot_temp = pd.DataFrame()
        def date():
            # Преобразование строки в datetime
            prognoz_date = TODEY[0]
            date = datetime.datetime.strptime(prognoz_date, '%d.%m.%Y').date()

            # Количество дней в месяце
            month_day_total = calendar.monthrange(date.year, date.month)[1]

            # Прошедших дней с начала месяца
            day_last = date.day - 1

            # Оставшихся дней в месяце
            day_ostatok = month_day_total - date.day + 1

            print("Дней в месяце:", month_day_total)
            print("Прошло дней:", day_last)
            print("Осталось дней:", day_ostatok)

            return month_day_total,day_last,day_ostatok
            # вычисление оставшихся и будуюих дней продаж
        # вычисление дат, оставшихся прошедших дней
        def col_n(x):
            FLOAT().float_colm(name_data=x, name_col="Сумма")
            x.loc[x["Аналитика хозяйственной операции"] == "Дегустации", "Дегустации"] = x["Сумма"]
            x.loc[x["Аналитика хозяйственной операции"] == "Хозяйственные товары", "Хозяйственные товары"] = x["Сумма"]
            x.loc[(x["Аналитика хозяйственной операции"] == "Кражи")
                    | (x["Аналитика хозяйственной операции"] == "ПОТЕРИ")
                    | (x["Аналитика хозяйственной операции"] == "Питание сотрудников")
                    | (x["Аналитика хозяйственной операции"] == "Подарок покупателю (сервисная фишка)")
                    | (x["Аналитика хозяйственной операции"] == "Подарок покупателю (бонусы)")
                    | (x["Аналитика хозяйственной операции"] == "Дегустации")
                    | (x["Аналитика хозяйственной операции"] == "МАРКЕТИНГ (блогеры, фотосессии)"), "Списания_показатель"] = x["Сумма"]
            return x
        # формирование столбцов списания
        def poisk_sales(file):
            file_p = file + '.xlsx'
            folder1 = PUT + "♀Продажи\\текущий месяц\\"
            folder2 = PUT + "♀Продажи\\2023\\"
            folder3 = PUT + "♀Продажи\\текущий день\\"
            for folder in [folder1, folder2, folder3]:

                file_path = os.path.join(folder, file_p)
                if os.path.exists(file_path):
                    x = pd.read_excel(file_path, parse_dates=["Дата/Время чека"], date_format='%Y-%m-%d %H:%M:%S')
                    y = x[["Дата/Время чека","!МАГАЗИН!","номенклатура_1с","Стоимость позиции","Сумма скидки"]]
                    del x
                    gc.collect()
                    # перименование столбцов
                    y = y.rename(columns={"!МАГАЗИН!":"магазин","номенклатура_1с":"номенклатура",
                                          "Стоимость позиции":"выручка","Сумма скидки":"скидка","Дата/Время чека":"дата"})

                    # перевод во float
                    len_float = ["выручка","скидка"]
                    FLOAT().float_colms(name_data=y,name_col=len_float)
                    # групировка таблицы
                    y= y.groupby(["магазин","номенклатура","дата"],
                                  as_index=False).agg(
                        {"выручка": "sum", "скидка": "sum"}).reset_index(drop=True)
                    return y
            # не ипользуется, для товара дня
        # поиск продаж(для номенклатуры)
        def poisk_check(file):
            file_p = file + '.xlsx'
            folder1 = PUT + "♀Чеки\\2023\\"
            folder2 = PUT + "♀Чеки\\Чеки текущий день\\"
            for folder in [folder1, folder2]:
                file_path = os.path.join(folder, file_p)
                if os.path.exists(file_path):
                    x = pd.read_excel(file_path, parse_dates=["дата"], date_format='%Y-%m-%d %H:%M:%S')
                    y = x[["дата", "!МАГАЗИН!","выручка","Количество чеков"]]
                    del x
                    gc.collect()
                    # перименование столбцов
                    y = y.rename(columns={"Количество чеков":"количество чеков"})
                    FLOAT().float_colm(name_data=y, name_col= "количество чеков")
                    y['месяц'] = pd.to_datetime(y['дата']).dt.month
                    return y
            # продажи и чеки
        # поиск данных о продажах и чеках
        def poisk_spisania(file):
            file_p = file + '.txt'
            folder1 = PUT + "♀Списания\\Текущий месяц\\"
            folder2 = PUT + "♀Списания\\История\\"
            for folder in [folder1, folder2]:

                file_path = os.path.join(folder, file_p)
                if os.path.exists(file_path):
                    x = pd.read_csv(file_path,sep="\t", encoding="utf-8",parse_dates=["дата"], date_format='%Y-%m-%d')

                    y = x[["дата","!МАГАЗИН!", "Аналитика хозяйственной операции", "Сумма","отбор"]]
                    del x
                    gc.collect()
                    # перименование столбцов
                    #y = y.rename(columns={"!МАГАЗИН!": "магазин", "номенклатура_1с": "номенклатура"})

                    col_n(y)
                    # перевод во float
                    #len_float = ["Дегустации", "Хозяйственные товары","Списания_показатель"]
                    #FLOAT().float_colms(name_data=y, name_col=len_float)
                    # групировка таблицы
                    y = y.groupby(["!МАГАЗИН!"],
                                  as_index=False).agg(
                        {"Дегустации": "sum", "Хозяйственные товары": "sum", "Списания_показатель" : "sum"}).reset_index(drop=True)

                    return y
            # списания
        # поиск списания
        def plan_month():
            # загрузка планов
            x = pd.read_excel(PUT + "♀Планы\\Планы ДЛЯ ДАШБОРДА.xlsx",parse_dates=["дата"], date_format='%d.%m.%Y')
            x = x[["!МАГАЗИН!", "ПЛАН", "дата","Показатель"]]
            FLOAT().float_colm(name_data=x, name_col="ПЛАН")
            x["месяц"] = pd.to_datetime(x["дата"]).dt.month
            x.loc[x["Показатель"] == "Выручка", "план_выручка"] = x["ПЛАН"]
            x.loc[x["Показатель"] == "Средний чек", "план_cредний_чек"] = x["ПЛАН"]
            x.loc[x["Показатель"] == "Кол чеков", "план_кол_чеков"] = x["ПЛАН"]
            x = x.drop(["ПЛАН", "Показатель","дата"], axis=1)
            x = x.groupby(["!МАГАЗИН!", "месяц"]).sum().reset_index()

            """sales_day = pd.merge(sales_day, sales_total, on=["!МАГАЗИН!", 'месяц'], how='left')

            sales_day = pd.merge(sales_day, x, on=["!МАГАЗИН!", 'месяц'], how='left')

            print(sales_day)
            # Рассчитываем дневной план
            sales_day["дневной_план_выручка"] = (sales_day["план_выручка"] - sales_day["выручка_за_текущий_месяц"]) / days_left
            sales_day["дневной_план_кол_чеков"] = (sales_day["план_кол_чеков"] -sales_day["чеков_за_текущий_месяц"]) /days_left
            #sales_day["дневной_cредний_чек"] = sales_day["дневной_план_выручка"] / sales_day["дневной_план_кол_чеков"]


            x.to_excel(PUT + "BOT\\temp\\" + "планы.xlsx", index=False)
            #x = x[["дата","!МАГАЗИН!","выручка","количество чеков","план_выручка","план_кол_чеков","план_cредний_чек","дневной_план_выручка","дневной_план_кол_чеков","дневной_cредний_чек"]]"""
            return x
        # поиск планов

        # region Сохранение временного файла с общими продажами за ткущий месяц
        for file in TODEY_month:

            x = poisk_check(file=str(file))
            Bot_temp = pd.concat([Bot_temp, x], axis=0, ).reset_index(drop=True)
        Bot_temp_Todey = Bot_temp.groupby(["!МАГАЗИН!", "месяц"],
                          as_index=False).agg(
            {"выручка": "sum", "количество чеков": "sum"}).reset_index(drop=True)
        Bot_temp_Todey.to_excel(PUT + "BOT\\temp\\" + "Выручка за месяц.xlsx", index=False)

        Bot_temp_nacpit = Bot_temp.groupby(["!МАГАЗИН!", "месяц", "дата"],
                                          as_index=False).agg(
            {"выручка": "sum", "количество чеков": "sum"}).reset_index(drop=True)

        # сортировка данных по магазинам, месяцам и датам
        Bot_temp_nacpit = Bot_temp_nacpit.sort_values(by=["!МАГАЗИН!", "месяц", "дата"])

        # расчет накопительной выручки и количества чеков по магазинам и месяцам
        Bot_temp_nacpit["накопительная выручка"] = Bot_temp_nacpit.groupby(
            ["!МАГАЗИН!", "месяц"])["выручка"].cumsum()
        Bot_temp_nacpit["накопительное количество чеков"] = Bot_temp_nacpit.groupby(
            ["!МАГАЗИН!", "месяц"])["количество чеков"].cumsum()
        Bot_temp_nacpit.to_excel(PUT + "BOT\\temp\\" + "Выручка за месяц_накопительный.xlsx", index=False)


        # endregion
        def todey():
            for file in TODEY:
                print("Формирование файла теущего дня: ", file)
                sales = poisk_check(file=str(file))
                total_sales_month = pd.read_excel(PUT + "BOT\\temp\\" + "Выручка за месяц.xlsx")

                total_sales_month = total_sales_month.rename(columns={"выручка": "выручка_total", "количество чеков": "чеков_total"})
                sales = pd.merge(sales, total_sales_month, on=["!МАГАЗИН!", 'месяц'], how='left')
                plan = plan_month()
                sales = pd.merge(sales, plan, on=["!МАГАЗИН!", 'месяц'], how='left')

                month_day_total, day_last, day_ostatok  = date()
                sales["дневной_план_выручка"] = (sales["план_выручка"] - sales["выручка_total"]) / day_ostatok
                sales["дневной_план_кол_чеков"] = (sales["план_кол_чеков"] - sales["чеков_total"]) / day_ostatok
                # sales_day["дневной_cредний_чек"] = sales_day["дневной_план_выручка"] / sales_day["дневной_план_кол_чеков"]
                sales   = sales.round()
                ty = RENAME().TY_Spravochnik()
                sales = sales.merge(ty, on=["!МАГАЗИН!"], how="left").reset_index(drop=True)
                sales = sales.drop([ "дата","месяц"], axis=1)

                sales.to_excel(PUT + "BOT\\Temp\\Файлы_данных_бота\\" + "TODEY.xlsx", index=False)

                del file,total_sales_month,month_day_total, day_last, day_ostatok,plan,ty
                gc.collect()
                memory.MEMORY().mem_total(x="TODEY")
            return
        todey()
        # формирование таблицы для текущего дня
        def vchera():
            vchera_conca = pd.DataFrame()
            for file in VCHERA:


                print("Формирование файла вчерашнего дня: ", file)
                sales = poisk_check(file=str(file))
                total_sales_month = pd.read_excel(PUT + "BOT\\temp\\" + "Выручка за месяц.xlsx")
                total_sales_month = total_sales_month.rename(columns={"выручка": "выручка_total", "количество чеков": "чеков_total"})
                sales = pd.merge(sales, total_sales_month, on=["!МАГАЗИН!", 'месяц'], how='left')
                plan = plan_month()
                sales = pd.merge(sales, plan, on=["!МАГАЗИН!", 'месяц'], how='left')
                # получение данных накопительного итога для расчета ещедневного плана для начала недели
                total_sales_nacop = pd.read_excel(PUT + "BOT\\temp\\" + "Выручка за месяц_накопительный.xlsx")
                # Преобразование строки в формат datetime
                file_dat = pd.to_datetime(file, format="%d.%m.%Y")
                total_sales_nacop = total_sales_nacop.loc[total_sales_nacop["дата"]==file_dat]
                sales = pd.merge(sales, total_sales_nacop[["!МАГАЗИН!", 'месяц',"накопительная выручка","накопительное количество чеков"]], on=["!МАГАЗИН!", 'месяц'], how='left')


                def date_ostak(file):
                    prognoz_date = file
                    date = datetime.datetime.strptime(prognoz_date, '%d.%m.%Y').date()
                    # Количество дней в месяце
                    month_day_total = calendar.monthrange(date.year, date.month)[1]

                    # Оставшихся дней в месяце
                    day_ostatok = month_day_total - date.day
                    print("остаток дней - ", day_ostatok )
                    return day_ostatok
                day_ostatok  = date_ostak(file=file)
                sales["дневной_план_выручка"] = (sales["план_выручка"] - sales["накопительная выручка"]) / day_ostatok
                sales["дневной_план_кол_чеков"] = (sales["план_кол_чеков"] - sales["накопительное количество чеков"]) / day_ostatok
                # sales_day["дневной_cредний_чек"] = sales_day["дневной_план_выручка"] / sales_day["дневной_план_кол_чеков"]
                sales = sales.drop(["накопительная выручка", "накопительное количество чеков"], axis=1)

                spisania = poisk_spisania(file)
                sales = sales.merge(spisania, on=["!МАГАЗИН!"], how="left").reset_index(drop=True)
                del spisania
                sales   = sales.round()
                ty = RENAME().TY_Spravochnik()
                sales = sales.merge(ty, on=["!МАГАЗИН!"], how="left").reset_index(drop=True)
                sales = sales.drop([ "дата","месяц"], axis=1)

                vchera_conca = pd.concat([vchera_conca, sales], axis=0, ).reset_index(drop=True)

                #vchera_conca.to_excel(PUT + "BOT\\Temp\\Файлы_данных_бота\\" + "VCHERA1.xlsx", index=False)

                del file,total_sales_month, day_ostatok,plan,ty
                gc.collect()
                memory.MEMORY().mem_total(x="VCHERA")
            vchera_conca = vchera_conca.groupby(["!МАГАЗИН!","Менеджер"],
                          as_index=False).agg(
                {"выручка": "sum", "количество чеков": "sum",
                 "выручка_total":"mean","чеков_total":"mean",
                 "план_выручка":"mean","план_cредний_чек":"mean",
                 "план_кол_чеков":"mean","дневной_план_выручка":"sum",
                 "дневной_план_кол_чеков":"sum","Дегустации":"sum",
                 "Хозяйственные товары":"sum","Списания_показатель":"sum"}).reset_index(drop=True)

            vchera_conca.to_excel(PUT + "BOT\\Temp\\Файлы_данных_бота\\" + "VCHERA.xlsx", index=False)
            return
        vchera()
        # формирование таблицы для вчерашнего дня и начала недели
        def todey_month():
            TODEY_month_conca = pd.DataFrame()
            for file in TODEY_month:
                print("Формирование файла текущего месяца: ", file)
                sales = poisk_check(file=str(file))
                total_sales_month = pd.read_excel(PUT + "BOT\\temp\\" + "Выручка за месяц.xlsx")
                total_sales_month = total_sales_month.rename(columns={"выручка": "выручка_total", "количество чеков": "чеков_total"})
                sales = pd.merge(sales, total_sales_month, on=["!МАГАЗИН!", 'месяц'], how='left')
                plan = plan_month()
                sales = pd.merge(sales, plan, on=["!МАГАЗИН!", 'месяц'], how='left')

                spisania = poisk_spisania(file)
                sales = sales.merge(spisania, on=["!МАГАЗИН!"], how="left").reset_index(drop=True)
                del spisania
                sales = sales.round()
                ty = RENAME().TY_Spravochnik()
                sales = sales.merge(ty, on=["!МАГАЗИН!"], how="left").reset_index(drop=True)
                sales = sales.drop(["дата", "месяц"], axis=1)

                TODEY_month_conca = pd.concat([TODEY_month_conca, sales], axis=0, ).reset_index(drop=True)

                #TODEY_month_conca.to_excel(PUT + "BOT\\Temp\\Файлы_данных_бота\\" + "TODEY_month1.xlsx", index=False)

                del file, total_sales_month, plan, ty
                gc.collect()
                memory.MEMORY().mem_total(x="TODEY_month")
            TODEY_month_conca = TODEY_month_conca.groupby(["!МАГАЗИН!", "Менеджер"],
                                                as_index=False).agg(
                {"выручка": "sum", "количество чеков": "sum",
                 "выручка_total": "mean", "чеков_total": "mean",
                 "план_выручка": "mean", "план_cредний_чек": "mean",
                 "план_кол_чеков": "mean", "Дегустации": "sum",
                 "Хозяйственные товары": "sum", "Списания_показатель": "sum"}).reset_index(drop=True)

            TODEY_month_conca.to_excel(PUT + "BOT\\Temp\\Файлы_данных_бота\\" + "TODEY_month.xlsx", index=False)

            return
        # формирование таблицы теущего  месяца
        todey_month()
        def last_month():
            LAST_month_conca = pd.DataFrame()
            for file in  LAST_month:
                print("Формирование файла прошлого: ", file)
                sales = poisk_check(file=str(file))
                total_sales_month = pd.read_excel(PUT + "BOT\\temp\\" + "Выручка за месяц.xlsx")
                total_sales_month = total_sales_month.rename(columns={"выручка": "выручка_total", "количество чеков": "чеков_total"})
                sales = pd.merge(sales, total_sales_month, on=["!МАГАЗИН!", 'месяц'], how='left')
                plan = plan_month()
                sales = pd.merge(sales, plan, on=["!МАГАЗИН!", 'месяц'], how='left')

                spisania = poisk_spisania(file)
                sales = sales.merge(spisania, on=["!МАГАЗИН!"], how="left").reset_index(drop=True)
                del spisania
                sales = sales.round()
                ty = RENAME().TY_Spravochnik()
                sales = sales.merge(ty, on=["!МАГАЗИН!"], how="left").reset_index(drop=True)
                sales = sales.drop(["дата", "месяц"], axis=1)

                LAST_month_conca = pd.concat([LAST_month_conca, sales], axis=0, ).reset_index(drop=True)

                #LAST_month_conca.to_excel(PUT + "BOT\\Temp\\Файлы_данных_бота\\" + "TODEY_month1.xlsx", index=False)

                del file, total_sales_month, plan, ty
                gc.collect()
                memory.MEMORY().mem_total(x="LAST_month")
            LAST_month_conca = LAST_month_conca.groupby(["!МАГАЗИН!", "Менеджер"],
                                                          as_index=False).agg(
                {"выручка": "sum", "количество чеков": "sum",
                 "выручка_total": "mean", "чеков_total": "mean",
                 "план_выручка": "mean", "план_cредний_чек": "mean",
                 "план_кол_чеков": "mean", "Дегустации": "sum",
                 "Хозяйственные товары": "sum", "Списания_показатель": "sum"}).reset_index(drop=True)

            LAST_month_conca.to_excel(PUT + "BOT\\Temp\\Файлы_данных_бота\\" + "LAST_month.xlsx", index=False)

            return
        last_month()
        # формирование таблицы прошлого месяца

        BOT_raschet().mes_bot()
    # Формирование таблиц на основе дат
    def mes_bot(self):
        # признак недели
        logic = setting.week_day
        # признак начала месяца
        new_month = setting.new_month
        def DATE():
            # Определение даты обновления дашборда
            """now = datetime.datetime.now()
            NEW_date = (now.hour + 1) if now.minute >= 30 else (now.hour)
            NEW_date = datetime.datetime(now.year, now.month, now.day, NEW_date, 0, 0)
            NEW_date = NEW_date.strftime("%H:%M")
            print("Текущее время (округлено до часа):", NEW_date)
            Seychas = f'🕙 Данные на : {NEW_date}\n'"""
            now = datetime.datetime.now()
            NEW_date = (now.hour + 1) if now.minute >= 30 else (now.hour)
            NEW_date = NEW_date % 24  # ограничения значения часа от 0 до 23
            NEW_date = datetime.datetime(now.year, now.month, now.day, NEW_date, 0, 0)
            NEW_date = NEW_date.strftime("%H:%M")
            print("Текущее время (округлено до часа):</b>", NEW_date)
            Seychas = f'<b>🕙 Данные на : {NEW_date}</b>\n'


            # список дат из файла TODEY_month
            with open(PUT + "Bot\\temp\\даты_файлов\\VCHERA.txt", 'r') as f:
                dates = f.read().strip()[1:-1].split(', ')

            # Формируем сообщение Вчерашнего дня
            VCHERA_date = f'🕙Результаты вчерашнего дня:\n'
            for date in dates:
                VCHERA_date += f' •\u200E {date[1:-1]}\n'
            print(VCHERA_date)


            # Формируем сообщение после выходных
            min_date = min(dates)[1:-1]
            max_date = max(dates)[1:-1]
            VCHERA_date_holidays = f"<b>🕙Результаты за выходные:</b>\n"
            VCHERA_date_holidays += f" •{min_date} - {max_date}\n"

            return VCHERA_date, Seychas, VCHERA_date_holidays
        # форирование сообщений заголовков даты и времени обновления
        def todey():
            VCHERA_date, Seychas, VCHERA_date_holidays = DATE()
            mes = f'{Seychas}'
            # заголовок сообщения с временем обновлений Времени получения данных
            BOT().bot_mes_html_TY(mes=mes,silka =0)
            # отправка сообщений в группу тест
            BOT().bot_mes_html(mes=mes,silka =0)

            def format_chislo(i):
                format =  '{:,.0f}'.format(i).replace(',', ' ')
                return format
            # фрматирование числа
            def format_prosent(i, ndigits):
                return "{:.{ndigits}%}".format(i, ndigits=ndigits)
            # форматирование процента


            todey_tabl = pd.read_excel(PUT + "BOT\\Temp\\Файлы_данных_бота\\TODEY.xlsx")
            ty_list = todey_tabl['Менеджер'].unique().tolist()
            for i in ty_list:
                print(i)
                sales = todey_tabl.loc[todey_tabl["Менеджер"] == i, "выручка"].sum()
                plan_day_sales = todey_tabl.loc[todey_tabl["Менеджер"] == i, "дневной_план_выручка"].sum()
                plan_itog = sales / plan_day_sales

                check = todey_tabl.loc[todey_tabl["Менеджер"] == i, "количество чеков"].sum()
                plan_check = todey_tabl.loc[todey_tabl["Менеджер"] == i, "дневной_план_кол_чеков"].sum()
                plan_itog_check = check / plan_check

                aver_chek = sales / check
                plan_aver_chek = plan_day_sales / plan_check
                plan_itog_aver_chek = aver_chek / plan_aver_chek

                mes = f'<b>👨‍💼{i}:</b>\n\n' \
                      f'<b>Выручка:\n</b>' \
                      f'• План(дневной): {format_chislo(i=plan_day_sales)}\n' \
                      f'• Факт: {format_chislo(i=sales)} ({format_prosent(i=plan_itog, ndigits=1)})\n' \
                      f'<b>Кол.чеков:\n</b>' \
                      f'• План(дневной): {format_chislo(i=plan_check)}\n' \
                      f'• Факт: {format_chislo(i=check)} ({format_prosent(i=plan_itog_check, ndigits=1)})\n' \
                      f'<b>Средний чек:\n</b>' \
                      f'• План(дневной): {format_chislo(i=plan_aver_chek)}\n ' \
                      f'• Факт: {format_chislo(i=aver_chek)} ({format_prosent(i=plan_itog_aver_chek, ndigits=1)})\n'

                t.sleep(setting.zaderjka)

                BOT().bot_mes_html(mes=mes,silka=1)
                BOT().bot_mes_html_TY(mes=mes,silka=1)
            del todey_tabl
            return mes
        # обработка сообщений за текущий день
        def vchera(priznak):
            VCHERA_date, Seychas, VCHERA_date_holidays = DATE()
            if priznak == "начало недели":
                priznak = VCHERA_date_holidays
            else:
                priznak = VCHERA_date

            def format_chislo(i):
                format =  '{:,.0f}'.format(i).replace(',', ' ')
                return format
            # фрматирование числа
            def format_prosent(i, ndigits):
                return "{:.{ndigits}%}".format(i, ndigits=ndigits)
            # форматирование процента
            #  ИТОГИ ПРОШЛОГО ДНЯ ИЛИ ДНЕЙ#################################################
            vcera_tabl = pd.read_excel(PUT + "BOT\\Temp\\Файлы_данных_бота\\VCHERA.xlsx")
            ty_list =  vcera_tabl['Менеджер'].unique().tolist()
            mount_todey_tabl = pd.read_excel(PUT + "BOT\\Temp\\Файлы_данных_бота\\TODEY_month.xlsx")
            mount_last_tabl = pd.read_excel(PUT + "BOT\\Temp\\Файлы_данных_бота\\LAST_month.xlsx")
            for i in ty_list:
                sales =  vcera_tabl.loc[ vcera_tabl["Менеджер"] == i, "выручка"].sum()
                plan_day_sales =  vcera_tabl.loc[ vcera_tabl["Менеджер"] == i, "дневной_план_выручка"].sum()
                plan_itog = sales / plan_day_sales

                check =  vcera_tabl.loc[ vcera_tabl["Менеджер"] == i, "количество чеков"].sum()
                plan_check =  vcera_tabl.loc[ vcera_tabl["Менеджер"] == i, "дневной_план_кол_чеков"].sum()
                plan_itog_check = check / plan_check

                aver_chek = sales / check
                plan_aver_chek = plan_day_sales / plan_check
                plan_itog_aver_chek = aver_chek / plan_aver_chek

                spisania = vcera_tabl.loc[vcera_tabl["Менеджер"] == i, "Списания_показатель"].sum()
                spisania_proc = spisania/ sales

                spisania_hoz = vcera_tabl.loc[vcera_tabl["Менеджер"] == i, "Хозяйственные товары"].sum()
                spisania_proc_hoz = spisania_hoz / sales

                spisania_deg = vcera_tabl.loc[vcera_tabl["Менеджер"] == i, "Дегустации"].sum()
                spisania_proc_deg  = spisania_hoz / sales


                #  ИТОГИ текущего месяца#################################################

                sales_mount_todey = mount_todey_tabl.loc[mount_todey_tabl["Менеджер"] == i, "выручка"].sum()
                plan_mount_todey = mount_todey_tabl.loc[mount_todey_tabl["Менеджер"] == i, "план_выручка"].sum()
                plan_itog_mount_todey = sales_mount_todey / plan_mount_todey

                check_mount_todey = mount_todey_tabl.loc[mount_todey_tabl["Менеджер"] == i, "количество чеков"].sum()
                plan_check_mount_todey = mount_todey_tabl.loc[mount_todey_tabl["Менеджер"] == i, "план_кол_чеков"].sum()
                plan_itog_check_mount_todey = check_mount_todey / plan_check_mount_todey

                aver_chek_mount_todey = sales_mount_todey / check_mount_todey
                plan_aver_chek_mount_todey = plan_mount_todey / plan_check_mount_todey
                plan_itog_aver_chek_mount_todey = aver_chek_mount_todey / plan_aver_chek_mount_todey

                spisania_mount_todey = mount_todey_tabl.loc[mount_todey_tabl["Менеджер"] == i, "Списания_показатель"].sum()
                spisania_proc_mount_todey = spisania_mount_todey / sales_mount_todey

                spisania_hoz_mount_todey = mount_todey_tabl.loc[mount_todey_tabl["Менеджер"] == i, "Хозяйственные товары"].sum()
                spisania_proc_hoz_mount_todey = spisania_hoz_mount_todey / sales_mount_todey

                spisania_deg_mount_todey = mount_todey_tabl.loc[mount_todey_tabl["Менеджер"] == i, "Дегустации"].sum()
                spisania_proc_deg_mount_todey = spisania_deg_mount_todey / sales_mount_todey



                mes = f'<b>👨‍💼{i}:</b>\n' \
                      f'{priznak}\n'\
                      f'<b>Выручка:\n</b>' \
                      f'• План(дневной): {format_chislo(i=plan_day_sales)}\n' \
                      f'• Факт: {format_chislo(i=sales)} ({format_prosent(i=plan_itog, ndigits=1)})\n' \
                      f'<b>Кол.чеков:\n</b>' \
                      f'• План(дневной): {format_chislo(i=plan_check)}\n' \
                      f'• Факт: {format_chislo(i=check)} ({format_prosent(i=plan_itog_check, ndigits=1)})\n' \
                      f'<b>Средний чек:\n</b>' \
                      f'• План(дневной): {format_chislo(i=plan_aver_chek)}\n' \
                      f'• Факт: {format_chislo(i=aver_chek)} ({format_prosent(i=plan_itog_aver_chek, ndigits=1)})\n' \
                      f'<b>Списания:\n</b>' \
                      f'• Показатель: {format_chislo(i=spisania)} ({format_prosent(i=spisania_proc, ndigits=1)})\n' \
                      f'• Хозы: {format_chislo(i=spisania_hoz)} ({format_prosent(i=spisania_proc_hoz, ndigits=1)})\n' \
                      f'• Дегустации: {format_chislo(i=spisania_deg)} ({format_prosent(i=spisania_proc_deg, ndigits=1)})\n\n' \
                      f'<b>📆 Результаты текущего месяца:\n</b>' \
                      f'<b>Выручка:\n</b>' \
                      f'• План(месяц): {format_chislo(i=plan_mount_todey)}\n' \
                      f'• Факт: {format_chislo(i=sales_mount_todey)} ({format_prosent(i=plan_itog_mount_todey, ndigits=1)})\n' \
                      f'• Прогноз: --- (---)\n' \
                      f'<b>Кол.чеков:\n</b>' \
                      f'• План(месяц): {format_chislo(i=plan_check_mount_todey)}\n' \
                      f'• Факт: {format_chislo(i=check_mount_todey)} ({format_prosent(i=plan_itog_check_mount_todey, ndigits=1)})\n'\
                      f'• Прогноз: --- (---)\n' \
                      f'<b>Средний чек:\n</b>' \
                      f'• План(месяц): {format_chislo(i=plan_aver_chek_mount_todey)}\n' \
                      f'• Факт: {format_chislo(i=aver_chek_mount_todey)} ({format_prosent(i=plan_itog_aver_chek_mount_todey, ndigits=1)})\n' \
                      f'• Прогноз: --- (---)\n' \
                      f'<b>Списания:\n</b>' \
                      f'• Показатель: {format_chislo(i=spisania_mount_todey)} ({format_prosent(i=spisania_proc_mount_todey, ndigits=1)})\n' \
                      f'• Хозы: {format_chislo(i=spisania_hoz_mount_todey)} ({format_prosent(i=spisania_proc_hoz_mount_todey, ndigits=1)})\n' \
                      f'• Дегустации: {format_chislo(i=spisania_deg_mount_todey)} ({format_prosent(i=spisania_proc_deg_mount_todey, ndigits=1)})\n'


                t.sleep(setting.zaderjka)
                BOT().bot_mes_html(mes=mes,silka =1)
                BOT().bot_mes_html_TY(mes=mes, silka =1)

            return
        # обработка сообщений за Вчерашний день
        if new_month=="нет":
            if setting.time_seychas < setting.time_bot_vrem:
                # фильтр фремени после которого меняются сообщение на дневные
                if logic == "начало недели":
                    # заголовок сообщения с датой обновлений получения данных за прошедшие выходные
                    t.sleep(setting.zaderjka)
                    # удаление сообщений из группы ту
                    BOT().del_lost(priznak_grup="TY")
                    vchera(priznak="начало недели")
                    print("начало недели")

                if logic == 'середина недели':
                    # задержка
                    t.sleep(setting.zaderjka)
                    # удаление сообщений из группы ту
                    BOT().del_lost(priznak_grup="TY")
                    vchera(priznak='середина недели')

                    print('середина недели')
                if logic == "выходной день":
                    VCHERA_date, Seychas,VCHERA_date_holidays = DATE()
                    mes = f'{VCHERA_date}'
                    # заголовок сообщения с датой обновлений получения данных
                    BOT().bot_mes_html(mes=mes,silka =0)
                    print( "выходной день")
            else:
                # ежедневные ообщения после 10 часов

                # задержка
                t.sleep(setting.zaderjka)
                # удаление сообщений из группы ту
                BOT().del_lost(priznak_grup="TY")
                todey()
                print("днеыные сообщения")
        else:
            print("первый день месяца")
        return

    def tovar_day(self):
        return
    # отвечает за товар дня
        # расчет для бота
# формирование сообщений

#BOT_raschet().mes_bot()
BOT_raschet().mes_bot()