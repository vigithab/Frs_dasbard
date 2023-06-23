import pandas as pd
import os
import datetime as dt

pd.set_option("expand_frame_repr", False)
pd.set_option('display.max_colwidth', None)

combined_zo = pd.DataFrame()
path_zo = r'P:\Фирменная розница\ФРС\Данные из 1 С\Отчет по продажам\По дням\2023'
for f_zo in os.listdir(path_zo):
    file_zo = path_zo + "\\" + f_zo
    df = pd.read_csv(file_zo, sep="\t", parse_dates=['Дата'], dayfirst=True, date_format="%d.%m.%Y")
    date_str = df['Дата'].unique()
    for date in date_str:
        df["Дата/Время чека"] = pd.to_datetime(df['Дата'], format="%d.%m.%Y")
        day_df = df.loc[df['Дата'] == pd.to_datetime(date, format="%d.%m.%Y")]
        name_fail = os.path.basename(file_zo)
        print(name_fail)
        print(day_df)
        input('ddd')


        file_name = os.path.join(PUT + "♀️Сибестоемость\\Текущий месяц\\", date + ".csv")
        day_df.to_csv(file_name, sep=";", encoding="utf-8", decimal=".", index=False)

    """   spisok_dat_1 = df_zo['Дата'].drop_duplicates().to_list()
    df_zo['Дата1'] = df_zo['Дата'].astype('datetime64[ns]')
    df_zo['Дата2'] = df_zo['Дата1'].dt.strftime("%d.%m.%Y")
    df_zo['Дата3'] = df_zo['Дата1'].dt.strftime("%m.%d.%Y")
    df_zo['Дата4'] = df_zo['Дата1'].dt.strftime("%d.%m.%Y")
    df_zo['Дата5'] = pd.to_datetime(df_zo['Дата1'], format("%d.%m.%Y"))
    df_zo['Дата6'] = pd.to_datetime(df_zo['Дата1'])
    df_zo["Дата/Время чека"] = pd.to_datetime(df_zo["Дата"], format="%d.%m.%Y")
    ##    day_df = df.loc[df["Дата/Время чека"] == pd.to_datetime(date, format="%d.%m.%Y")]
    ##    file_name = os.path.join(PUT + "♀️Сибестоемость\\Текущий месяц\\", date + ".csv")    day_df.to_csv(file_name, sep=";", encoding="utf-8", decimal=".", index=False)
    print(df_zo.head())
    spisok_dat = df_zo['Дата'].drop_duplicates().to_list()
    path_zo_to = r'P:\Фирменная розница\ФРС\Данные из 1 С\Отчет по продажам\По дням\2023 N'
    print(spisok_dat)
    for d in spisok_dat:
        tablex = df_zo.copy()
        tablex = tablex.loc[tablex['Дата'] == d]
        den = str(d)
        distination = path_zo_to + '\\' + den + '.txt'
        ##        tablex.to_csv(distination,sep='\t',index=False,decimal=',')
        input('ddd')"""

