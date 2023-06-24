import holidays
import timeit
from datetime import datetime, timedelta, time, date
import datetime
import time as t
import os
import pandas as pd
import calendar
import gc
import requests
import json
from Bot_FRS_v2.INI import Float
from Bot_FRS_v2.GooGL_TBL import Google as g
from Bot_FRS_v2.INI import ini
from Bot_FRS_v2.INI import memory
from Bot_FRS_v2.INI import rename

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
class BOT:
    def bot_mes_html_TY(self, mes,silka, url=None):
        token = ini.token

        file_name = ""
        if TY_GROP == 1:
            # ключ группы ТУ
            chat_id = ini.TY_id
            if ini.time_seychas < ini.time_bot_vrem:
                file_name = "id_message_TY_last_day"
            else:
                file_name = "id_message_TY_day"

            def send_message(chat_id, text, token, reply_markup=None):
                url = f'https://api.telegram.org/bot{token}/sendMessage'
                data = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML', "disable_web_page_preview":True}
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
            buttons = [{"text": "Ссылка Google таблицу", "callback_data": "button1", "url": url}]
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
    def bot_mes_html(self, mes,silka,url=None):
        token = ini.token
        file_name = ""
        chat_id = ""
        if TEST_BOT == 1:
            # тестовая есть алексей
            chat_id = ini.test_all
            file_name = "id_message_test_all"
        if TEST_BOT == 2:
            # тестовая нет алексея
            chat_id = ini.test_not
            file_name = "id_message_test_not"
        if TEST_BOT == 000:
            return

        def send_message(chat_id, text, token, reply_markup=None):
            url = f'https://api.telegram.org/bot{token}/sendMessage'
            data = {'chat_id': chat_id,'text': text,'parse_mode': 'HTML',}
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
        buttons = [{"text": "Ссылка Google Docs(в разработке)", "callback_data": "button1", "url": url}]
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
        token = ini.token
        file_name = ""
        chat_id = ""
        if TY_GROP == 1 and priznak_grup == "TY":
            chat_id = ini.TY_id
            if ini.time_seychas < ini.time_bot_vrem:
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
class BOT_rashet():
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
        #print("Дата в файле\n", MAX_DATE)

        # тестовая
        test = 0
        if test ==1:
            MAX_DATE = datetime.datetime.strptime("2023-05-10", '%Y-%m-%d').date()
            LAST_DATE = MAX_DATE - datetime.timedelta(days=1)

        # region ФОРМИРОВАНИЕ СПИСКА ВЧЕРАШНЕЙ ДАТЫ
        priznzk = ""
        VCHERA= []
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
        #print("Прошлый день\n",VCHERA)
        # endregion

        # region ТЕКУШИЙ МЕСЯЦ
        TODEY_month_min_day = MAX_DATE.replace(day=1)
        # список дат
        TODEY_month = pd.date_range(start=TODEY_month_min_day, end=MAX_DATE  - datetime.timedelta(days=1), freq='D').strftime(format_date_str).tolist()
        #print("Текущий месяц\n",TODEY_month)
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
        #print("Прошлый месяц\n",LAST_month)

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

        return TODEY, VCHERA, TODEY_month, LAST_month, priznzk, new_month
    def rashet(self):
        # форматирование числа
        def format_chislo(i):
            format = '{:,.0f}'.format(i).replace(',', ' ')
            return format
        # фрматирование процента
        def format_prosent(i, ndigits):
            return "{:.{ndigits}%}".format(i, ndigits=ndigits)

        # Формирование списка дат
        TODEY, VCHERA, TODEY_month, LAST_month, priznzk, new_month = BOT_rashet().tabl_bot_date()
        # Преобразование формата даты
        TODEY= [datetime.datetime.strptime(date, '%d.%m.%Y').strftime('%Y-%m-%d') for date in TODEY]
        VCHERA = [datetime.datetime.strptime(date, '%d.%m.%Y').strftime('%Y-%m-%d') for date in  VCHERA]
        TODEY_month = [datetime.datetime.strptime(date, '%d.%m.%Y').strftime('%Y-%m-%d') for date in TODEY_month]
        LAST_month = [datetime.datetime.strptime(date, '%d.%m.%Y').strftime('%Y-%m-%d') for date in LAST_month]

        # загрзка таблиц, формирование списка ТУ
        tabl = pd.read_csv(PUT + "♀Вычисляемые_таблицы\\Нарастающие итоги.csv", sep="\t", encoding="utf-8",parse_dates=['дата'],date_format='%Y-%m-%d',dtype={'LFL': str})
        # доавление ТУ
        TY, ty_open_magaz = rename.RENAME().TY_Spravochnik()
        TY = TY.loc[TY["Менеджер"].notnull()]
        tabl = tabl.merge(TY, on=["магазин"], how="left").reset_index(drop=True)
        # создание списка ТУ
        ty_list = tabl['Менеджер'].unique().tolist()
        # удаление пустых значений и нан  списк ТУ
        ty_list = [value for value in ty_list if value and not isinstance(value, float)]
        print(ty_list)

        # отправка сообений вчерашнего дня.
        def vhera():
            VCHERA_tabl = tabl[tabl['дата'].isin(VCHERA)]
            TODEY_month_tabl = tabl[tabl['дата'].isin(TODEY_month)]
            print(TODEY_month_tabl)
            # ормирование соощение даты
            def __date():
                #VCHERA_mes = ['02.05.2023', '03.05.2023']
                VCHERA_date = ""
                kol_day = len(VCHERA)
                if kol_day == 1:
                    for date in VCHERA:
                        VCHERA_date = f'🕙 Результаты вчерашнего дня:\n'
                        VCHERA_date += f' •\u200E {date}\n'
                else:
                    min_date = min(VCHERA)
                    max_date = max(VCHERA)
                    VCHERA_date = f"🕙 Результаты за выходные:\n"
                    VCHERA_date += f" •{min_date} - {max_date}\n"
                print("Количество дней" , kol_day)
                return VCHERA_date

            for i in ty_list:
                print(i)
                # получение общех продаж и плана
                sales_total =  TODEY_month_tabl.loc[TODEY_month_tabl["Менеджер"] == i, "выручка"].sum()
                check_total = TODEY_month_tabl.loc[TODEY_month_tabl["Менеджер"] == i, "Количество чеков"].sum()

                TODEY_month_tabl_plan =  TODEY_month_tabl.groupby(["магазин", "Менеджер"],
                          as_index=False).agg(
                {"план_выручка": "mean", "план_кол_чеков": "mean"}) \
                .reset_index(drop=True)
                print(TODEY_month_tabl_plan)

                plan_sales_total =  TODEY_month_tabl_plan.loc[TODEY_month_tabl_plan["Менеджер"]
                                                              == i, "план_выручка"].sum()
                check_plan_total = TODEY_month_tabl_plan.loc[TODEY_month_tabl_plan["Менеджер"]
                                                             == i, "план_кол_чеков"].sum()

                # если план не выполнен
                def __not_end_mes_sales():
                    sales = VCHERA_tabl.loc[VCHERA_tabl["Менеджер"] == i, "выручка"].sum()
                    plan_day_sales = VCHERA_tabl.loc[VCHERA_tabl["Менеджер"] == i, "дневной_план_выручка"].sum()
                    plan_itog = sales / plan_day_sales
                    mes_sales = f'<b>👨‍💼{i}:</b>\n\n' \
                            f'{__date()}\n' \
                            f'<b>Выручка:\n</b>' \
                            f'• План(дневной): {format_chislo(i=plan_day_sales)}\n' \
                            f'• Факт: {format_chislo(i=sales)} ({format_prosent(i=plan_itog, ndigits=1)})\n'

                    plan_itog_total = sales_total / plan_sales_total
                    mes_sales_total = f'<b>\n📆 Результаты текущего месяца:\n</b>' \
                                        f'<b>Выручка:\n</b>' \
                                        f'• План(месяц): {format_chislo(i=plan_sales_total)}\n' \
                                        f'• Факт: {format_chislo(i=sales_total)} ({format_prosent(i=plan_itog_total, ndigits=1)})\n'

                    return  mes_sales, sales, plan_day_sales, mes_sales_total
                # если план выполнене
                def __end_mes_sales():
                    return mes_sales
                # план по кол чекам.
                def __not_end_mes_chek():
                    check = VCHERA_tabl.loc[VCHERA_tabl["Менеджер"] == i, "Количество чеков"].sum()
                    plan_check = VCHERA_tabl.loc[VCHERA_tabl["Менеджер"] == i, "дневной_план_кол_чеков"].sum()
                    plan_itog_check = check / plan_check
                    mes_chek = f'<b>Кол.чеков:\n</b>' \
                            f'• План(дневной): {format_chislo(i=plan_check)}\n' \
                            f'• Факт: {format_chislo(i=check)} ({format_prosent(i=plan_itog_check, ndigits=1)})\n'
                    return mes_chek,check,plan_check
                # если план выполнене
                def __end_mes_chek():
                    return  mes_chek
                # средний чек
                def aver_chek(sales,plan_day_sales, check,plan_check):
                    plan_aver_check =  plan_day_sales / plan_check
                    aver_check = sales/check
                    plan_itog_aver_check = aver_check/plan_aver_check
                    mes_aver_chek = f'<b>Средний чек:\n</b>' \
                               f'• План(дневной): {format_chislo(i=plan_aver_check)}\n' \
                               f'• Факт: {format_chislo(i=aver_check)} ({format_prosent(i=plan_itog_aver_check, ndigits=1)})\n'
                    return mes_aver_chek
                # списания
                def __spisania(sales):
                    print(sales)
                    spis = VCHERA_tabl.loc[VCHERA_tabl["Менеджер"] == i, "списания_оказатель"].sum()
                    spisania_proc = spis/sales
                    spis_total = TODEY_month_tabl.loc[TODEY_month_tabl["Менеджер"] == i, "списания_оказатель"].sum()

                    hoz = VCHERA_tabl.loc[VCHERA_tabl["Менеджер"] == i, "списания_хозы"].sum()
                    spisania_proc_hoz = hoz / sales

                    hz_total = TODEY_month_tabl.loc[TODEY_month_tabl["Менеджер"] == i, "списания_хозы"].sum()

                    mes_spis = f'<b>Списания:\n</b>' \
                               f'• Показатель: {format_chislo(i=spis)} ({format_prosent(i=spisania_proc, ndigits=1)})\n' \
                               f'• Хозы: {format_chislo(i=hoz)} ({format_prosent(i=spisania_proc_hoz, ndigits=1)})\n'
                    mes_spis_total = f'<b>Списания:\n</b>' \
                               f'• Показатель: {format_chislo(i=spis)} ({format_prosent(i=spisania_proc, ndigits=1)})\n' \
                               f'• Хозы: {format_chislo(i=hoz)} ({format_prosent(i=spisania_proc_hoz, ndigits=1)})\n'
                    return mes_spis, mes_spis_total
                def __result_TODEY_month():
                    return
                # бновление таблицы гугл
                def Google():
                    tabl_googl_vchera = VCHERA_tabl.loc[VCHERA_tabl["Менеджер"] == i]
                    tabl_googl_vchera = tabl_googl_vchera[["дата","магазин",
                                               "выручка","план_выручка","дневной_план_выручка",
                                               "Количество чеков","план_кол_чеков","дневной_план_кол_чеков",
                                               "Средний чек","план_cредний_чек",
                                               "списания_оказатель","списания_хозы"]]

                    tabl_googl_vchera = tabl_googl_vchera.rename(columns={"дата":"Дата","магазин":'Магазин',
                                               "выручка":'Выручка Факт',"план_выручка":"Выручка План","дневной_план_выручка":"Выручка Дневной план ",
                                               "Количество чеков":"Кол.чеков","план_кол_чеков":"Кол.чеков план","дневной_план_кол_чеков":"Кол.чеков Дневной план",
                                               "Средний чек": "Средний чек","план_cредний_чек":"Средний чек план",
                                               "списания_оказатель":"Cписания","списания_хозы":"Хозы"})
                    tabl_googl_vchera = pd.concat([tabl_googl_vchera, pd.DataFrame(tabl_googl_vchera.sum(numeric_only=True), columns=['Итого']).T.assign(
                                        Магазин='ИТОГО')]).reset_index(drop=True)
                    tabl_googl_vchera["Дата"] = tabl_googl_vchera["Дата"].dt.strftime('%d.%m.%Y')
                    tabl_googl_vchera = tabl_googl_vchera.round(0)
                    tabl_googl_vchera.fillna('', inplace=True)

                    Goole_url = g.tbl().record(name=i, name_df=tabl_googl_vchera,
                                   sheet_name="Результаты прошлого дня")

                    return Goole_url


                # роверка на выполнение плана по выручке
                priznak_sales = ""
                if sales_total<plan_sales_total:
                    # действие если план ен выполнен
                    mes_sales, sales, plan_day_sales, mes_sales_total = __not_end_mes_sales()
                    priznak_sales = 1
                else:
                    # действие если план выполнен
                    mes_sales, sales, plan_day_sales, mes_sales_total = __end_mes_sales()
                    priznak_sales = 0

                # роверка на выполнение плана по количеств чеков
                priznak_chek = ""
                if check_total<check_plan_total:
                    # действие если план ен выполнен
                    mes_chek,check,plan_check = __not_end_mes_chek()
                    priznak_chek = 1
                else:
                    # действие если план выполнен
                    mes_chek,check,plan_check = __end_mes_chek()
                    priznak_chek = 0

                # вычисление среднего чека
                priznak_aver_chek = priznak_chek + priznak_sales
                # если не выполнены оба планоа по выручке и кол чекам
                if priznak_aver_chek == 2:
                    mes_aver_chek = aver_chek(sales=sales, plan_day_sales=plan_day_sales,
                                              check =check ,plan_check= plan_check)
                else:
                    mes_aver_chek = 0
                    #################################################### работать исключение

                mes_spis, mes_spis_total = __spisania(sales=sales)


                Goole_url = Google()
                #BOT().bot_mes_html(mes=mes_sales + mes_chek + mes_aver_chek + mes_spis +
                                       #mes_sales_total, silka=1 ,url = Goole_url)
                url = f'<a href={Goole_url}>Ссылка Google таблицу</a>'
                url = f'<code>&lt;a href="{Goole_url}"&gt;Перейти на Google&lt;/a&gt;</code>'
                url = f'<b>\n 📎 <a href="{Goole_url}">Ссылка Google таблицу</a></b>'
                BOT().bot_mes_html_TY(mes=mes_sales + mes_chek + mes_aver_chek + mes_spis +
                                       mes_sales_total + url , silka=0)

                """######### если дневной план по выручке не выполнен
                if sales < VCHERA_tabl.loc[VCHERA_tabl["Менеджер"] == i, "план_выручка"].sum():

                    sales = VCHERA_tabl.loc[VCHERA_tabl["Менеджер"] == i, "выручка"].sum()
                    plan_day_sales = VCHERA_tabl.loc[VCHERA_tabl["Менеджер"] == i, "дневной_план_выручка"].sum()
                    plan_itog = sales / plan_day_sales
                    sales_F = format_prosent(i=plan_itog, ndigits=1)
                    mes_1 = f'<b>👨‍💼{i}:</b>\n\n' \
                            f'{VCHERA_date}\n' \
                            f'<b>Выручка:\n</b>' \
                            f'• План(дневной): {format_chislo(i=plan_day_sales)}\n' \
                            f'• Факт: {format_chislo(i=sales)} ({sales_F})\n'
                # если дневной план по выручке выполнен
                else:
                    mes_1 = f'<b>👨‍💼{i}:</b>\n\n' \
                            f'{VCHERA_date}\n' \
                            f'<b>Выручка: план выполнен👍\n</b>' \
                            f'• Факт: {format_chislo(i=sales)}\n'
                check = VCHERA_tabl.loc[VCHERA_tabl["Менеджер"] == i, "Количество чеков"].sum()

                #########  если дневной план по количеству чеков не выполнен
                if check < VCHERA_tabl.loc[VCHERA_tabl["Менеджер"] == i, "план_кол_чеков"].sum():
                    plan_check = VCHERA_tabl.loc[VCHERA_tabl["Менеджер"] == i, "дневной_план_кол_чеков"].sum()
                    plan_itog_check = check / plan_check
                    mes_2 = f'<b>Кол.чеков:\n</b>' \
                            f'• План(дневной): {format_chislo(i=plan_check)}\n' \
                            f'• Факт: {format_chislo(i=check)} ({format_prosent(i=plan_itog_check, ndigits=1)})\n' \
                # если дневной план по количеству чеков выполнен
                else:
                    mes_2 = f'<b>Кол.чеков:\n</b>'\
                            f'<b>Кол.чеков: план выполнен👍\n</b>' \
                            f'• Факт: {format_chislo(i=check)}\n'"""

        priznzk = "начало недели"
        if priznzk == "начало недели" or priznzk == 'середина недели':
            vhera()

