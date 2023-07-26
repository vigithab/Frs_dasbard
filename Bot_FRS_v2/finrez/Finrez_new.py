from datetime import datetime, timedelta, time, date
import os
import pandas as pd
import gc
import datetime
import time
from Bot_FRS_v2.INI import memory
from Bot_FRS_v2.INI import ini
from Bot_FRS_v2.NEW_DATA.SET_SD import run_NEW_DATA_sd
from Bot_FRS_v2.NEW_DATA import SORT_FILE
from Bot_FRS_v2.BOT_TELEGRAM import BOT
from Bot_FRS_v2.NEW_DATA import SETRETEYL as set
import numpy as np
from Bot_FRS_v2.INI import rename
from Bot_FRS_v2.INI import Float
from Bot_FRS_v2.NEW_DATA import GRUP_FILE
from Bot_FRS_v2.INI import log
from Bot_FRS_v2.RASSILKA import Voropaev
from Bot_FRS_v2.NEW_DATA import Personal_v2


class finrez_obrabotka():
    def __init__(self):
        pd.set_option("expand_frame_repr", False)
        pd.set_option('display.max_colwidth', None)
        self.PUT = ini.PUT

    def finrez_itog(self):
        for files in os.listdir(self.PUT + "Финрез\\Исходник\\"):
            FINREZ = pd.read_excel(self.PUT + "Финрез\\Исходник\\" + files, sheet_name="Динамика ТТ исходник")
            FINREZ = FINREZ.rename(columns={"Торговая точка": "магазин", "Дата": "дата",
                                            "Канал": "канал",
                                            "Режим налогообложения": "режим налогообложения",
                                            "Канал на последний закрытый период": "канал на последний закрытый период"})

            FINREZ = FINREZ.loc[FINREZ['дата'] >= "2022-01-01"]
            FINREZ = rename.RENAME().Rread(name_data=FINREZ, name_col="магазин")

            # region для получения уникальных значений колонок
            FINREZ_SPRAVOCHNIK_STATIYA = FINREZ.melt(
                id_vars=["дата", "магазин", "режим налогообложения", "канал", "канал на последний закрытый период"],
                var_name="статья",
                value_name="значение")
            unique_values = FINREZ_SPRAVOCHNIK_STATIYA["статья"].unique()
            FINREZ_SPRAVOCHNIK_STATIYA = pd.DataFrame({'статья': unique_values})
            # DOC().to_exel(x=FINREZ_SPRAVOCHNIK_STATIYA, name="Справоник статей.xlsx")
            del unique_values
            del FINREZ_SPRAVOCHNIK_STATIYA
            gc.collect()
            # endregion
            # region выбор столбцов в файле
            FINREZ = FINREZ[
                ["дата", "магазин", "режим налогообложения", "канал", "канал на последний закрытый период",
                 "Товарооборот (продажи) МКП, ед", "Товарооборот (продажи) МКП, руб с НДС",
                 "Товарооборот (продажи) КП, ед",
                 "Товарооборот (продажи) КП, руб с НДС", "Товарооборот (продажи) сопутка, ед",
                 "Товарооборот (продажи) сопутка, руб с НДС",
                 # ---Доход
                 "Выручка Итого, руб без НДС",
                 "Прочие доходы (субаренда), руб без НДС", "Прочие доходы (утилизация), руб без НДС",
                 "Доход от продажи ТМЦ, руб без НДС",
                 "Прочие доходы (паушальный взнос, услуги по открытию), руб без НДС", "Доход Штрафы, руб без НДС",
                 "Доход Аренда помещений, руб без НДС",
                 "Доход (аренда оборудования), руб без НДС",

                 "Доход роялти2 в аренду, руб без НДС",
                 "Доход роялти 4,1% инвестц, 8,1% в аренду, руб без НДС",
                 # "Доход Роялти, руб без НДС",
                 "Доход комиссионное вознаграждение, руб без НДС",
                 "Доход Услуги по договору комиссии интернет-магазин, руб без НДС",
                 # ---Закуп
                 "* Закуп товара (МКП, КП, сопутка), руб без НДС",
                 # ---Затраты
                 "ОЕ - Общие Операционные расходы (сумма всех статей расходов), руб без НДС",
                 "2.1. ФОТ+Отчисления", "2.2. Аренда", "2.19. Бонусы программы лояльности",
                 "2.3.1. Электроэнергия", "2.3.2. Вывоз мусора, ЖБО, ТБО",
                 "2.3.3. Тепловая энергия",
                 "2.3.4. Водоснабжение",
                 "2.3.5. Водоотведение",
                 "2.3.6. Прочие коммунальные услуги (ФРС)",
                 "2.3.7. Газоснабжение",
                 "2.11. Маркетинговые расходы",
                 "2.9. Налоги",
                 "2.5.2. НЕУ",
                 "2.10. Питание сотрудников ",
                 "2.17. Распределяемая аналитика",
                 ''
                 # "2.18. Затраты службы развития",
                 "2.3.8. Охрана",
                 "2.4. Услуги банка",
                 "2.7. Прочие прямые затраты",
                 "2.7.1. Дезинфекционные средства",
                 "2.7.10. Услуги сотовой связи",
                 "2.7.2. Канцелярские товары",
                 "2.7.3. Командировочные расходы",
                 "2.7.4. Медицинские услуги, медикаменты, медосмотры",
                 "2.7.5. Расходы на аренду прочего имущества",
                 "2.7.6. Спецодежда, спецобувь, СИЗ",
                 "2.7.7. Транспортные услуги",
                 "2.7.8. Интернет",
                 "2.7.9. Услуги по дератизации, дезинсекции",
                 "2.16. Роялти",
                 "2.5.1. Списание потерь (до ноября 19г НЕУ + Списание потерь)",
                 "2.13. Инструменты/инвентарь",
                 "2.14. Ремонт и содержание зданий, оборудования",
                 "2.15.ТО оборудования (аутсорсинг)",
                 "2.6. Хозяйственные товары",
                 "2.8. ТМЦ ",
                 "Рентабельность, %",
                 "Прибыль (+) / Убыток (-) (= Т- ОЕ), руб без НДС",
                 "Наценка Общая, руб без НДС",
                 "Наценка Общая, %",
                 "Наценка МКП и КП, руб с НДС",
                 "Наценка сопутка, руб с НДС",
                 "Наценка МКП и КП, %",
                 "Наценка сопутка, %",
                 ##
                 "Доля колбаса",
                 "Доля п/ф",
                 "Доля  гриль",
                 "Доля  Кости ливер отруба",
                 "Доля куриные п/ф",
                 "Доля субпродукты кур",
                 "Доля сопутка",
                 "Доля Калина малина",
                 "Доля зеленый магазин",
                 "Доля Волков Кофе",
                 "Доля \"Изготовлено по заказу\"",
                 "Доля Рыбные п/ф",
                 "Доля Продукция кулинарного цеха КХВ",
                 "Доля Пекарня",
                 # Инвестиции
                 "Инвестиции 3.1. Маркетинговые расходы",
                 "Инвестиции 3.2. Инструменты/инвентарь",
                 "Инвестиции 3.3. Ремонт и содержание зданий, оборудования",
                 "3.3.1. Инвестиции на переформат и открытие",
                 "3.3.2. Инвестиции на переформат и открытие Оборудование (тех служба ФРС)",
                 "3.3.3. Инвестиции на переформат и открытие Ремонт (тех служба ФРС)",
                 "Инвестиции 3.4. ТО оборудования (аутсорсинг)",
                 # точка безубыточности
                 "Точка безубыточности (МКП, КП, Сопутка), руб с НДС",
                 "Разница между точкой безубыточности и объемом продаж, руб с НДС",
                 "Среднесписочная численность персонала на ТТ",
                 "Средняя з/пл с отчислениями",
                 ###
                 "1.1.Закуп товара (МКП и КП), руб с НДС",
                 "1.2.Закуп товара (сопутка), руб с НДС",
                 "Выручка Итого, руб с НДС"]]
            # endregion
            # region получение числа коналов для каждого магазина для фильтрации ФРС, даты перехода магазина корректировка
            FINREZ_00 = FINREZ.groupby(["магазин", "дата"])['канал'].nunique().reset_index()
            FINREZ_00 = FINREZ_00.rename(columns={'канал': 'канал_кол'})
            FINREZ = pd.merge(FINREZ, FINREZ_00[['магазин', 'дата', 'канал_кол']], on=['магазин', 'дата'],
                              how='left')
            # даты пререхода на франшизу корректировка
            FINREZ.loc[
                (FINREZ['дата'] == '2022-07-01') & (FINREZ['магазин'] == 'Комсомольский, 34'), 'канал_кол'] = 1
            FINREZ.loc[
                (FINREZ['дата'] == '2022-08-01') & (FINREZ['магазин'] == 'Л-К, ул.Ленина, 50'), 'канал_кол'] = 1
            FINREZ.loc[(FINREZ['дата'] == '2022-07-01') & (FINREZ['магазин'] == 'Ленина, 133'), 'канал_кол'] = 1
            FINREZ.loc[
                (FINREZ['дата'] == '2022-07-01') & (FINREZ['магазин'] == 'Ленинградский, 30/1'), 'канал_кол'] = 1
            FINREZ.loc[
                (FINREZ['дата'] == '2022-05-01') & (FINREZ['магазин'] == 'Ленинградский, 45'), 'канал_кол'] = 1
            FINREZ.loc[
                (FINREZ['дата'] == '2022-06-01') & (
                            FINREZ['магазин'] == 'Межд-к, пр.Шахтеров, 23А'), 'канал_кол'] = 1
            FINREZ.loc[(FINREZ['дата'] == '2022-02-01') & (FINREZ['магазин'] == 'Московский, 18'), 'канал_кол'] = 1
            FINREZ.loc[
                (FINREZ['дата'] == '2022-01-01') & (
                            FINREZ['магазин'] == 'Новосиб, ул.Каменская, 44'), 'канал_кол'] = 1
            FINREZ.loc[(FINREZ['дата'] == '2022-05-01') & (FINREZ['магазин'] == 'Ноградская, 34'), 'канал_кол'] = 1
            FINREZ.loc[(FINREZ['дата'] == '2022-02-01') & (FINREZ['магазин'] == 'Октябрьский, 78'), 'канал_кол'] = 1
            FINREZ.loc[
                (FINREZ['дата'] == '2022-08-01') & (FINREZ['магазин'] == 'Осинники, Победы, 32'), 'канал_кол'] = 1
            FINREZ.loc[
                (FINREZ['дата'] == '2022-07-01') & (
                            FINREZ['магазин'] == 'Полысаево, Космонавтов 82'), 'канал_кол'] = 1
            FINREZ.loc[
                (FINREZ['дата'] == '2022-07-01') & (
                            FINREZ['магазин'] == 'Прокопьевск, Гагарина, 37'), 'канал_кол'] = 1
            FINREZ.loc[(FINREZ['дата'] == '2022-08-01') & (FINREZ['магазин'] == 'Терешковой, 22А'), 'канал_кол'] = 1
            FINREZ.loc[(FINREZ['дата'] == '2022-05-01') & (FINREZ['магазин'] == 'Шахтеров, 111'), 'канал_кол'] = 1
            FINREZ.loc[(FINREZ['дата'] == '2022-06-01') & (FINREZ['магазин'] == 'Шахтеров, 36'), 'канал_кол'] = 1
            ######################################################## изменено
            FINREZ.loc[(FINREZ['дата'] == '2023-05-01') & (FINREZ['магазин'] == '40 лет Октября, 20'), 'канал_кол'] = 1


            FINREZ["Закуп товара общий, руб с НДС"] = FINREZ["1.1.Закуп товара (МКП и КП), руб с НДС"] + FINREZ[
                "1.2.Закуп товара (сопутка), руб с НДС"]
            FINREZ.loc[FINREZ["режим налогообложения"] == "упрощенка", "Закуп(режм налога)"] = FINREZ[
                "Закуп товара общий, руб с НДС"]
            FINREZ.loc[FINREZ["режим налогообложения"] == "общий", "Закуп(режм налога)"] = FINREZ[
                "* Закуп товара (МКП, КП, сопутка), руб без НДС"]
            FINREZ.loc[FINREZ["канал"] == "Итого Франшиза", "Закуп(режм налога)"] = FINREZ["Наценка Общая, %"]
            FINREZ.loc[FINREZ["канал"] == "Итого ФРС", "Закуп(режм налога)"] = FINREZ["Наценка Общая, %"]
            FINREZ["Товарооборот КП + МКП, руб с НДС"] = FINREZ["Товарооборот (продажи) КП, руб с НДС"] + FINREZ[
                "Товарооборот (продажи) МКП, руб с НДС"]
            FINREZ["Товарооборот(Общий) с НДС"] = FINREZ["Товарооборот (продажи) КП, руб с НДС"] + FINREZ[
                "Товарооборот (продажи) МКП, руб с НДС"] + FINREZ["Товарооборот (продажи) сопутка, руб с НДС"]
            FINREZ["Наценка (Общий) с НДС"] = FINREZ["Наценка МКП и КП, руб с НДС"] + FINREZ[
                "Наценка сопутка, руб с НДС"]

            # endregion
            # переименование обобщения
            FINREZ.loc[FINREZ['магазин'] == "Офис", "канал"] = "Офис"
            FINREZ.loc[FINREZ['магазин'] == "Роялти ФРС", "канал"] = "Роялти ФРС"
            FINREZ = FINREZ.reset_index(drop=True)
            # сохранение временного файла с каналами и режимом налогобложения
            FINREZ_MAX = FINREZ[
                ["дата", 'магазин', 'режим налогообложения', 'канал', 'канал на последний закрытый период']]

            FINREZ_MAX.to_csv(ini.PUT + "Финрез\\Temp\\Дата_канал_налог.csv", encoding="ANSI", sep=';',
                              index=False, decimal='.')
            del FINREZ_MAX
            gc.collect()

            # добавление закуп товара с НДС
            FINREZ["Закуп товара общий, руб с НДС"] = FINREZ["1.1.Закуп товара (МКП и КП), руб с НДС"] + \
                                                      FINREZ["1.2.Закуп товара (сопутка), руб с НДС"]
            FINREZ.loc[(FINREZ["канал"] == "ФРС") & (FINREZ["режим налогообложения"] == "упрощенка"),
            "* Закуп товара (МКП, КП, сопутка), руб без НДС"] = FINREZ["Закуп товара общий, руб с НДС"]

            # разворот таблицы фнреза
            FINREZ = FINREZ.melt(
                id_vars=["дата", "магазин", "режим налогообложения", "канал", "канал на последний закрытый период",
                         'канал_кол'],
                var_name="статья",
                value_name="значение")
            # очистка от мусора
            FINREZ['значение'] = FINREZ['значение'].astype("str")
            FINREZ['значение'] = FINREZ['значение'].str.replace(u'\xa0', "")
            FINREZ['значение'] = np.where((FINREZ['значение'] == 0), "nan", FINREZ['значение'])
            FINREZ['значение'] = np.where((FINREZ['значение'] == "-"), "nan", FINREZ['значение'])
            FINREZ['значение'] = np.where((FINREZ['значение'] == "#ДЕЛ/0!"), "nan", FINREZ['значение'])
            FINREZ['значение'] = np.where((FINREZ['значение'] == "#ЗНАЧ!"), "nan", FINREZ['значение'])
            FINREZ['значение'] = FINREZ['значение'].str.replace(",", ".")
            FINREZ = FINREZ.loc[(FINREZ['значение'] != "nan")]

            FINREZ['значение'] = FINREZ['значение'].astype("float")
            FINREZ = FINREZ.loc[(FINREZ['значение'] != 0)]
            # округление
            FINREZ['значение'] = FINREZ['значение'].round(2)
            # переименование названия закупа
            FINREZ.loc[FINREZ[
                           "статья"] == "* Закуп товара (МКП, КП, сопутка), руб без НДС", "статья"] = "Закуп товара (МКП, КП, сопутка), руб без НДС"
            # region добавление справочника сатей

            STATYA = pd.read_excel(ini.PUT + "Финрез\\Данные\\↓СПРАВОЧНИК_СТАТЕЙ.xlsx",
                                   sheet_name="STATYA_REDAKT")
            FINREZ = FINREZ.merge(STATYA[["статья", "фрс_расчет среднего",
                                          "фр_расчет чистой прибыли", "подгруппа", "группа",
                                          "фрс_расчет чистой прибыли", "удалить для фрс и аренда", "отбор"]],
                                  on=["статья"], how="left")
            # endregion

            # region убрать все значения для сочетания фрс где более 2х каналов в месяце
            FINREZ_Er = FINREZ.copy()
            mask = (FINREZ['канал'] == 'ФРС') & (FINREZ['канал_кол'] == 2) & (
                    FINREZ["удалить для фрс и аренда"] == 'да')
            FINREZ.loc[mask, 'значение'] = 0

            # добавление столбца для каскадных значений
            FINREZ["каскад"] = FINREZ["значение"]
            FINREZ.loc[FINREZ["группа"] == "Затраты, руб.(без НДС)", "каскад"] = -FINREZ["значение"]
            FINREZ.loc[FINREZ["группа"] == "Закуп, руб.(без НДС)", "каскад"] = -FINREZ["значение"]

            # деление таблиц на каналы
            # ################################################################# ФРС
            # ФРС только стать участвующие в чистой прибыли
            FINREZ_FRS = FINREZ.loc[FINREZ["канал"] == "ФРС"]
            FINREZ_FRS = FINREZ_FRS.loc[(FINREZ_FRS["фрс_расчет чистой прибыли"] == "да")]

            # добавление чистой прибыли
            grouped = FINREZ_FRS.groupby(
                ['магазин', 'дата', 'канал', "канал на последний закрытый период", "режим налогообложения"])

            sums = grouped['каскад'].agg('sum')
            new_row = pd.DataFrame({
                'магазин': sums.index.get_level_values('магазин'),
                'дата': sums.index.get_level_values('дата'),
                "канал на последний закрытый период": sums.index.get_level_values(
                    "канал на последний закрытый период"),
                "режим налогообложения": sums.index.get_level_values("режим налогообложения"),
                'канал': sums.index.get_level_values('канал'),
                "статья": 'чистая прибыль',
                'значение': sums.values,
                'каскад': sums.values})
            FINREZ_FRS = pd.concat([FINREZ_FRS, new_row], axis=0)
            # region ERROR ФРС
            FINREZ_Er = FINREZ_Er.loc[FINREZ_Er["канал"] == "ФРС"].copy()
            FINREZ_Er.loc[
                FINREZ_Er[
                    "статья"] == "Прибыль (+) / Убыток (-) (= Т- ОЕ), руб без НДС", "статья"] = "чистая прибыль"
            FINREZ_ERROR = FINREZ_Er.loc[FINREZ_Er["статья"] == "чистая прибыль"].copy()
            FINREZ_ERROR = FINREZ_ERROR.rename(columns={"значение": "значение из итогов"})

            FINREZ_FRS_00 = FINREZ_FRS.copy()
            FINREZ_FRS_00 = FINREZ_FRS_00.loc[FINREZ_FRS_00["статья"] == "чистая прибыль"]
            FINREZ_ERROR_FRS = FINREZ_FRS_00.merge(
                FINREZ_ERROR[["дата", "значение из итогов", "магазин", "статья", 'канал']],
                on=["статья", "магазин", "дата", 'канал'], how="left")
            FINREZ_ERROR_FRS["расхождение"] = FINREZ_ERROR_FRS["значение"] - FINREZ_ERROR_FRS["значение из итогов"]
            FINREZ_ERROR_FRS = FINREZ_ERROR_FRS.loc[
                (FINREZ_ERROR_FRS["расхождение"] < -10) | (FINREZ_ERROR_FRS["расхождение"] > 10)]
            # endregion
            # добавление статей для фрс
            FINREZ_FRS_01 = FINREZ.loc[FINREZ["канал"] == "ФРС"]
            FINREZ_FRS_01 = FINREZ_FRS_01.loc[(FINREZ_FRS_01["отбор"] == "товароборот") |
                                              (FINREZ_FRS_01["отбор"] == "наценка") |
                                              (FINREZ_FRS_01["отбор"] == "доля") |
                                              (FINREZ_FRS_01["отбор"] == "инвестиции") |
                                              (FINREZ_FRS_01["отбор"] == "точка безубыточности") |
                                              (FINREZ_FRS_01["отбор"] == "персонал")]
            FINREZ_FRS = pd.concat([FINREZ_FRS, FINREZ_FRS_01], axis=0)
            # Фрс исключения для расчета рентабельности
            FINREZ_FRS.loc[(FINREZ_FRS["отбор"] == "товароборот") |
                           (FINREZ_FRS["отбор"] == "наценка") |
                           (FINREZ_FRS["отбор"] == "доля") |
                           (FINREZ_FRS["отбор"] == "инвестиции") |
                           (FINREZ_FRS["отбор"] == "точка безубыточности") |
                           (FINREZ_FRS["отбор"] == "персонал"), "каскад"] = 0

            FINREZ_FRS = FINREZ_FRS.reset_index(drop=True)

            # ################################################################# ФРАНШИЗА
            # ФРАНШИЗА только стать участвующие в чистой прибыли
            FINREZ_FRANSHIZA = FINREZ.loc[
                (FINREZ["канал"] == "Франшиза в аренду") | (FINREZ["канал"] == "Франшиза внешняя")]
            FINREZ_FRANSHIZA = FINREZ_FRANSHIZA.loc[(FINREZ_FRANSHIZA["фр_расчет чистой прибыли"] == "да")]

            # добавление чистой прибыли
            grouped = FINREZ_FRANSHIZA.groupby(
                ['магазин', 'дата', 'канал', "канал на последний закрытый период", "режим налогообложения"])
            sums = grouped['каскад'].agg('sum')
            new_row = pd.DataFrame({
                'магазин': sums.index.get_level_values('магазин'),
                'дата': sums.index.get_level_values('дата'),
                "канал на последний закрытый период": sums.index.get_level_values(
                    "канал на последний закрытый период"),
                "режим налогообложения": sums.index.get_level_values("режим налогообложения"),
                'канал': sums.index.get_level_values('канал'),
                "статья": 'чистая прибыль',
                'значение': sums.values,
                'каскад': sums.values})
            FINREZ_FRANSHIZA = pd.concat([FINREZ_FRANSHIZA, new_row], axis=0)
            # region ERROR ФР
            FINREZ_00 = FINREZ.copy()
            FINREZ_00.loc[
                FINREZ_00[
                    "статья"] == "Прибыль (+) / Убыток (-) (= Т- ОЕ), руб без НДС", "статья"] = 'чистая прибыль'
            FINREZ_ERROR = FINREZ_00.loc[FINREZ_00["статья"] == 'чистая прибыль'].copy()
            FINREZ_ERROR = FINREZ_ERROR.rename(columns={"значение": "значение из итогов"})
            FINREZ_FRANSHIZA_00 = FINREZ_FRANSHIZA.copy()
            FINREZ_FRANSHIZA_00 = FINREZ_FRANSHIZA_00.loc[FINREZ_FRANSHIZA_00["статья"] == "чистая прибыль"]

            FINREZ_ERROR_FR = FINREZ_FRANSHIZA_00.merge(
                FINREZ_ERROR[["дата", "значение из итогов", "магазин", "статья", 'канал']],
                on=["статья", "магазин", "дата", 'канал'], how="left")
            FINREZ_ERROR_FR["расхождение"] = FINREZ_ERROR_FR["значение"] - FINREZ_ERROR_FR["значение из итогов"]
            FINREZ_ERROR_FR = FINREZ_ERROR_FR.loc[
                (FINREZ_ERROR_FR["расхождение"] < -10) | (FINREZ_ERROR_FR["расхождение"] > 10)]
            # endregion
            # добавление выручки без ндс для франшизы
            FINREZ_FRANSHIZA_01 = FINREZ.loc[
                (FINREZ["канал"] == "Франшиза в аренду") | (FINREZ["канал"] == "Франшиза внешняя")]
            FINREZ_FRANSHIZA_01 = FINREZ_FRANSHIZA_01.loc[
                (FINREZ_FRANSHIZA_01["статья"] == "Выручка Итого, руб без НДС")]

            FINREZ_FRANSHIZA_01.loc[FINREZ_FRANSHIZA_01[
                                        "статья"] == "Выручка Итого, руб без НДС", "статья"] = 'Выручка Итого, руб без НДС(для франшизы)'
            FINREZ_FRANSHIZA = pd.concat([FINREZ_FRANSHIZA, FINREZ_FRANSHIZA_01], axis=0)
            FINREZ_FRANSHIZA = FINREZ_FRANSHIZA.reset_index(drop=True)

            # добавление Товарооборота без ндс для франшизы
            FINREZ_FRANSHIZA_01 = FINREZ.loc[
                (FINREZ["канал"] == "Франшиза в аренду") | (FINREZ["канал"] == "Франшиза внешняя")]
            FINREZ_FRANSHIZA_01 = FINREZ_FRANSHIZA_01.loc[(FINREZ_FRANSHIZA_01["отбор"] == "товароборот") |
                                                          (FINREZ_FRANSHIZA_01["отбор"] == "наценка") |
                                                          (FINREZ_FRANSHIZA_01["отбор"] == "доля") |
                                                          (FINREZ_FRS_01["отбор"] == "инвестиции")]
            FINREZ_FRANSHIZA = pd.concat([FINREZ_FRANSHIZA, FINREZ_FRANSHIZA_01], axis=0)
            # Фрс исключения для расчета рентабельности
            FINREZ_FRANSHIZA.loc[(FINREZ_FRANSHIZA["отбор"] == "товароборот") |
                                 (FINREZ_FRANSHIZA["отбор"] == "наценка") |
                                 (FINREZ_FRANSHIZA["отбор"] == "доля") |
                                 (FINREZ_FRANSHIZA["отбор"] == "инвестиции") |
                                 (FINREZ_FRANSHIZA["отбор"] == "точка безубыточности") |
                                 (FINREZ_FRANSHIZA["отбор"] == "персонал"), "каскад"] = 0
            FINREZ_FRANSHIZA = FINREZ_FRANSHIZA.reset_index(drop=True)

            # ################################################################# ФРАНШИЗА
            FINREZ_FRANSHIZA = FINREZ_FRANSHIZA.rename(columns={'значение': 'значение_фр', "каскад": "каскад_фр"})
            FINREZ_FRS = FINREZ_FRS.rename(columns={'значение': 'значение_фрс', "каскад": "каскад_фрс"})
            FINREZ = pd.concat([FINREZ_FRANSHIZA, FINREZ_FRS], axis=0)
            FINREZ = FINREZ.reset_index(drop=True)

            # сохранение временного файла для дальнецшей обработки
            FINREZ_ERROR_FRS.to_csv(
                ini.PUT + "Финрез\\error\\Ошики ФРС(сравнение чистой приыли из файла и вычесленой по статейно для каждого магазина.csv",
                encoding="ANSI", sep=';',
                index=False, decimal='.')
            FINREZ_ERROR_FR.to_csv(
                ini.PUT + "Финрез\\error\\Ошики франшиза(сравнение чистой приыли из файла и вычесленой по статейно для каждого магазина.csv",
                encoding="ANSI", sep=';',
                index=False, decimal='.')

            FINREZ = FINREZ.merge(
                FINREZ_ERROR_FRS[
                    ["дата", "магазин", "режим налогообложения", "канал", 'канал на последний закрытый период',
                     "статья", "расхождение"]],
                on=["дата", "магазин", "режим налогообложения", "канал", 'канал на последний закрытый период',
                    "статья"], how="left")

            # FINREZ.loc[FINREZ["расхождение"] > 0, ["значение_фрс", "каскад_фрс"]] -= FINREZ.loc[FINREZ["расхождение"] > 0, "расхождение"]

            mask = FINREZ["расхождение"].notnull()
            FINREZ.loc[mask, "значение_фрс"] -= FINREZ.loc[mask, "расхождение"]
            FINREZ.loc[mask, "каскад_фрс"] -= FINREZ.loc[mask, "расхождение"]
            # FINREZ.loc[FINREZ["расхождение"]>0 , ["значение_фрс","каскад_фрс"]] = FINREZ[["значение_фрс", "каскад_фрс"]] - FINREZ["расхождение"]

            # FINREZ.loc[FINREZ["расхождение"] > 0, ["значение_фрс", "каскад_фрс"]] = FINREZ[["значение_фрс", "каскад_фрс"]] - FINREZ["расхождение"]
            self.FINREZ = FINREZ


            FINREZ.to_csv(ini.PUT + "Финрез\\error\\удалить.csv",
                          encoding="ANSI", sep=';',
                          index=False, decimal='.')

            FINREZ_FRANSHIZA.to_csv(ini.PUT+ "Финрез\\Данные для ДШ\\Финрез_Франшиза.csv", encoding="ANSI", sep=';',
                                    index=False, decimal=',')
            FINREZ_FRS.to_csv(ini.PUT + "Финрез\\Данные для ДШ\\Финрез_ФРС.csv", encoding="ANSI", sep=';',
                              index=False, decimal=',')
            FINREZ.to_csv(ini.PUT + "Финрез\\Данные для ДШ\\↓Финрез_Обработанный.csv", encoding="ANSI", sep=';',
                          index=False, decimal=',')
            print("Сохранено - Финрез_Обработанный.csv")
    def prgnoz(self):
        print("self.FINREZ")
        print(self.FINREZ)
        FINREZ = self.FINREZ
        min_date = self.FINREZ['дата'].max()
        future_month = min_date + pd.DateOffset(months=1)
        future_month = future_month.replace(day=1)
        # Установка желаемой даты
        target_date = '01.06.2023'
        # Получение даты 3 месяца назад от желаемой даты
        start_date = pd.to_datetime(min_date, format='%d.%m.%Y') - pd.DateOffset(months=2)
        print(start_date)
        # Фильтрация данных за последние 3 месяца
        filtered_df = FINREZ[FINREZ['дата'] >= start_date]
        print(filtered_df)
        filtered_df.to_csv(ini.PUT + "Финрез\\Данные для ДШ\\↓Прогноз1.csv", encoding="ANSI", sep=';',
                           index=False, decimal=',')
        # Группировка данных по магазину, статье и расчет среднего значения для 'значение_фр' и 'значение_фрс'
        forecast_df = filtered_df.groupby(['магазин',"режим налогообложения","канал","канал на последний закрытый период",
                                            'статья']).agg(
            {'значение_фр': 'mean',"каскад_фр":'mean', 'значение_фрс': 'mean',"каскад_фрс":'mean'}).reset_index()
        # Вывод прогнозного датафрейма

        print(forecast_df)
        forecast_df.to_csv(ini.PUT + "Финрез\\Данные для ДШ\\↓Прогноз.csv", encoding="ANSI", sep=';',
                                  index=False, decimal=',')

finrez_obrabotka = finrez_obrabotka()
finrez_obrabotka.finrez_itog()
finrez_obrabotka.prgnoz()



