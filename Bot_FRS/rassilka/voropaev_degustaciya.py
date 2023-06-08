import pandas as pd
import os
import datetime as dt
import numpy as np
from Bot_FRS.Goo import Googl as g
from Bot_FRS.bot_telegram import Bot as bot
from Bot_FRS.inf import NASTROYKA as setting
pd.set_option("expand_frame_repr", False)
pd.set_option('display.max_colwidth', None)

PUT= setting.PUT

class RENAME:
    def Rread(self, name_data, name_col, name):
        print("Загрузка справочника магазинов...")
        while True:
            try:
                replacements = pd.read_excel("https://docs.google.com/spreadsheets/d/1SfuC2zKUFt6PQOYhB8EEivRjy4Dz-o4WDL-IR7CT3Eg/export?exportFormat=xlsx")
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
class Degustacia:
    def sotka(self):
        if setting.time_seychas <setting.time_voropaev_vrem:
            bot.BOT().bot_mes_html(mes="Оновление таблицы шашлыка", silka=0)
            file = PUT + 'NEW\\Дегустации\\Отчет по дегустациям - X (TXT).txt'
            replacements = pd.read_excel(r'https://docs.google.com/spreadsheets/d/1SfuC2zKUFt6PQOYhB8EEivRjy4Dz-o4WDL-IR7CT3Eg/export?exportFormat=xlsx')
            rng = len(replacements)
            #########Убираем лишние столбцы в справочнике, оставляем только рабочие магазины.
            sprq_tt = pd.read_excel(r'https://docs.google.com/spreadsheets/d/1qXyD0hr1sOzoMKvMyUBpfTXDwLkh0RwLcNLuiNbWmSM/export?exportFormat=xlsx')
            sprq_tt = sprq_tt[['!МАГАЗИН!', 'Старые/Новые']]
            sprq_tt = sprq_tt.loc[sprq_tt['Старые/Новые'] != 'ЗАКРЫТЫЕ']
            sprq_tt.columns = ['Магазин', 'Старые/Новые']
            sprq_tt = sprq_tt.dropna(subset='Старые/Новые')

            #########Работаем с файлом дегустации
            df = pd.read_csv(file, sep="\t", skiprows=4)

            df.columns = ['Магазин', 'Номенклатура', 'Дата дегустации', 'Входит в группу', 'Время начала дегустации', 'Время окончания дегустации',
                          'Количество продано, кг', 'Сумма продаж, руб', 'Наценка руб.',
                          'Количество списано, кг', 'Сумма списания, руб', 'Процент списаний',
                          'Количество чеков всего', 'Количество чеков с товаром', 'Доля чеков с дегустацией']


            df['Дата дегустации'] = df['Дата дегустации'].astype(str).apply(lambda x: (x.replace(' г.', '').replace(u'\xa0', u'')))
            df['Дата дегустации'] = pd.to_datetime(df['Дата дегустации'], dayfirst=True)
            df['Время начала дегустации'] = pd.to_datetime(df['Время начала дегустации'], dayfirst=True)
            df['Время окончания дегустации'] = pd.to_datetime(df['Время окончания дегустации'], dayfirst=True)

            ###########ПРоверяем шашлык это или нет
            """df['Est shahsl'] = np.where(df['Номенклатура'].str.contains('Шашл', regex=True), "Y",
                                        np.where(df['Входит в группу'].str.contains('100', regex=True), "Y",
                                                 np.where(df['Входит в группу'].str.contains('Шашл', regex=True), "Y",
                                                          np.where(df['Входит в группу'].str.extract('(200.07 Гриль \(Шашлык на шпажке\))', expand=False).notna(), "Y", "N"))))"""

            spisok_shash = ['Купаты Барбекю, охл, 0,5 кг, шт', 'Купаты куриные, охл, 0,5 кг, шт', 'Колбаски для гриля Улитка, охл, 0,5 кг, шт',
                            'Колбаски для гриля Ассорти, охл, 0,5 кг, шт', 'Сердце цыпленка-бройлера (шашлык из сердечек), охл, 0,4 кг, шт',
                            'Шашлык из индейки в маринаде, охл, 0,35 кг, шт', 'Колбаски Свиные с вяленными томатами, вар, в/у, охл, 0,3 кг, шт',
                            'Колбаски Свиные с сыром, вар, в/у, охл, 0,3 кг, шт', 'Колбаски для гриля (с соусом Терияки), вар, в/у, охл, 0,3 кг, шт',
                            'Колбаски для гриля (луковые), вар, в/у, охл, 0,3 кг, шт', 'Колбаски Мексиканские, охл, в/у, 0,4 кг, шт',
                            'Колбаски Нежные, охл, в/у, 0,4 кг, шт']

            df['Est shahsl'] = np.where(df['Номенклатура'].str.contains('Р/К', regex=True), "N",
                                   np.where(df['Входит в группу'].str.contains('191.15 Сэндвичи', regex=True), "N",
                                            np.where(df['Номенклатура'].str.contains('Шашл', regex=True), "Y",
                                                     np.where(df['Входит в группу'].str.contains('100', regex=True), "Y",
                                                              np.where(df['Входит в группу'].str.contains('Шашл', regex=True), "Y",
                                                                       np.where(df['Входит в группу'].str.contains(
                                                                           '200.07 Гриль (Шашлык на шпажке)', regex=True), "Y",
                                                                           np.where(df['Номенклатура'].isin(spisok_shash), "Y",

                                                                                    "N")))))))


            #####Замена имен
            for i in range(rng):
                df['Магазин'] = df['Магазин'].str.replace(replacements['НАЙТИ'][i],
                                                          replacements['ЗАМЕНИТЬ'][i],
                                                          regex=False)
                #####Оставляем только ШАШ и только последние 7 дней
            df = df.loc[df['Est shahsl'] == 'Y']
            df = df.loc[df['Входит в группу'] != '191.15 Сэндвичи']
            df['day'] = (dt.datetime.now() - df['Дата дегустации']).dt.days
            df = df.loc[df['day'] <= 7] \
                ####ID дегустации для подсчета наличия дегустаций
            df['ID'] = df['Дата дегустации'].astype(str) + df['Номенклатура'].astype(str)

            ########    Группируем для подсчета кол-ва дегустаций
            agg_func_count = {'ID': ['nunique']}
            table = df.groupby(['Магазин'], as_index=False).agg(agg_func_count)
            table.columns = ['_'.join(col).rstrip('_') for col in table.columns.values]
            table.columns = ['Магазин', 'Количество дегустации']
            ######Дроп ненужные строки
            df = df.drop(columns=['day', 'Est shahsl', 'ID'])
            sprq_tt = sprq_tt.merge(table, on='Магазин', how="left")

            sprq_tt['del'] = np.where(np.isnan(sprq_tt['Количество дегустации']), 'y', 'n')
            sprq_tt = sprq_tt.loc[sprq_tt['del'] == 'y']
            sprq_tt = sprq_tt.drop(columns=['Старые/Новые', 'del'])
            all_columns = df.columns.tolist()

            # Исключить из списка нужные столбцы
            exclude_columns = ['Магазин', 'Номенклатура', "Входит в группу", "Время начала дегустации", "Время окончания дегустации", "Процент списаний",
                               "Доля чеков с дегустацией", 'Дата дегустации']
            columns_to_sum = [column for column in all_columns if column not in exclude_columns]
            ######        print(columns_to_sum)
            df['Дата дегустации'] = df['Дата дегустации'].dt.strftime('%Y-%m-%d')
            df['Время начала дегустации'] = df['Время начала дегустации'].dt.strftime('%H:%M')
            df['Время окончания дегустации'] = df['Время окончания дегустации'].dt.strftime('%H:%M')
            FLOAT().float_colms(name_data=df, name_col=columns_to_sum)

            ty = RENAME().TY_Spravochnik()
            ty = ty.rename(columns={"!МАГАЗИН!": "Магазин"})
            df = df.merge(ty, on=["Магазин"], how="left").reset_index(drop=True)

            # df = pd.concat([df, pd.DataFrame(df.sum(numeric_only=True), columns=['Итого']).T]).reset_index(drop=True)
            df = pd.concat([df, pd.DataFrame(df.sum(numeric_only=True), columns=['Итого']).T.assign(Магазин='ИТОГО')]).reset_index(drop=True)
            df.fillna('', inplace=True)

            g.tbl().record(name="Дегустация шашлыка(за последние 7 дней)", name_df=df, sheet_name="ЕСТЬ ДЕГУСТАЦИИ")
            sprq_tt.fillna('', inplace=True)

            ty = RENAME().TY_Spravochnik()
            ty = ty.rename(columns={"!МАГАЗИН!": "Магазин"})
            sprq_tt = sprq_tt.merge(ty, on=["Магазин"], how="left").reset_index(drop=True)
            sprq_tt.fillna('', inplace=True)
            g.tbl().record(name="Дегустация шашлыка(за последние 7 дней)", name_df=sprq_tt, sheet_name="НЕТ ДЕГУСТАЦИЙ")

#Degustacia().sotka()