class bot_mesege:
    def __init__(self):

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
        TODEY, VCHERA, TODEY_month, LAST_month, priznzk, new_month = BOT_rashet().tabl_bot_date()
        # Преобразование формата даты
        self.VCHERA_mes = VCHERA.copy()
        self.TODEY = [datetime.datetime.strptime(date, '%d.%m.%Y').strftime('%Y-%m-%d') for date in TODEY]
        self.VCHERA = [datetime.datetime.strptime(date, '%d.%m.%Y').strftime('%Y-%m-%d') for date in VCHERA]
        self.TODEY_month = [datetime.datetime.strptime(date, '%d.%m.%Y').strftime('%Y-%m-%d') for date in TODEY_month]
        self.LAST_month = [datetime.datetime.strptime(date, '%d.%m.%Y').strftime('%Y-%m-%d') for date in LAST_month]

        # загрзка таблиц, формирование списка ТУ
        self.tabl = pd.read_csv(PUT + "♀Вычисляемые_таблицы\\Нарастающие итоги.csv", sep="\t", encoding="utf-8",
                           parse_dates=['дата'], date_format='%Y-%m-%d',
                           dtype={'магазин': str, 'LFL': str},low_memory=False)
        # Получение списка всех столбцов, исключая ['магазин', 'LFL', 'дата']

        All_colms = list(set(self.tabl.columns) - {'магазин', 'LFL', 'дата'})
        print(All_colms)
        Float.FLOAT().float_colms(name_data=self.tabl,name_col=All_colms)
        self.ty_list, self.tabl = ty(name_df=self.tabl)

    def ff(self):
        print("Сегодняшняя дата: ", self.TODEY)
        print("Вчерашняя дата: ", self.VCHERA)
        print("Даты текущего месяца: ", self.TODEY_month)
        print("Даты прошлого месяца: ", self.LAST_month)
        print("Список территориалов: ", self.ty_list)

    def vchera(self):
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
            kol_day = len(self.VCHERA)
            if kol_day == 1:
                date = min(self.VCHERA)
                VCHERA_date = f'🕙 Результаты вчерашнего дня:\n'
                VCHERA_date += f' •\u200E {date}\n'
            else:
                min_date = min(self.VCHERA)
                max_date = max(self.VCHERA)
                VCHERA_date = f"🕙 Результаты за выходные:\n"
                VCHERA_date += f" •{min_date} - {max_date}\n"
            return VCHERA_date
        # результаты за вчера
        VCHERA_tabl = self.tabl[self.tabl['дата'].isin(self.VCHERA)]
        print(VCHERA_tabl)
        VCHERA_tabl  = VCHERA_tabl.groupby(["магазин", "Менеджер"],
                                                    as_index=False).agg(
                                {"выручка": "sum", "Количество чеков": "sum", "дневной_план_выручка": "sum",
                                 "дневной_план_кол_чеков": "sum",
                                 "списания_оказатель":"sum","списания_хозы":"sum"}) \
                                .reset_index(drop=True)

        # Результаты за месяц
        TODEY_month_tabl = self.tabl[self.tabl['дата'].isin(self.TODEY_month)]
        # Плыны сгрупированные
        TODEY_month_tabl = TODEY_month_tabl.groupby(["магазин", "Менеджер"],
                                                              as_index=False).agg(
                                {"выручка":"sum","Количество чеков":"sum","план_выручка": "mean",
                                 "план_кол_чеков": "mean","план_cредний_чек":"mean",
                                 "списания_оказатель":"sum","списания_хозы":"sum"}) \
                                .reset_index(drop=True)

        for i in self.ty_list:
            t.sleep(1)
            # выруча за месяц
            manager_data_total = TODEY_month_tabl.loc[TODEY_month_tabl["Менеджер"] == i]
            sales_total = manager_data_total["выручка"].sum()
            sales_total_plan = manager_data_total["план_выручка"].sum()
            sales_total_itog = sales_total / sales_total_plan
            # чеки  за месяц
            check_total = manager_data_total["Количество чеков"].sum()
            check_total_plan = manager_data_total["план_кол_чеков"].sum()
            check_total_itog = check_total/ check_total_plan
            # Средний чек  за месяц
            aver_chek_total = sales_total/check_total
            aver_chek_total_plan = manager_data_total["план_cредний_чек"].mean()
            aver_chek_total_itog =aver_chek_total/aver_chek_total_plan
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
                    mes_sales = f'<b> 👨‍💼 {i}:</b>\n\n' \
                                     f' {__date()}\n' \
                                     f'<b>Выручка:\n</b>' \
                                     f'• План(дневной): {fn(i=plan_sales_day)}\n' \
                                     f'• Факт: {fn(i=sales_day)} ({fp(i=plan_sales_itog, ndigits=1)})\n'
                else:
                    mes_sales = f'<b> 👨‍💼 {i}:</b>\n\n' \
                                     f' {__date()}\n' \
                                     f'<b>Выручка:\n</b>' \
                                     f'• План(дневной): "Выполнен"\n'


                mes_sales_total = f'<b>\n📆 Результаты текущего месяца: \n</b>' \
                                  f'<b>Выручка:\n</b>' \
                                  f'• План(месяц): {fn(i=sales_total_plan)}\n' \
                                  f'• Факт: {fn(i=sales_total)} ({fp(i=sales_total_itog, ndigits=1)})\n'

                return  mes_sales, mes_sales_total

            # формирование сообщений чеки
            def __check():
                s = 0
                if check_total<check_total_plan:
                    s = check_total_plan - check_total
                    print(f'{i} - "До плана" {fn(s)}')
                    mes_check = f'<b>Кол.чеков:\n</b>' \
                                     f'• План(дневной): {fn(i=plan_check_day)}\n' \
                                     f'• Факт: {fn(i=check_day)} ({fp(i=plan_check_itog, ndigits=1)})\n'
                else:
                    mes_check = f'<b>Кол.чеков:\n</b>' \
                                     f'• План(дневной): "Выполнен"\n'\

                mes_check_total = f'<b>Кол.чеков:\n</b>' \
                                  f'• План(месяц): {fn(i=check_total_plan)}\n' \
                                  f'• Факт: {fn(i=check_total)} ({fp(i=check_total_itog, ndigits=1)})\n'

                return  mes_check, mes_check_total

            # формирование сообщений средний чек
            def aver_chek():
                s = 0
                if check_total < check_total_plan:
                    s = check_total_plan - check_total
                    print(f'{i} - "До плана" {fn(s)}')
                    mes_aver_chek = f'<b>Средний чек:\n</b>' \
                                f'• План(дневной): {fn(i=aver_chek_plan_day)}\n' \
                                f'• Факт: {fn(i=aver_chek_day)} ({fp(i=aver_chek_itog_day, ndigits=1)})\n'
                else:
                    mes_aver_chek = f'<b>Средний чек:\n</b>' \
                                    f'• План(дневной): "Выполнен"\n'

                mes_aver_chek_total = f'<b>Средний чек:\n</b>' \
                                      f'• План(месяц): {fn(i=aver_chek_total_plan)}\n' \
                                      f'• Факт: {fn(i=aver_chek_total)} ({fp(i=aver_chek_total_itog, ndigits=1)})\n'

                return mes_aver_chek, mes_aver_chek_total

            # формирование сообщений списания
            def spisania():
                signal_spisania = ""
                print(spis_day_total_itog)
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
            BOT().bot_mes_html_TY(mes=mes_sales + mes_check+ mes_aver_chek + mes_spisania_day +
                                      mes_sales_total+mes_check_total + mes_aver_chek_total + mes_spisania_total ,silka=0)











#BOT_rashet().rashet()
bot_mesege = bot_mesege()
bot_mesege.ff()
bot_mesege.vchera()

