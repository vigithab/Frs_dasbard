import shutil
import sys
sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON\venv\Lib\site-packages")
sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON")

from datetime import datetime, timedelta, time, date
import os
import pandas as pd
import gc
import datetime
import time
from Bot_FRS_v2.NEW_DATA.SET_SD import run_NEW_DATA_sd
from Bot_FRS_v2.BOT_TELEGRAM import BOT
from Bot_FRS_v2.NEW_DATA import SETRETEYL as set
from Bot_FRS_v2.INI import Float, log, rename, ini, memory
from Bot_FRS_v2.RASSILKA import Voropaev,count_tt,Storno
from Bot_FRS_v2.NEW_DATA import Personal_v2, Plan_2023, GRUP_FILE, SORT_FILE, Konvers,Reting

PUT = ini.PUT
class NEW_data:
    def Obrabotka(self):
        log.LOG().log_data()
        BOT.BOT().bot_mes_html(mes="Скрипт Дашборда запущен",silka=0)
        # Получение данных для персонала
        try:
            new_personal = Personal_v2.new_data()
            new_personal.tudey()
            log.LOG().log_new_data(name_txt="Персонал")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            mes = f"Ошибка при скачивании : {exc_type.__name__} на строке {exc_tb.tb_lineno}: {e}\n"
            log.LOG().log_new_data(name_txt="Персонал", e=mes)
            BOT.BOT().bot_mes_html(mes="Ошибка при Обновлении Персонал", silka=0)
        # Получение С сетевого диска
        try:
            run_NEW_DATA_sd()
            log.LOG().log_new_data(name_txt="Сетевой диск")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            mes = f"Ошибка при скачивании : {exc_type.__name__} на строке {exc_tb.tb_lineno}: {e}\n"
            log.LOG().log_new_data(name_txt="Сетевой диск", e=mes)
            BOT.BOT().bot_mes_html(mes="📛 Ошибка при получение данных с сетевого диска", silka=0)

        if ini.set_== 1:
            print("Будеть обновлены данные с сета")
            # Получение С СЕТРЕТЕЙЛА
            try:
                set.SET().Set_obrabotka()
                log.LOG().log_new_data(name_txt="Cетритеил")
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                mes = f"Ошибка при скачивании : {exc_type.__name__} на строке {exc_tb.tb_lineno}: {e}\n"
                log.LOG().log_new_data(name_txt="Ошибка Cетритеил", e=mes)
                BOT.BOT().bot_mes_html(mes=mes, silka=0)
        if ini.set_ != 1:
            BOT.BOT().bot_mes_html(mes="🟡 Нужно выбрать сколько фалов нужно обработать", silka=0)
            print("данные с сента обнгалены не будут, тресем историю")
            def copy_last_n_files(source_folder, destination_folder, n):
                files = [(os.path.join(source_folder, f), os.path.getctime(os.path.join(source_folder, f))) for f in
                         os.listdir(source_folder)]
                files.sort(key=lambda x: x[1])
                last_n_files = [f[0] for f in files[-n:]]
                for file in last_n_files:
                    shutil.copy(file, destination_folder)
            source_folder = ini.PUT +"\\Selenium\\исходники\\"
            destination_folder = ini.PUT + "Selenium\\Оригинальные файлы\\"
            count = 0
            for _, _, files in os.walk(source_folder):
                count += len(files)
            print(f"Файлов в базе: {count}")
            n = int(input(f"Сколько последних файлов обработать? ввести цифру: "))
            copy_last_n_files(source_folder, destination_folder, n)
            print(f"Скопировано последних {n} файлов:\nиз {source_folder}\nв {destination_folder}.")
        spqr, sprav_magaz, open_mag = rename.RENAME().magazin_info()

        for root, dirs, files in os.walk(PUT + "Selenium\\Оригинальные файлы\\"):
            # "PUT + "Selenium\\Оригинальные файлы\\"
            for file in files:
                if "2023" in file:
                    os.path.basename(file)
                    file_path = os.path.join(root, file)
                    print("Фаил: ", os.path.basename(file_path)[:-5], " / Начат: ",
                          str(datetime.datetime.now())[:-10], )
                    df = pd.read_excel(file_path)
                    if "Магазин 1C" in df.columns:
                        # удаление столбца "магазин"
                        df.drop("Магазин 1C", axis=1, inplace=True)
                    d = df['Дата/Время чека'][1]
                    new_filename = d[0:10] + ".xlsx"
                    df = df.rename(columns={"Магазин": 'ID'})
                    table = df.merge(spqr[['!МАГАЗИН!', 'ID']], on='ID', how="left")
                    del df
                    table = table.loc[table["Тип"].notnull()]
                    table['!МАГАЗИН!'] = table['!МАГАЗИН!'].astype("str")
                    table['Наименование товара'] = table['Наименование товара'].fillna("неизвестно").astype("str")

                    sales_day = table.copy()
                    # удаление микромаркетов
                    l_mag = ("Микромаркет", "Экопункт", "Вендинг", "Итого")
                    for w in l_mag:
                        sales_day = sales_day[~sales_day["!МАГАЗИН!"].str.contains(w)].reset_index(drop=True)

                    # удаление подарочных карт
                    PODAROK = ["Подарочная карта КМ 500р+ конверт", "Подарочная карта КМ 1000р+ конверт",
                               "подарочная карта КМ 500 НОВАЯ",
                               "подарочная карта КМ 1000 НОВАЯ"]
                    for x in PODAROK:
                        sales_day = sales_day.loc[sales_day["Наименование товара"] != x]

                    # обработка файла чеков
                    sales_day_cehk = NEW_data().selenium_day_chek(name_datafreme=sales_day,
                                                                  name_file=str(new_filename))

                    # сохранение Сгрупированного файла чеков
                    sales_day_cehk.to_csv(PUT + "♀Чеки\\2023\\" + new_filename[:-5] + ".csv", encoding="utf-8",
                                          sep=';',index=False,
                                          decimal=",")
                    try:
                        sales_day_cehk.to_csv("P:\\Фирменная розница\\ФРС\\Данные из 1 С\\Чеки_Сгруппированные_конверсия\\Чеки_сгруппированные\\2023\\"+
                                              new_filename[:-5] + ".csv", encoding="utf-8",
                                              sep=';', index=False,
                                              decimal=",")
                    except Exception as e:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        mes = f"Ошибка при : {exc_type.__name__} на строке {exc_tb.tb_lineno}: {e}\n"
                        log.LOG().log_new_data(name_txt="Файлы чеков паблик", e=mes)
                        BOT.BOT().bot_mes_html(mes="Ошибка при сохранении Файлы чеков паблик", silka=0)


                    # сохранение Сгрупированного файла продаж;
                    sales_day_sales = NEW_data().Set_sales(name_datafreme=sales_day, name_file=str(new_filename))
                    sales_day_sales.to_csv(PUT + "♀Продажи\\текущий месяц\\" + new_filename[:-5] + ".csv", encoding="utf-8",
                                          sep=';', index=False,
                                          decimal=",")

                    del sales_day_cehk
                    del sales_day
                    gc.collect()
                    # region СОХРАНЕНИЕ УДАЛЕННЫХ ДАННЫХ
                    # Сохранение отдельно вейдинги и микромаркеты
                    mask_VEN = table["!МАГАЗИН!"].str.contains("|".join(l_mag))
                    sales_day_VEN = table[mask_VEN]
                    sales_day_VEN.to_csv(PUT + "Selenium\\Вейдинги и микромаркет\\" + new_filename[:-5] + ".csv",
                                           encoding="utf-8",
                                           sep=';', index=False,
                                           decimal=",")

                    del sales_day_VEN
                    gc.collect()
                    # Сохранение отдельно подарочные карты
                    sales_day_Podarok = \
                        table.loc[(table["Наименование товара"] == "Подарочная карта КМ 500р+ конверт") |
                        (table["Наименование товара"] == "Подарочная карта КМ 1000р+ конверт") |
                        (table["Наименование товара"] == "подарочная карта КМ 500 НОВАЯ") |
                        (table["Наименование товара"] == "подарочная карта КМ 1000 НОВАЯ")]

                    sales_day_Podarok.to_csv(PUT + "Selenium\\Подарочные карты\\" + new_filename[:-5] + ".csv",
                                           encoding="utf-8",
                                           sep=';', index=False,
                                           decimal=",")
                    del sales_day_Podarok
                    gc.collect()
                    try:
                        # Сохранение отдельно анулированные и возвращенные чеки
                        sales_null = table.loc[(table["Тип"] == "Отмена") | (table["Тип"] == "Возврат")]
                        sales_null.to_csv(PUT + "Selenium\\Анулированные и возврат чеки\\" +
                                            new_filename[:-5] + ".csv",
                                             encoding="utf-8",
                                             sep=';', index=False,
                                             decimal=",")
                        del sales_null
                        gc.collect()
                    except:
                        print("Ошибка при сохранении анулированные и возвращенные чеки")

                    # Формирование Конверсии
                    try:
                        Konvers.konvers().selenium_day_chek(name_datafreme=table,name_file=str(new_filename) )
                        log.LOG().log_new_data(name_txt="Таблица Конверсии")
                    except Exception as e:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        mes = f"Ошибка при : {exc_type.__name__} на строке {exc_tb.tb_lineno}: {e}\n"
                        log.LOG().log_new_data(name_txt="Конверсии", e=mes)
                        BOT.BOT().bot_mes_html(mes="Ошибка при обработке Конверсии", silka=0)
        # обработка списания
        try:
            NEW_data().selenium_day_Spisania()
            log.LOG().log_new_data(name_txt="Обработка списания")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            mes = f"Ошибка при скачивании : {exc_type.__name__} на строке {exc_tb.tb_lineno}: {e}\n"
            log.LOG().log_new_data(name_txt="Обработка списания", e=mes)

            BOT.BOT().bot_mes_html(mes="Ошибка при обработке списания", silka=0)
        # обработка сибестоймости
        try:
            NEW_data().sebest()
            log.LOG().log_new_data(name_txt="Себестоемости")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            mes = f"Ошибка при скачивании : {exc_type.__name__} на строке {exc_tb.tb_lineno}: {e}\n"
            log.LOG().log_new_data(name_txt="Себестоемости", e=mes)
            BOT.BOT().bot_mes_html(mes="Ошибка при обработке Сбестоймости", silka=0)
        # обработка СОРТИРОВКА ФАЙЛОВ
        try:
            SORT_FILE.SORT().sort_files_sales()
            log.LOG().log_new_data(name_txt="Сортировка продаж")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            mes = f"Ошибка при скачивании : {exc_type.__name__} на строке {exc_tb.tb_lineno}: {e}\n"
            log.LOG().log_new_data(name_txt="Сортировка продаж", e=mes)
        try:
            SORT_FILE.SORT().sort_files_chek()
            log.LOG().log_new_data(name_txt="Сортировка чеков")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            mes = f"Ошибка при скачивании : {exc_type.__name__} на строке {exc_tb.tb_lineno}: {e}\n"
            log.LOG().log_new_data(name_txt="Сортировка чеков", e=mes)

        try:
            SORT_FILE.SORT().sort_files_spis()
            log.LOG().log_new_data(name_txt="Сортировка Списния")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            mes = f"Ошибка при скачивании : {exc_type.__name__} на строке {exc_tb.tb_lineno}: {e}\n"
            log.LOG().log_new_data(name_txt="Сортировка Списния", e=mes)

        try:
            SORT_FILE.SORT().sort_files_sebes()
            log.LOG().log_new_data(name_txt="Сортировка сибестоймости")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            mes = f"Ошибка при скачивании : {exc_type.__name__} на строке {exc_tb.tb_lineno}: {e}\n"
            log.LOG().log_new_data(name_txt="Сортировка сибестоймости", e=mes)

        try:
            SORT_FILE.SORT().original()
            log.LOG().log_new_data(name_txt="Сортировка исходников")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            mes = f"Ошибка при скачивании : {exc_type.__name__} на строке {exc_tb.tb_lineno}: {e}\n"
            log.LOG().log_new_data(name_txt="Сортировка сибестоймости", e=mes)

        # группировка файлов
        try:
            GRUP_FILE.Grup().grups()
            log.LOG().log_new_data(name_txt="Групировка файлов")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            mes = f"Ошибка при скачивании : {exc_type.__name__} на строке {exc_tb.tb_lineno}: {e}\n"
            log.LOG().log_new_data(name_txt="Групировка файлов", e=mes)
            BOT.BOT().bot_mes_html(mes="Ошибка Групировка файлов", silka=0)

        # перенос Ежедневного списания
        try:
            SORT_FILE.SORT().Ostatki_chas()
            log.LOG().log_new_data(name_txt="Перенос Ежедневного списания ДШ")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            mes = f"Ошибка при скачивании : {exc_type.__name__} на строке {exc_tb.tb_lineno}: {e}\n"
            log.LOG().log_new_data(name_txt="Перенос Ежедневного списания", e=mes)
            BOT.BOT().bot_mes_html(mes="Ошибка Перенос Ежедневного списания", silka=0)

        # перенос шашлычного сезона
        try:
            SORT_FILE.SORT().sashl_sezn()
            log.LOG().log_new_data(name_txt="Перенос шашлычного сезона")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            mes = f"Ошибка при скачивании : {exc_type.__name__} на строке {exc_tb.tb_lineno}: {e}\n"
            log.LOG().log_new_data(name_txt="Перенос шашлычного сезона", e=mes)
            BOT.BOT().bot_mes_html(mes="Ошибка Перенос шашлычного сезона", silka=0)

        # Формирование таблицы шашлыка
        try:
            Voropaev.Degustacia().sotka()
            log.LOG().log_new_data(name_txt="Гугл таблица шашлычный сезон")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            mes = f"Ошибка при скачивании : {exc_type.__name__} на строке {exc_tb.tb_lineno}: {e}\n"
            log.LOG().log_new_data(name_txt="Гугл таблица шашлычный сезон", e=mes)
            BOT.BOT().bot_mes_html(mes="Ошибка при обработке дегустации(ворп)", silka=0)

        # Формирование таблицы подсчета ТТ
        try:
            count_tt.tabl_count_tt().tabl_form()
            log.LOG().log_new_data(name_txt="Подсчет количества ТТ")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            mes = f"Ошибка при : {exc_type.__name__} на строке {exc_tb.tb_lineno}: {e}\n"
            log.LOG().log_new_data(name_txt="Подсчет количества ТТ", e=mes)
            BOT.BOT().bot_mes_html(mes="Ошибка при обработке Подсчет количества ТТ", silka=0)

        # Формирование Талицы планов
        try:
            Plan_2023.plan()
            log.LOG().log_new_data(name_txt="Таблица планов")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            mes = f"Ошибка при : {exc_type.__name__} на строке {exc_tb.tb_lineno}: {e}\n"
            log.LOG().log_new_data(name_txt="Таблица планов", e=mes)
            BOT.BOT().bot_mes_html(mes="Ошибка при обработке Таблица планов", silka=0)
        # Формирование таблиц рейтинга
        try:
            Reting.reting()
            log.LOG().log_new_data(name_txt="Таблица Рейтинга")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            mes = f"Ошибка при : {exc_type.__name__} на строке {exc_tb.tb_lineno}: {e}\n"
            log.LOG().log_new_data(name_txt="Таблица Рейтинга", e=mes)
            BOT.BOT().bot_mes_html(mes="Ошибка при обработке Таблица рейтингов", silka=0)

        BOT.BOT().bot_mes_html(mes="😃 Завершено успешно ☺️",silka=0)
        SORT_FILE.SORT().pysto_sales_month()
        SORT_FILE.SORT().pysto_sebes_month()
        with open(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON\Bot_FRS_v2\LOGI\log_new_data.txt", 'a',
                  encoding="utf-8") as file:
            file.write(f'**************************************************************************\n')
        print("завершено")
        time.sleep(240)
    # главная функция запускает все
    def Set_sales(self, name_datafreme, name_file):
        # групировка файлов продаж по дням
        def grup_sales(name_df, name_file):
            x = name_df
            ln = ["Стоимость позиции", "Количество", "Сумма скидки"]
            Float.FLOAT().float_colms(name_data=x, name_col=ln)
            do = x["Стоимость позиции"].sum()
            x = x.groupby(["!МАГАЗИН!", "ID", "Дата/Время чека"],
                          as_index=False).agg(
                {"Стоимость позиции": "sum", "Количество": "sum", "Сумма скидки": "sum"}) \
                .reset_index(drop=True)
            posslw = x["Стоимость позиции"].sum()
            # сохранение лога
            txt = f'Групировка выручка до - {do:.1f}, после - {posslw:.1f},' \
                  f' разница {(do - posslw):.1f}'
            log.LOG().log_obrabotka(mes=txt, priznak="Групировка Продажи", name_file=name_file)
            x = x.rename(columns={"!МАГАЗИН!": "магазин", "Стоимость позиции": "выручка",
                                  "Количество": "количество_продаж",
                                  "Сумма скидки": "скидка", "Дата/Время чека": "дата"})
            x = x[["дата", "ID", "магазин", "выручка", "количество_продаж", "скидка"]]
            x.to_csv(PUT + "♀Продажи\\Сгрупированные файлы по дням\\" +
                     str(os.path.basename(name_file)[:-5]) + ".csv", encoding="utf-8", sep='\t',
                     index=False,
                     decimal=",")
            return
        name_datafreme["Касса"] = name_datafreme["Касса"].astype(str)
        name_datafreme = name_datafreme.loc[~((name_datafreme["!МАГАЗИН!"] == "Таврическая 37") & (name_datafreme["Касса"] == "4.0"))]

        sales_day_sales = name_datafreme[
            ["ID", "!МАГАЗИН!", "Код товара", "Тип", "Наименование товара", "Количество", "Стоимость позиции",
             "Сумма скидки", "Штрихкод"]]
        sales_day_sales = sales_day_sales.loc[(sales_day_sales["Тип"] == "Продажа") | (sales_day_sales["Тип"] ==
                                                                                       "Возврат")]
        sales_day_sales = sales_day_sales.drop(["Тип"], axis=1)
        ln = ("Стоимость позиции", "Количество", "Сумма скидки")
        Float.FLOAT().float_colms(name_data=sales_day_sales, name_col=ln)
        sales_sum_do = sales_day_sales["Стоимость позиции"].sum()
        sales_day_sales = sales_day_sales[["ID", "!МАГАЗИН!", "Код товара", "Наименование товара", "Количество",
                                           "Стоимость позиции", "Сумма скидки"]]
        sales_day_sales = sales_day_sales.groupby(["!МАГАЗИН!", "ID", "Наименование товара", "Код товара"],
                                                  as_index=False) \
            .agg({"Стоимость позиции": "sum",
                  "Количество": "sum",
                  "Сумма скидки": "sum"}) \
            .sort_values("!МАГАЗИН!", ascending=False).reset_index(drop=True)
        sales_sum_posle = sales_day_sales["Стоимость позиции"].sum()
        txt = f'Выручка до - {sales_sum_do:.1f}, после - {sales_sum_posle:.1f},' \
              f' разница {(sales_sum_do - sales_sum_posle):.1f}'
        log.LOG().log_obrabotka(mes=txt, priznak="Продажи", name_file=name_file)
        # ######################################## Загузка названий с 1 с
        spravka_nom = pd.read_csv(PUT + "Справочники\\номенклатура\\Список.txt", sep="\t", encoding="utf-8")
        spravka_nom = spravka_nom.rename(columns={"Номенклатура": "номенклатура_1с", "Код SKU": "Код товара"})
        # единый формат столбца длясоеденения
        Float.FLOAT().float_colm(name_data=sales_day_sales, name_col="Код товара")
        sales_day_sales["Код товара"] = sales_day_sales["Код товара"].astype(int).astype(str)
        Float.FLOAT().float_colm(name_data=spravka_nom, name_col="Код товара")
        spravka_nom["Код товара"] = spravka_nom["Код товара"].astype(int).astype(str)

        sales_day_sales = sales_day_sales.merge(spravka_nom[['номенклатура_1с', "Код товара"]],
                                                on=["Код товара"], how="left").reset_index(drop=True)


        sales_day_sales_null = sales_day_sales.loc[sales_day_sales["номенклатура_1с"].isnull()]
        sales_day_sales_null = len(sales_day_sales_null)
        txt = f'📛 Номенклатура не найдено - {sales_day_sales_null} 📛'
        if sales_day_sales_null > 0:
            BOT.BOT().bot_mes_html(mes=txt, silka=0)
        else:
            txt = f'✅ Номенклатура не найдено - {sales_day_sales_null}'
            BOT.BOT().bot_mes_html(mes=txt, silka=0)
            txt = f'Номенклатура не найдено - {sales_day_sales_null}'
            print(txt)
            log.LOG().log_obrabotka(mes=txt, priznak="Номенклатура", name_file=name_file)
        del spravka_nom
        gc.collect()
        # название файл и даты ####################################################################
        sales_day_sales['filename'] = os.path.basename(name_file)[:-5]
        sales_day_sales = sales_day_sales.rename(columns={'filename': "Дата/Время чека"})
        sales_day_sales["Дата/Время чека"] = pd.to_datetime(sales_day_sales["Дата/Время чека"], format='%d.%m.%Y')
        grup_sales(sales_day_sales,name_file=name_file)
        BOT.BOT().bot_mes_html(mes="✅ Обработка продаж", silka=0)
        return sales_day_sales
    # обработка файлов продаж
    def selenium_day_chek(self, name_datafreme, name_file):
        memory.MEMORY().mem_total(x="Формирование чеков: ")
        name_datafreme["Касса"] = name_datafreme["Касса"].astype(str)
        name_datafreme = name_datafreme.loc[
            ~((name_datafreme["!МАГАЗИН!"] == "Таврическая 37") & (name_datafreme["Касса"] == "4.0"))]
        sp = ["Касса"]
        Float.FLOAT().float_colms(name_data=name_datafreme,name_col=sp)
        def cnevk(tip):
            sales_day_cehk = name_datafreme[["Тип","!МАГАЗИН!", "ID", "Дата/Время чека", "Касса", "Чек",
                                             "Стоимость позиции", "Код товара","Смена"]]
            if tip=="Продажа":
                sales_day_cehk = sales_day_cehk.loc[(sales_day_cehk["Тип"] == tip) | (sales_day_cehk["Тип"] ==
                                                                                      "Возврат")]
                sales_day_cehk = sales_day_cehk.drop(["Тип"], axis=1)
            else:
                sales_day_cehk = sales_day_cehk.loc[(sales_day_cehk["Тип"] == tip)]
                sales_day_cehk = sales_day_cehk.drop(["Тип"], axis=1)
            # время обновления
            set_check_date = sales_day_cehk["Дата/Время чека"].max()
            with open(PUT + "NEW\\DATE.txt", "w") as f:
                f.write(str(set_check_date))
            del set_check_date
            sales_day_cehk["Дата/Время чека"] = pd.to_datetime(sales_day_cehk["Дата/Время чека"],
                                                               format="%d.%m.%Y %H:%M:%S").dt.date
            # Формирование ID Чека
            sales_day_cehk["ID_Chek"] = sales_day_cehk["ID"].astype(int).astype(str) + \
                                        sales_day_cehk["Касса"].astype(int).astype(str) + \
                                        sales_day_cehk["Чек"].astype(int).astype(
                str) + sales_day_cehk["Дата/Время чека"].astype(str) + sales_day_cehk["Смена"].astype(str)

            sales_day_cehk = sales_day_cehk.drop(["Касса", "Чек","Смена"], axis=1)
            # удаление не нужных символов
            Float.FLOAT().float_colm(name_data=sales_day_cehk, name_col="Стоимость позиции")
            # Групировки по дням
            sales_day_cehk = sales_day_cehk.groupby(["!МАГАЗИН!", "ID", "Дата/Время чека", "ID_Chek"],
                                                    as_index=False).agg({
                "Стоимость позиции": "sum",
                "Код товара": [("Количество товаров в чеке", "count"), ("Количество уникальных товаров в чеке",
                                                                        "nunique")]})

            # переименовываем столбцы
            sales_day_cehk.columns = ['!МАГАЗИН!', "ID", 'Дата/Время чека', 'ID_Chek', 'Стоимость позиции',
                                      'Количество товаров в чеке',
                                 'Количество уникальных товаров в чеке']
            # выбираем нужные столбцы и сортируем по дате/времени чека в порядке убывания
            sales_day_cehk = sales_day_cehk[
                ["ID", '!МАГАЗИН!', 'Дата/Время чека', 'ID_Chek', 'Стоимость позиции', 'Количество товаров в чеке',
                 'Количество уникальных товаров в чеке']] \
                .sort_values('Дата/Время чека', ascending=False) \
                .reset_index(drop=True)
            # групировка по магазинам
            sales_day_cehk = sales_day_cehk.groupby(["ID", "!МАГАЗИН!", "Дата/Время чека"], as_index=False) \
                .agg({"Стоимость позиции": "sum",
                      'ID_Chek': "count",
                      "Количество товаров в чеке": "mean",
                      "Количество уникальных товаров в чеке": "mean"}) \
                .sort_values("Дата/Время чека", ascending=False).reset_index(drop=True)

            # дбавление среднего чека
            sales_day_cehk["Средний чек"] = sales_day_cehk["Стоимость позиции"] / sales_day_cehk["ID_Chek"]
            # переименование столбцов
            sales_day_cehk = sales_day_cehk.rename(columns=
                                                   { "Дата/Время чека": "дата",
                                                    "Стоимость позиции": "выручка",
                                                    "ID_Chek": "Количество чеков",
                                                    "Количество товаров в чеке": "количество товаров в чеке",
                                                    "Количество уникальных товаров в чеке": "количество уникальных товаров в чеке"})
            # округление
            sales_day_cehk= sales_day_cehk.round(2)
            sales_day_cehk['filename'] = os.path.basename(name_file)[:-5]
            sales_day_cehk = sales_day_cehk.drop(['дата'], axis=1)
            sales_day_cehk = sales_day_cehk.rename(columns={'filename': 'дата'})
            sales_day_cehk["дата"] = pd.to_datetime(sales_day_cehk["дата"], format='%d.%m.%Y')
            return sales_day_cehk

        sales_day_cehk = cnevk(tip="Продажа")
        sales_day_cehk = sales_day_cehk.rename(columns={"Количество чеков": "Количество чеков_продажа"})
        vozvrat = cnevk(tip="Возврат")
        vozvrat = vozvrat[["!МАГАЗИН!","Количество чеков","дата"]]
        vozvrat = vozvrat.rename(columns={"Количество чеков": "Количество чеков_возврат"})
        sales_day_cehk = sales_day_cehk.merge(vozvrat,
                                                on=["!МАГАЗИН!","дата"], how="left").reset_index(drop=True)

        sales_day_cehk["Количество чеков_возврат"] = sales_day_cehk["Количество чеков_возврат"].fillna(0)
        sales_day_cehk["Количество чеков"] = sales_day_cehk["Количество чеков_продажа"]
        sales_day_cehk = sales_day_cehk.drop(["Количество чеков_продажа"], axis=1)
        BOT.BOT().bot_mes_html(mes="✅ Обработка Чеков", silka=0)
        return sales_day_cehk
    # обработка файлов Чеков
    def selenium_day_Spisania(self):
        print("Обработка списания")
        if ini.time_seychas <ini.time_bot_vrem:

            for root, dirs, files in os.walk(PUT + "NEW\\Списания\\"):
                for file in files:
                    os.path.basename(file)
                    file_path = os.path.join(root, file)
                    try:
                        df = pd.read_csv(file_path, sep="\t", encoding='utf-8',skiprows=5,
                                         parse_dates=["Регистратор.Дата"], date_format="%d.%m.%Y %H:%M:%S")

                        df = df.rename(columns={"Магазин": "!МАГАЗИН!","Регистратор.Дата":"дата" })
                        # замена корявых названий
                        df = df.loc[(df["Аналитика хозяйственной операции"] =="Дегустации") |
                                    (df["Аналитика хозяйственной операции"] == "Питание сотрудников")|
                                    (df["Аналитика хозяйственной операции"] == "ПОТЕРИ") |
                                    (df["Аналитика хозяйственной операции"] == "МАРКЕТИНГ (блогеры, фотосессии)")|
                                    (df["Аналитика хозяйственной операции"] == "Подарок покупателю (бонусы)")|
                                    (df["Аналитика хозяйственной операции"] == "Подарок покупателю (сервисная фишка)")|
                                    (df["Аналитика хозяйственной операции"] == "Хозяйственные товары")|
                                    (df["Аналитика хозяйственной операции"] == "Кражи")]

                        df.loc[(df["Аналитика хозяйственной операции"] == "Дегустации") |
                                    (df["Аналитика хозяйственной операции"] == "Питание сотрудников")|
                                    (df["Аналитика хозяйственной операции"] == "ПОТЕРИ") |
                                    (df["Аналитика хозяйственной операции"] == "МАРКЕТИНГ (блогеры, фотосессии)")|
                                    (df["Аналитика хозяйственной операции"] == "Подарок покупателю (бонусы)")|
                                    (df["Аналитика хозяйственной операции"] == "Подарок покупателю (сервисная фишка)")|
                                    (df["Аналитика хозяйственной операции"] == "Кражи"), "отбор"] = "показатель"

                        df = df.rename(columns={"Регистратор.Причина списания": "Причина списания"})
                        df['Причина списания'] = df['Причина списания'].fillna('не определено')
                        df.loc[df['Причина списания'].str.contains('<Объект не найден>'), 'Причина списания'] =\
                            'не определено'
                        df = df.loc[df["дата"] != "Итого"]
                        df = df.loc[df["!МАГАЗИН!"] != "Итого"]

                        df["дата"] = pd.to_datetime(df["дата"]).dt.strftime('%d.%m.%Y')
                        rename.RENAME().Rread(name_data=df, name_col="!МАГАЗИН!", name="Списания")

                        l_mag = ("Микромаркет", "Экопункт", "Вендинг", "Итого")
                        df["!МАГАЗИН!"] = df["!МАГАЗИН!"].fillna("Не известно")
                        for w in l_mag:
                            df = df[~df["!МАГАЗИН!"].str.contains(w)]

                        dates = df["дата"].unique()
                        date_str = dates

                        for date in date_str:
                            df["дата"] = pd.to_datetime(df["дата"], format="%d.%m.%Y")
                            day_df = df.loc[df["дата"] == pd.to_datetime(date, format="%d.%m.%Y")]

                            file_name = os.path.join(PUT + "♀Списания\\История\\", date + ".csv")
                            day_df.to_csv(file_name, sep=";", encoding="utf-8", decimal=",", index=False)

                            ln = ["Количество вес", "Количество", "Сумма"]
                            Float.FLOAT().float_colms(name_data=day_df, name_col=ln)
                            do = day_df["Сумма"].sum()
                            x = day_df
                            x.loc[x["Аналитика хозяйственной операции"] == "Хозяйственные товары", "отбор"] = \
                                "Хозы"
                            x = x.groupby(["!МАГАЗИН!", "Аналитика хозяйственной операции", "дата", "отбор"],
                                          as_index=False).agg(
                                {"Количество": "sum", "Количество вес": "sum", "Сумма": "sum"}).reset_index(
                                drop=True)
                            posslw = x["Сумма"].sum()
                            # запись в лог
                            txt = f'Списания - {do:.1f}, после - {posslw:.1f},' \
                                  f' разница {(do - posslw):.1f}'
                            log.LOG().log_obrabotka(mes=txt, priznak="Списания", name_file=date)

                            # перименование столбцов
                            y = x.rename(columns={"!МАГАЗИН!": "магазин", "Сумма": "Списания"})
                            # удаление микромаркетов
                            l_mag = ("Микромаркет", "Экопункт", "Вендинг", "Итого")
                            for w in l_mag:
                                y = y[~y["магазин"].str.contains(w)].reset_index(drop=True)
                            y.to_csv(PUT + "♀Списания\\Сгрупированные файлы по дням\\" +
                                     date + ".csv", encoding="utf-8", sep='\t', index=False,
                                     decimal=',')

                            del x,y
                            gc.collect()
                            memory.MEMORY().mem_total(x="Списания")

                        try:
                            os.remove(PUT + "NEW\\Списания\\" + file)
                        except:
                            print("Нет файл для удаления")
                    except:
                        BOT.BOT().bot_mes_html(mes="📛 Фаил списания не найден",silka=0)
                gc.collect()
        BOT.BOT().bot_mes_html(mes="✅ Обработка списания....", silka=0)
        return
    # Обработка файлов списания
    def sebest(self):
        if ini.time_seychas < ini.time_bot_vrem:
            print("Обработка сибестоймости")

            for root, dirs, files in os.walk(PUT + "NEW\\Сибестоемость\\"):
                for file in files:
                    os.path.basename(file)
                    file_path = os.path.join(root, file)
                    df = pd.read_csv(file_path, sep="\t", encoding='utf-8',parse_dates=["Дата/Время чека"],
                                     date_format="%d.%m.%Y",  skiprows=2, names=("Дата/Время чека", "!МАГАЗИН!",
                                                                                 "номенклатура_1с", "Сибистоемость",
                                                                                 "Вес_продаж", "прибыль"))
                    rename.RENAME().Rread(name_data=df, name_col="!МАГАЗИН!", name="Списания")
                    df = df.loc[df["!МАГАЗИН!"] != "Итого"]
                    df = df.loc[df["Дата/Время чека"] != "Итого"]
                    l_mag = ("Микромаркет", "Экопункт", "Вендинг", "Итого")
                    df["!МАГАЗИН!"] = df["!МАГАЗИН!"].fillna("Не известно")
                    for w in l_mag:
                        df = df[~df["!МАГАЗИН!"].str.contains(w)]
                    date_str = df["Дата/Время чека"].unique()
                    for date in date_str :
                        df["Дата/Время чека"] = pd.to_datetime(df["Дата/Время чека"], format="%d.%m.%Y")
                        day_df = df.loc[df["Дата/Время чека"] == pd.to_datetime(date, format="%d.%m.%Y")]
                        file_name = os.path.join(PUT + "♀Сибестоемость\\Текущий месяц\\", date + ".csv")
                        day_df.to_csv(file_name, sep=";", encoding="utf-8", decimal=".", index=False)
                        x = day_df
                        ln = ["Сибистоемость", "Вес_продаж", "прибыль"]
                        Float.FLOAT().float_colms(name_data=x, name_col=ln)
                        # удаление микромаркетов
                        l_mag = ("Микромаркет", "Экопункт", "Вендинг", "Итого")
                        for w in l_mag:
                            x = x[~x["!МАГАЗИН!"].str.contains(w)].reset_index(drop=True)
                            # удаление подарочных карт
                        PODAROK = ["Подарочная карта КМ 500р+ конверт", "Подарочная карта КМ 1000р+ конверт",
                                   "подарочная карта КМ 500 НОВАЯ",
                                   "подарочная карта КМ 1000 НОВАЯ"]
                        for i in PODAROK:
                            x = x.loc[x["номенклатура_1с"] != i]
                        do = x["Сибистоемость"].sum()

                        x = x.groupby(["!МАГАЗИН!", "Дата/Время чека"],
                                      as_index=False).agg(
                            {"Сибистоемость": "sum", "Вес_продаж": "sum", "прибыль": "sum"}).reset_index(drop=True)
                        posslw = x["Сибистоемость"].sum()
                        # запись в лог
                        txt = f'Сибестоймость - {do:.1f}, после - {posslw:.1f},' \
                              f' разница {(do - posslw):.1f}'
                        log.LOG().log_obrabotka(mes=txt, priznak="Сибестоймость", name_file=date)

                        x = x.rename(columns={"!МАГАЗИН!": "магазин",
                                              "Сибистоемость": "себестоимость", "Вес_продаж": "вес_продаж",
                                              "Дата/Время чека": "дата"})
                        x.to_csv(PUT + "♀Сибестоемость\\Сгрупированные файлы по дням\\" + date + ".csv",
                                 encoding="utf=8", sep='\t', index=False,
                                 decimal=',')
                        gc.collect()
                        memory.MEMORY().mem_total(x="Сибестоемость")
                    os.remove(PUT + "NEW\\Сибестоемость\\" +file)
                BOT.BOT().bot_mes_html(mes="✅ Обработка сибестоемости....", silka=0)
                gc.collect()
    # Обработка сиестомости

if __name__ == '__main__':
    NEW_data().Obrabotka()





