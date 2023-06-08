import os
import pandas as pd
import xlsxwriter
import gc
import numpy as np
from openpyxl.styles import PatternFill
from openpyxl import Workbook
pd.set_option("expand_frame_repr", False)
pd.set_option('display.max_colwidth', None)
gc.enable()

PUT = "C:\\Users\\lebedevvv\\Desktop\\ДЛя жени\\Данные\\"
class RENAME:
    def Rread(self):
        print("Загрузка справочника магазинов...")
        replacements = pd.read_excel("https://docs.google.com/spreadsheets/d/1SfuC2zKUFt6PQOYhB8EEivRjy4Dz-o4WDL-IR7CT3Eg/export?exportFormat=xlsx")
        """replacements = pd.read_excel(PUT + "Справочники\\ДЛЯ ЗАМЕНЫ.xlsx",
                                     sheet_name="Лист1")"""
        unique_vals = set(replacements ['НАЙТИ'].unique())
        return unique_vals
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
class Obrabotka:
    def poisk(self):
        ISKL = ["Гостиница, Островского",
                "Интернет-магазин Калина малина",
                "Лента ООО",
                "Отдел управления проектами",
                "Распределяемая аналитика структуры сбыта",
                "Распределительный центр (РЦ)",
                "ТАНДЕР АО",
                "Склад Экопункт г.Кемерово, пр.Кузнецкий, 33",
                "Бюджет собственников",
                "Склад №26 (Новокузнецк)",
                "Не исп Склад №106 ФМ г.Новокузнецк, пр.Металлургов, 34",
                "Администрация",
                "Склад №10 (Новокузнецк, Селекционная)",
                "Склад №11",
                "Склад №11 (Тухачевского яч №6)",
                "Склад №12",
                "Склад №12 (Тухач. магазин)",
                "Склад №13 (Новосибирск, Сиб-Гвардейцев, 49/1)",
                "Склад №14 (Красноярск, Шахтеров 35 к.1)"]

        # Поиск файлов текущих продаж. Список всех файлов в папке и подпапках
        all_files = []
        for root, dirs, files in os.walk(PUT + "АА\\"):
            for file in files:
                all_files.append(os.path.join(root, file))
        for i in all_files:
            print(i)
            AA = pd.read_excel(i)
            print(AA)
            name_file =AA.iat[1, 1]
            Name_file = AA.columns[1][-24:]+"_44сч_" + name_file[8:-3]
            Name_file_col = AA.columns[1][-24:]
            AA = AA[["Индивидуальный предприниматель Волков Артем Анатольевич", "Unnamed: 4"]]
            # создание новой строки с названиями столбцов
            AA.columns = ['Дробить', "Обороты за период"]
            AA = AA.iloc[10:]
            Spisok_magaz = RENAME().Rread()

            for i in Spisok_magaz :
                AA.loc[AA['Дробить'] == i, 'магазин'] = AA['Дробить']
            AA["магазин"] = AA["магазин"].ffill()
            AA.loc[AA["магазин"] == AA['Дробить'], ["магазин", "Обороты за период", 'Дробить']] = [np.nan, np.nan,np.nan]
            #AA.loc[AA["магазин"] == AA['Дробить'], ["магазин", "Обороты за период"]] = [np.nan, np.nan]

            AA['номер склада'] = AA["магазин"].str.extract('№(\d+)', expand=False)
            AA= AA.loc[AA["магазин"].notnull()]
            FLOAT().float_colm(name_data= AA, name_col="Обороты за период")
            AA['фаил'] = Name_file_col
            # region ДОП ТАБЛИЦА ДЛЯ ПОИСКА СТАТЕЙ
            LN_1 = AA[["Дробить", "фаил", "магазин", "номер склада"]]
            LN_1.to_excel(PUT + "ОБРАБОТАННЫЙ\\промежуточные\\" + Name_file_col + ".xlsx",index=False)
            # endregion

            AA = AA.pivot_table(index=['магазин','номер склада','фаил'], columns='Дробить', values='Обороты за период').reset_index()
            AA = AA.drop(columns={"Итого"})

            AA.to_csv(PUT + Name_file + ".csv", encoding="ANSI", sep=';',
                      index=False, decimal=',')

        # Поиск файлов текущих продаж. Список всех файлов в папке и подпапках
        all_files = []
        for root, dirs, files in os.walk(PUT + "АП\\"):
            for file in files:
                all_files.append(os.path.join(root, file))
        for i in all_files:
            AP = pd.read_excel(i)
            name_file = AP.iat[1, 1]
            Name_file = AP.columns[1][-24:] + "_44сч_" + name_file[8:-3]
            Name_file_col = AP.columns[1][-24:]
            AP = AP[["Индивидуальный предприниматель Волков Анатолий Павлович", "Unnamed: 4"]]
            AP.columns = ['Дробить', "Обороты за период"]
            AP = AP.iloc[11:]
            Spisok_magaz = RENAME().Rread()
            for i in Spisok_magaz :
                AP.loc[AP['Дробить'] == i, 'магазин'] = AP['Дробить']

            # Извлекаем номер склада из столбца "магазин" и создаем новый столбец "номер склада"
            AP['номер склада'] = AP['магазин'].str.extract('№(\d+)', expand=False)
            # Создаем новый столбец "содержит_франшизу", который будет содержать булевую маску
            mask = AP['магазин'].fillna('not_found').str.contains('Франшиза Склад', case=False)
            # Используем метод loc для установки значения "номер склада"
            AP.loc[mask & ~AP['номер склада'].isna(), 'номер склада'] = AP.loc[mask & ~AP['номер склада'].isna(), 'номер склада'] + 'Ф'
            AP.loc[~mask & ~AP['номер склада'].isna(), 'номер склада'] = AP.loc[~mask & ~AP['номер склада'].isna(), 'номер склада']
            # Если в исходных данных были пропущенные значения в столбце "магазин", то можно заменить их обратно на пропущенные значения с помощью метода where()
            AP['номер склада'] = AP['номер склада'].where(AP['магазин'].notna(), np.nan)
            AP["магазин"] = AP["магазин"].ffill()
            AP['номер склада'] = AP['номер склада'].ffill()
            AP.loc[AP["магазин"] ==AP['Дробить'], ["магазин", "Обороты за период", 'Дробить']] = [np.nan, np.nan, np.nan]
            AP = AP.loc[AP["магазин"].notnull()]
            for i in ISKL:
                AP = AP.loc[AP["магазин"]!=i]
            AP = AP.loc[AP['Дробить'] != 'Итого']
            AP['фаил'] = Name_file_col
            # region ДОП ТАБЛИЦА ДЛЯ ПОИСКА СТАТЕЙ
            LN_1 = AP[["Дробить", "фаил", "магазин", "номер склада"]]

            LN_1.to_excel(PUT + "ОБРАБОТАННЫЙ\\промежуточные\\" + Name_file_col + ".xlsx",index=False,)
            # endregion

            FLOAT().float_colm(name_data=AP, name_col="Обороты за период")
            AP = AP.pivot_table(index=['магазин', 'номер склада', 'фаил'], columns='Дробить', values='Обороты за период').reset_index()




            print(Name_file_col)
            print(Name_file)
            AP.to_csv(PUT + Name_file + ".csv", encoding="ANSI", sep=';',
                      index=False, decimal=',')

        # Поиск файлов текущих продаж. Список всех файлов в папке и подпапках
        all_files = []
        for root, dirs, files in os.walk(PUT + "ЛН\\"):
            for file in files:
                all_files.append(os.path.join(root, file))
        for i in all_files:
            LN = pd.read_excel(i)
            name_file = LN.iat[1, 1]
            Name_file = LN.columns[1][-24:] + "_44сч_" + name_file[8:-3]
            Name_file_col = LN.columns[1][-24:]
            LN = LN[["Индивидуальный предприниматель Волкова Лидия Николаевна", "Unnamed: 4"]]
            # создание новой строки с названиями столбцов
            LN.columns = ['Дробить', "Обороты за период"]
            LN = LN.iloc[8:]
            Spisok_magaz = RENAME().Rread()
            for i in Spisok_magaz :
                LN.loc[LN['Дробить'] == i, 'магазин'] = LN['Дробить']
            # Извлекаем номер склада из столбца "магазин" и создаем новый столбец "номер склада"
            LN['номер склада'] = LN['магазин'].str.extract('№(\d+)', expand=False)
            LN["магазин"] = LN["магазин"].ffill()
            LN['номер склада'] = LN['номер склада'].ffill()
            for i in ISKL:
                LN = LN.loc[LN["магазин"]!=i]
            LN = LN.loc[LN['Дробить'] != 'Итого']
            LN.loc[LN["магазин"] == LN['Дробить'], ["магазин", "Обороты за период", 'Дробить']] = [np.nan, np.nan, np.nan]
            LN = LN.loc[LN["магазин"].notnull()]
            LN['фаил'] = Name_file_col

            # region ДОП ТАБЛИЦА ДЛЯ ПОИСКА СТАТЕЙ
            LN_1 = LN[["Дробить", "фаил", "магазин", "номер склада"]]

            LN_1.to_excel(PUT + "ОБРАБОТАННЫЙ\\промежуточные\\" + Name_file_col + ".xlsx",index=False)
            # endregion

            LN= LN.pivot_table(index=['магазин', 'номер склада', 'фаил'], columns='Дробить', values='Обороты за период').reset_index()



            print(Name_file_col)
            print(Name_file)
            LN.to_csv(PUT + Name_file + ".csv", encoding="ANSI", sep=';',
                      index=False, decimal=',')

        # Поиск файлов текущих продаж. Список всех файлов в папке и подпапках
        all_files = []
        for root, dirs, files in os.walk(PUT + "ФИЕ\\"):
            for file in files:
                all_files.append(os.path.join(root, file))
        for i in all_files:
            LN = pd.read_excel(i)
            name_file = LN.iat[1, 1]
            Name_file = LN.columns[1][-24:] + "_44сч_" + name_file[8:-3]
            Name_file_col = LN.columns[1][-24:]
            LN = LN[["ИП Фукалов Игорь Евгеньевич", "Unnamed: 4"]]
            # создание новой строки с названиями столбцов
            LN.columns = ['Дробить', "Обороты за период"]
            LN = LN.iloc[8:]
            Spisok_magaz = RENAME().Rread()
            for i in Spisok_magaz:
                LN.loc[LN['Дробить'] == i, 'магазин'] = LN['Дробить']
            # Извлекаем номер склада из столбца "магазин" и создаем новый столбец "номер склада"
            LN['номер склада'] = LN['магазин'].str.extract('№(\d+)', expand=False)
            LN["магазин"] = LN["магазин"].ffill()
            LN['номер склада'] = LN['номер склада'].ffill()
            for i in ISKL:
                LN = LN.loc[LN["магазин"] != i]
            LN = LN.loc[LN['Дробить'] != 'Итого']
            LN.loc[LN["магазин"] == LN['Дробить'], ["магазин", "Обороты за период", 'Дробить']] = [np.nan, np.nan, np.nan]
            LN = LN.loc[LN["магазин"].notnull()]
            LN['фаил'] = Name_file_col

            # region ДОП ТАБЛИЦА ДЛЯ ПОИСКА СТАТЕЙ
            LN_1 = LN[["Дробить", "фаил", "магазин", "номер склада"]]

            LN_1.to_excel(PUT + "ОБРАБОТАННЫЙ\\промежуточные\\" + Name_file_col + ".xlsx",index=False)
            # endregion

            LN = LN.pivot_table(index=['магазин', 'номер склада', 'фаил'], columns='Дробить', values='Обороты за период').reset_index()

            print(Name_file_col)
            print(Name_file)
            LN.to_csv(PUT + Name_file + ".csv", encoding="ANSI", sep=';',
                      index=False, decimal=',')

        # Поиск файлов текущих продаж. Список всех файлов в папке и подпапках
        all_files = []
        for root, dirs, files in os.walk(PUT + "ФСА\\"):
            for file in files:
                all_files.append(os.path.join(root, file))
        for i in all_files:
            LN = pd.read_excel(i)
            name_file = LN.iat[1, 1]
            Name_file = LN.columns[1][-29:] + "_44сч_" + name_file[8:-3]
            Name_file_col = LN.columns[1][-29:]
            LN = LN[["ИП Фукалова Светлана Анатольевна", "Unnamed: 4"]]
            # создание новой строки с названиями столбцов
            LN.columns = ['Дробить', "Обороты за период"]
            LN = LN.iloc[8:]
            Spisok_magaz = RENAME().Rread()
            for i in Spisok_magaz:
                LN.loc[LN['Дробить'] == i, 'магазин'] = LN['Дробить']
            # Извлекаем номер склада из столбца "магазин" и создаем новый столбец "номер склада"
            LN['номер склада'] = LN['магазин'].str.extract('№(\d+)', expand=False)
            LN["магазин"] = LN["магазин"].ffill()
            LN['номер склада'] = LN['номер склада'].ffill()
            for i in ISKL:
                LN = LN.loc[LN["магазин"] != i]
            LN = LN.loc[LN['Дробить'] != 'Итого']
            LN.loc[LN["магазин"] == LN['Дробить'], ["магазин", "Обороты за период", 'Дробить']] = [np.nan, np.nan, np.nan]
            LN = LN.loc[LN["магазин"].notnull()]
            LN['фаил'] = Name_file_col
            # region ДОП ТАБЛИЦА ДЛЯ ПОИСКА СТАТЕЙ
            LN_1 =  LN[["Дробить","фаил","магазин","номер склада"]]
            LN_1.to_excel(PUT  + "ОБРАБОТАННЫЙ\\промежуточные\\" + Name_file_col + ".xlsx",
                         index=False)
            # endregion


            LN = LN.pivot_table(index=['магазин', 'номер склада', 'фаил'], columns='Дробить', values='Обороты за период').reset_index()
            print(Name_file_col)
            print(Name_file)
            LN.to_csv(PUT + Name_file + ".csv", encoding="ANSI", sep=';',
                      index=False, decimal=',')

        ITOGI = pd.DataFrame()
        all_files = []
        for file in os.listdir(PUT):
            full_path = os.path.join(PUT, file)
            if os.path.isfile(full_path):
                all_files.append(full_path)

        for i in all_files:
            print(i)
            Itog = pd.read_csv(i,encoding="ANSI",sep=';')
            ITOGI = pd.concat([ITOGI,Itog],axis=0).reset_index(drop=True)




        ITOGI = ITOGI.drop('фаил', axis=1)
        print(ITOGI)
        # Получить список всех названий столбцов
        all_columns = ITOGI.columns.tolist()

        # Исключить из списка нужные столбцы
        exclude_columns = ['номер склада', 'магазин']
        columns_to_sum = [column for column in all_columns if column not in exclude_columns]
        print(columns_to_sum)
        FLOAT().float_colms(name_data=ITOGI, name_col=columns_to_sum)
        ITOGI = ITOGI.groupby(["магазин", ],
                              as_index=False).agg(
            {col: 'sum' for col in columns_to_sum}).reset_index(drop=True)

        # считываем названия столбцов из Excel-файла
        cols = pd.read_excel(PUT + "Условия сложения\\Итого ФОТ на 44 сч.xlsx")
        cols = cols.iloc[:, 0].tolist()
        if set(cols).issubset(set(ITOGI.columns)):
            # столбцы из cols содержатся в ITOGI.columns
            print("Все столбцы есть Итого ФОТ на 44 сч")
        else:
            # некоторые столбцы отсутствуют, нужно создать их
            missing_cols = set(cols) - set(ITOGI.columns)
            for col in missing_cols:
                ITOGI[col] = 0
        # складываем столбцы с нужными названиями и сохраняем результат в новом столбце
        ITOGI['Итого ФОТ на 44 сч'] = ITOGI[cols].sum(axis=1)


        # считываем названия столбцов из Excel-файла
        cols = pd.read_excel(PUT + "Условия сложения\\Итого ТРАНСПОРТНЫЕ.xlsx")
        cols = cols.iloc[:, 0].tolist()
        if set(cols).issubset(set(ITOGI.columns)):
            # столбцы из cols содержатся в ITOGI.columns
            print("Все столбцы есть Итого ТРАНСПОРТНЫЕ")
        else:
            # некоторые столбцы отсутствуют, нужно создать их
            missing_cols = set(cols) - set(ITOGI.columns)
            for col in missing_cols:
                ITOGI[col] = 0
        # складываем столбцы с нужными названиями и сохраняем результат в новом столбце
        ITOGI['Итого ТРАНСПОРТНЫЕ'] = ITOGI[cols].sum(axis=1)

        # считываем названия столбцов из Excel-файла
        cols = pd.read_excel(PUT + "Условия сложения\\Итого ТМЦ.xlsx")
        cols = cols.iloc[:, 0].tolist()
        if set(cols).issubset(set(ITOGI.columns)):
            # столбцы из cols содержатся в ITOGI.columns
            print("Все столбцы есть Итого ТМЦ")
        else:
            # некоторые столбцы отсутствуют, нужно создать их
            missing_cols = set(cols) - set(ITOGI.columns)
            for col in missing_cols:
                ITOGI[col] = 0

        # складываем столбцы с нужными названиями и сохраняем результат в новом столбце
        ITOGI['Итого ТМЦ'] = ITOGI[cols].sum(axis=1)

        # считываем названия столбцов из Excel-файла
        cols = pd.read_excel(PUT + "Условия сложения\\Итого Прочие прямые.xlsx")
        cols = cols.iloc[:, 0].tolist()
        if set(cols).issubset(set(ITOGI.columns)):
            # столбцы из cols содержатся в ITOGI.columns
            print("Все столбцы есть Итого Прочие прямые")
        else:
            # некоторые столбцы отсутствуют, нужно создать их
            missing_cols = set(cols) - set(ITOGI.columns)
            for col in missing_cols:
                ITOGI[col] = 0
        # складываем столбцы с нужными названиями и сохраняем результат в новом столбце
        ITOGI['Итого Прочие прямые'] = ITOGI[cols].sum(axis=1)

        # считываем названия столбцов из Excel-файла
        cols = pd.read_excel(PUT + "Условия сложения\\Без названия.xlsx")
        cols = cols.iloc[:, 0].tolist()
        if set(cols).issubset(set(ITOGI.columns)):
            # столбцы из cols содержатся в ITOGI.columns
            print("Все столбцы есть Без названия")
        else:
            # некоторые столбцы отсутствуют, нужно создать их
            missing_cols = set(cols) - set(ITOGI.columns)
            for col in missing_cols:
                ITOGI[col] = 0
        # складываем столбцы с нужными названиями и сохраняем результат в новом столбце
        ITOGI['итого з-ты без маркетинга, ремонтов, оборудования'] = ITOGI[cols].sum(axis=1)

        # считываем названия столбцов из Excel-файла
        cols = pd.read_excel(PUT + "Условия сложения\\Итого Реклама.xlsx")
        cols = cols.iloc[:, 0].tolist()
        if set(cols).issubset(set(ITOGI.columns)):
            # столбцы из cols содержатся в ITOGI.columns
            print("Все столбцы есть Без названия")
        else:
            # некоторые столбцы отсутствуют, нужно создать их
            missing_cols = set(cols) - set(ITOGI.columns)
            for col in missing_cols:
                ITOGI[col] = 0
        # складываем столбцы с нужными названиями и сохраняем результат в новом столбце
        ITOGI['Итого Реклама'] = ITOGI[cols].sum(axis=1)

        ITOGI = ITOGI.rename(columns={'магазин': 'Магазин', 'номер склада': '№ скл'})

        # считываем порядок столбцов из файла Excel
        cols_order = pd.read_excel(PUT + "Условия сложения\\Порядок.xlsx", header=None)[0].tolist()

        # переупорядочиваем столбцы в исходном датафрейме в нужном порядке
        ITOGI = ITOGI.reindex(columns=cols_order)

        ITOGI = ITOGI.drop('названия столбцов', axis=1)
        # порядок столбцов


        # Получить список всех названий столбцов
        all_columns = ITOGI.columns.tolist()

        # Исключить из списка нужные столбцы
        exclude_columns = ['Магазин', '№ скл',"Канал","Без названия","Итого Прочие прямые","Итого Реклама","Итого ТМЦ","Итого ТРАНСПОРТНЫЕ","Итого ФОТ на 44 сч"]
        columns_to_sum = [column for column in all_columns if column not in exclude_columns]
        print(columns_to_sum)
        FLOAT().float_colms(name_data=ITOGI, name_col=columns_to_sum)

        ITOGI['ИТОГО'] = ITOGI[columns_to_sum].sum(axis=1)


        ITOGI  = pd.concat([ITOGI, pd.DataFrame(ITOGI.sum(numeric_only=True), columns=['Итого']).T]).reset_index(drop=True)



        # Сохранение названий столбцов
        column_names = ITOGI.columns.tolist()
        # Добавление номеров столбцов в первую строку
        ITOGI.loc[-1] = range(ITOGI.shape[1])
        ITOGI.index = ITOGI.index + 1
        ITOGI = ITOGI.sort_index()

        # Восстановление названий столбцов
        ITOGI.columns = column_names

        ITOGI.loc[ITOGI["Магазин"] == 0, "ИТОГО"] = np.nan



        # Извлекаем номер склада из столбца "магазин" и создаем новый столбец "номер склада"
        ITOGI['№ скл'] = ITOGI['Магазин'].str.extract('№(\d+)', expand=False)

        # Создаем новый столбец "содержит_франшизу", который будет содержать булевую маску
        mask = ITOGI['Магазин'].fillna('not_found').str.contains('Франшиза Склад', case=False)
        # Используем метод loc для установки значения "номер склада"
        ITOGI.loc[mask & ~ITOGI['№ скл'].isna(), '№ скл'] = ITOGI.loc[mask & ~ITOGI['№ скл'].isna(), '№ скл'] + 'Ф'
        ITOGI['№ скл'] = ITOGI['№ скл'].astype('str')


        ITOGI.to_excel(PUT + "ОБРАБОТАННЫЙ\\Обработанный" + ".xlsx", index=False)


        all_files = []
        combain = pd.DataFrame()
        for root, dirs, files in os.walk(PUT + "ОБРАБОТАННЫЙ\\промежуточные\\"):
            for file in files:
                all_files.append(os.path.join(root, file))
        for i in all_files:
            print(i)
            x = pd.read_excel(i)
            x = x.rename(columns={'Дробить': 'Статья', "фаил": "Юр.лицо", 'магазин': 'Магазин', 'номер склада': '№ скл'})
            print(x)
            combain = pd.concat([combain,x],axis=0)



        combain.to_excel(PUT + "ОБРАБОТАННЫЙ\\Для поиска сатей" + ".xlsx",index=False)


Obrabotka().poisk()






