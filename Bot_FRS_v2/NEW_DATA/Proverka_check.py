import pandas as pd
from Bot_FRS_v2.INI import ini
from Bot_FRS_v2.INI import log
from Bot_FRS_v2.INI import rename
from Bot_FRS_v2.INI import memory
from Bot_FRS_v2.INI import Float

import os
import shutil
import zipfile
import datetime

pd.set_option("expand_frame_repr", False)
pd.set_option('display.max_colwidth', None)

PUT = ini.PUT

class data():
    def new(self):
        zip  =r"\\rtlfranch3\Данные из 1С\Для Дашборда\Проверка Сетретейл-1С(потерянные чеки)"
        not_zip = PUT + "NEW\\Проверки_чеков\\"
        # Получение списка файлов в заданной директории
        files = os.listdir(zip)
        # Фильтрация списка файлов для получения только ZIP-архивов
        zip_files = [file for file in files if file.endswith('.zip')]
        # Создание списка пар (время изменения, имя файла)
        file_times = [(os.path.getmtime(os.path.join( zip, file)), file) for file in zip_files]
        # Сортировка списка пар по времени изменения (последний измененный файл будет первым)
        file_times.sort(reverse=True)
        # Получение пути к последнему измененному ZIP-архиву
        last_modified_zip = os.path.join( zip, file_times[0][1])
        # Имя файла
        name_fail = os.path.basename(last_modified_zip)
        # Копирование ZIP-файла в указанный путь
        shutil.copy(last_modified_zip, not_zip)
        # Распаковка файла
        zip_files = os.path.join(not_zip, name_fail)
        print(zip_files)

        # Разархивирование файла
        with zipfile.ZipFile(zip_files, 'r') as zip_ref:
            zip_ref.extractall(not_zip)
        # Удаление архива
        os.remove(zip_files)
        not_zip = PUT + "NEW\\Проверки_чеков\\"
        files = os.listdir(not_zip)
        for file in files:
            if file.endswith('.txt'):
                txt_fil = os.path.join(not_zip, file)
                one = pd.read_csv(txt_fil, sep="\t", encoding="utf-8", skiprows=8, names=["Магазин", "Номер чека", "Дата чека.Начало дня",
                                                                                          "Касса (ККМ).Код", "Документ.Номер смены ККМ", "Выручка"], dtype={"Касса (ККМ).Код": str})
                one = one.loc[one["Дата чека.Начало дня"].notnull()]
                one = one.rename(columns={"Магазин": "!МАГАЗИН!", "Касса (ККМ).Код": "Касса", "Номер чека": "Чек", "Дата чека.Начало дня": 'Дата/Время чека',
                                          "Документ.Номер смены ККМ": "Смена", "Выручка": "Выручка_1c"})
                print(one)
                rename.RENAME().Rread(name_data=one, name_col="!МАГАЗИН!", name="one")
                print(one)
                # удаление микромаркетов
                l_mag = ("Микромаркет", "Экопункт", "Вендинг", "Итого")
                for w in l_mag:
                    one = one[~one["!МАГАЗИН!"].str.contains(w)].reset_index(drop=True)

                one.to_csv(PUT + "NEW\\Проверки_чеков\\Проверка_чеков.csv", sep="\t", encoding="utf-8",decimal=".", index=False)
                os.remove(txt_fil)

                one["Дата/Время чека"] = pd.to_datetime(one["Дата/Время чека"], format='%d.%m.%Y')
                unique_dates = one["Дата/Время чека"].unique()
                formatted_dates = [date.strftime('%d.%m.%Y') for date in unique_dates]
                with open(PUT + "NEW\\Проверки_чеков\\Даты_в файле\\Даты.txt", 'w') as f:
                    f.write(str(formatted_dates))
                print(formatted_dates)
    def one_c(self,date):
        # Преобразование строки даты в объект datetime
        date = datetime.datetime.strptime(date, '%d.%m.%Y')
        # Изменение формата даты на 'гггг-мм-дд'
        formatted_date = date.strftime('%Y-%m-%d')
        print(formatted_date)
        not_zip = PUT + "NEW\\Проверки_чеков\\"
        files = os.listdir(not_zip)
        for file in files:
            if file.endswith('.csv'):
                txt_fil = os.path.join(not_zip, file)
                one = pd.read_csv(txt_fil,sep="\t", encoding="utf-8", dtype={"Касса (ККМ).Код": str})

                one ["Дата/Время чека"] = pd.to_datetime(one ["Дата/Время чека"], format='%d.%m.%Y')
                one=one.loc[one["Дата/Время чека"]==formatted_date]
                one.to_excel(PUT + "NEW\\Проверки_чеков\\Чеки 1 с разбитые\\" + formatted_date + ".xlsx", index=False)
                print(one)
                Float.FLOAT().float_colm(name_data=one, name_col="Выручка_1c")
                one_sum = one["Выручка_1c"].sum()
                one_count_chek = one["Чек"].count()
                rename.RENAME().Rread_kassa(name_data=one, name_col="Касса", name="one")

                return one, one_sum,one_count_chek
    def one_c_publik(self,date):
        # Преобразование строки даты в объект datetime
        #date = datetime.datetime.strptime(date, '%d.%m.%Y')
        # Изменение формата даты на 'гггг-мм-дд'
        #formatted_date = date.strftime('%Y-%m-%d')
        #publik = r"\\tw1\PUBLIC\Фирменная розница\ФРС\Данные из 1 С\Чеки New\2023\Май"
        publik = PUT + "NEW\\Проверки_чеков\\Май\\"
        file_extension = ".txt"
        file_name = date + file_extension
        file_path = os.path.join(publik, file_name)
                #txt_fil = os.path.join(publik, file)
        one = pd.read_csv(file_path,sep="\t", encoding="utf-8", dtype={"Касса (ККМ).Код": str})

        one = one.loc[one["Дата"].notnull()]
        one = one[["Дата","Магазин","Номер чека","Номер кассы","Выручка"]]
        one = one.rename(columns={"Магазин": "!МАГАЗИН!", "Номер кассы": "Касса", "Номер чека": "Чек", "Дата": 'Дата/Время чека',"Выручка": "Выручка_1c"})
        rename.RENAME().Rread(name_data=one, name_col="!МАГАЗИН!", name="one")

        # удаление микромаркетов
        l_mag = ("Микромаркет", "Экопункт", "Вендинг", "Итого")
        for w in l_mag:
            one = one[~one["!МАГАЗИН!"].str.contains(w)].reset_index(drop=True)
        Float.FLOAT().float_colm(name_data=one, name_col="Выручка_1c")
        one_sum_g1 = one["Выручка_1c"].sum()

        one = one.groupby(["!МАГАЗИН!", "Чек", "Дата/Время чека", "Касса"], as_index=False) \
            .agg({"Выручка_1c": "sum"})
        one_sum_g2 = one["Выручка_1c"].sum()
        print(one_sum_g1)
        print(one_sum_g2)
        one ["Дата/Время чека"] = pd.to_datetime(one ["Дата/Время чека"], format='%d.%m.%Y')

        Float.FLOAT().float_colm(name_data=one, name_col="Выручка_1c")
        one_sum = one["Выручка_1c"].sum()
        one_count_chek = one["Чек"].count()
        rename.RENAME().Rread_kassa(name_data=one, name_col="Касса", name="one")
        return one, one_sum,one_count_chek
    def setreteyl(self):
        folder1 = PUT + "Selenium\\исходники\\"
        file_extension = ".xlsx"
        Non_chek = pd.DataFrame()
        formatted_dates= ini.last_mount()
        print(formatted_dates)
        # Проход по списку форматированных дат
        for date in formatted_dates:
            date= str(date)
            #date = date[1:-1]
            one, one_sum, one_count_chek = data().one_c_publik(date=date)
            file_name = date + file_extension
            file_path = os.path.join(folder1, file_name)
            x = pd.read_excel(file_path)

            x[['Дата', 'Время']] = x['Дата/Время чека'].str.split(' ', expand=True)
            x["Дата/Время чека"] = pd.to_datetime(x['Дата'], format='%d.%m.%Y')

            spqr, sprav_magaz = rename.RENAME().magazin_info()
            x = x.rename(columns={"Магазин": 'ID',"Стоимость позиции":"Выручка_set"})
            x = x.merge(spqr[['!МАГАЗИН!', 'ID']], on='ID', how="left")
            x = x.loc[x["Тип"]=="Продажа"]
            x = x[["Тип","Дата/Время чека","ID","Касса", "Смена","Чек","Выручка_set","Сумма скидки","!МАГАЗИН!",'Время']]
            # удаление микромаркетов
            l_mag = ("Микромаркет", "Экопункт", "Вендинг", "Итого")
            for w in l_mag:
                x =  x[~x["!МАГАЗИН!"].str.contains(w)].reset_index(drop=True)

            Float.FLOAT().float_colm(name_data=x, name_col="Сумма скидки")
            Float.FLOAT().float_colm(name_data=x, name_col="Выручка_set")

            """x = x.groupby(["!МАГАЗИН!","Чек","Дата/Время чека", "Касса", "Смена"], as_index=False) \
                .agg({"Выручка_set": "sum",
                      'Сумма скидки': "sum"})"""

            x = x.groupby(["!МАГАЗИН!", "Чек", "Дата/Время чека", "Касса"], as_index=False) \
                .agg({"Выручка_set": "sum",
                      'Сумма скидки': "sum"})


            x_sum = x["Выручка_set"].sum()
            x_count_chek = x["Чек"].count()
            log.log_file(date,"1c выручка: "+ str(one_sum),"  сет выручка: " + str(x_sum),"  разница: " + str(x_sum - one_sum),1)
            log.log_file(date,"1 cчеки: "+  str(one_count_chek),"  сет чеки: " + str(x_count_chek),"  разница: " +str(x_count_chek - one_count_chek), 0)

            x['Касса'] = x['Касса'].astype(float).apply(lambda x: '{:.0f}'.format(x))
            x["Чек"] = x["Чек"].astype(float).apply(lambda x: '{:.0f}'.format(x))
            #ln = ["Чек","Касса","Смена"]
            ln = ["Чек", "Касса",]
            for i in ln:
                x[i] = x[i].astype("str")
            for i in ln:
                one[i] = one[i].astype("str")

            #union = pd.merge(x,one, on=["!МАГАЗИН!","Чек","Дата/Время чека", "Касса", "Смена"], how="outer")
            union = pd.merge(x, one, on=["!МАГАЗИН!", "Чек", "Дата/Время чека", "Касса"], how="outer")

            union["разница"] = union["Выручка_set"]- union["Выручка_1c"]
            union_raz = union.loc[union["разница"].round(0)!=0]

            union_non = union.loc[union["Выручка_1c"].isnull()]
            Non_chek = pd.concat([Non_chek,union_non], axis=0)

            union_sum_one = union["Выручка_1c"].sum()
            union_sum_set = union["Выручка_set"].sum()

            log.log_file(date, "До групировки 1c " + str(one_sum), "  после: " + str(union_sum_one), "разница : " + str(one_sum-union_sum_one), 1)
            log.log_file(date, "До групировки 1c " + str(x_sum), "  после: " + str(union_sum_set), "разница : " + str(x_sum - union_sum_set), 0)

            union1 = union.loc[union["Выручка_set"].isnull()]
            union1 = union1.groupby(["!МАГАЗИН!", "Дата/Время чека", "Касса"], as_index=False) \
                .agg({"Выручка_1c": "sum"})

            union2 = union.loc[union["Выручка_1c"].isnull()]
            union2 = union2.groupby(["!МАГАЗИН!", "Дата/Время чека", "Касса"], as_index=False) \
                .agg({"Выручка_set": "sum"})

            union_kassa = pd.merge(union2, union1, on=["!МАГАЗИН!", "Дата/Время чека","Касса"], how="outer")
            print(union1)
            print(union2)
            #set = pd.concat([set,x],axis=0)
            union_kassa.to_excel(PUT + "NEW\\Проверки_чеков\\Обработанные\\Сопоставелние касс\\" + date + ".xlsx", index=False)
            union_raz.to_excel(PUT +"NEW\\Проверки_чеков\\Обработанные\\По дням\\" + date + ".xlsx", index=False)
        Non_chek.to_excel(PUT + "NEW\\Проверки_чеков\\Обработанные\\нет чеков.xlsx", index=False)
        data().union()
        return
    def union(self):
        con = PUT + "NEW\\Проверки_чеков\\Обработанные\\По дням\\"
        files = os.listdir(con)
        Non_chek_raz = pd.DataFrame()
        for file in files:
            if file.endswith('.xlsx'):
                file_path = os.path.join(con,  file)
                print(file_path)
                x = pd.read_excel(file_path)
                Non_chek_raz = pd.concat([Non_chek_raz, x], axis=0)

        Non_chek_raz.to_excel(PUT + "NEW\\Проверки_чеков\\Обработанные\\нет чеков и разница.xlsx", index=False)



        return
#data().one_c()
#data().setreteyl()
#data().union()
#data().new()