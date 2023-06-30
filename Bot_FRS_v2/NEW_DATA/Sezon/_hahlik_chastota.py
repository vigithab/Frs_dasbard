import pandas as pd
import numpy as np
import os
import datetime as dt
from Bot_FRS_v2.BOT_TELEGRAM import BOT
from Bot_FRS_v2.INI import ini
import time
# try :
pd.set_option("expand_frame_repr", False)
pd.set_option('display.max_colwidth', None)

BOT.BOT().bot_mes_html(mes="Скрипт Дашборда запущен",silka=0)
nachalo = dt.datetime.now()
tek_m=dt.datetime.now().month
##if tek_d==1 :
##    nuzhen_m="0"+str(tek_m-1)
##    spisok_m_number.append(nuzhen_m)
##else :
##    nuzhen_m="0"+str(tek_m)
##    spisok_m_number.append(nuzhen_m)



# ОБНОВИТЬ В РУЧНУЮ В НАЧАЛЕ МЕСЯЦА
#spisok_m_number = ['07']
spisok_m_number=['04','05',"06"]


spisok_shash=['Купаты Барбекю, охл, 0,5 кг','Купаты куриные, охл, 0,5 кг','Колбаски для гриля Улитка, охл, 0,5 кг',\
              'Колбаски для гриля Ассорти, охл, 0,5 кг','Сердце цыпленка-бройлера (шашлык из сердечек), охл, 0,4 кг',\
              'Шашлык из индейки в маринаде, охл, 0,35 кг','Колбаски Свиные с вяленными томатами, вар, в/у, охл, 0,3 кг',\
              'Колбаски Свиные с сыром, вар, в/у, охл, 0,3 кг','Колбаски для гриля (с соусом Терияки), вар, в/у, охл, 0,3 кг',\
              'Колбаски для гриля (луковые), вар, в/у, охл, 0,3 кг','Колбаски Мексиканские, охл, в/у, 0,4 кг','Колбаски Нежные, охл, в/у, 0,4 кг']

replacements = pd.read_excel(
    r'https://docs.google.com/spreadsheets/d/1SfuC2zKUFt6PQOYhB8EEivRjy4Dz-o4WDL-IR7CT3Eg/export?exportFormat=xlsx')
rng = len(replacements)

spr = pd.read_csv(ini.PUT + "Справочники\\номенклатура\\Справочник номеклатуры.txt",
    sep='\t', skiprows=1)
spr.columns = ['Владелец', 'Входит в группу', 'Срок годности', 'Классификатор для infovizion', 'Штрихкод']
spr['Shsh'] = np.where(spr['Владелец'].str.contains('Р/К', regex=True), "N", \
                       np.where(spr['Входит в группу'].str.contains('191.15 Сэндвичи', regex=True), "N", \
                                np.where(spr['Владелец'].str.contains('Шашл', regex=True), "Y", \
                                         np.where(spr['Входит в группу'].str.contains('100', regex=True), "Y", \
                                                  np.where(spr['Входит в группу'].str.contains('Шашл', regex=True), "Y",
                                                           np.where(spr['Входит в группу'].str.contains(
                                                               '200.07 Гриль (Шашлык на шпажке)', regex=True), "Y",
                                                                    np.where(spr['Владелец'].isin(spisok_shash), "Y",
                                                                        "N")))))))

spr['Штрихкод'] = spr['Штрихкод'].astype(str)

spr = spr.dropna(subset='Входит в группу')
spr["Владелец"] = spr["Владелец"].astype(str).apply(lambda x: (x.replace('Не исп ', '')))
spr["Владелец"] = spr["Владелец"].astype(str).apply(lambda x: (x.replace('не исп ', '')))
spr['Входит в группу'] = spr['Входит в группу'].astype(str).apply(lambda x: (x.replace(' ВЫВЕДЕННЫЕ', '')))
spr = spr[['Владелец', 'Входит в группу', 'Штрихкод','Shsh']]
spr.columns = ['Номенклатура', 'Входит в группу', 'Штрихкод','Shsh']
spr_shash=spr.copy()
spr_shash = spr_shash.loc[spr_shash['Shsh'] == "Y"]
spr_list=spr_shash['Номенклатура'].drop_duplicates().to_list()
##print(spr_list)
##spr.to_csv('SPQR.txt', sep='\t')
spr = spr[['Номенклатура', 'Входит в группу', 'Штрихкод']]

######################################################2023################################################################
path_cheks = r'P:\Фирменная розница\ФРС\Данные из 1 С\Чеки Set'


combined_ch = pd.DataFrame()
for f_ch in os.listdir(path_cheks):
    m = f_ch[3:5]
    if m in spisok_m_number:
        file_ch = path_cheks + "\\" + f_ch
        print(f_ch, 'yeaaaah bitch')
        df_ch = pd.read_csv(file_ch,sep='\t')
        df_ch = df_ch[['Тип', 'Дата/Время чека', 'Магазин', 'Касса','Смена', 'Чек', 'Сумма чека', 'Сумма скидки чека', 'Штрихкод', \
                       'Наименование товара', 'Количество', 'Цена', 'Процент скидки', 'Сумма скидки', 'Стоимость позиции',
                       'Магазин 1C']]
        for i in range(rng):
            df_ch['Магазин 1C'] = df_ch['Магазин 1C'].replace(replacements['НАЙТИ'][i], \
                                                                  replacements['ЗАМЕНИТЬ'][i], \
                                                                  regex=False)
        df_ch["Наименование товара"] = df_ch["Наименование товара"].astype(str).apply(lambda x: (x.replace('Не исп ', '')))
        df_ch["Наименование товара"] = df_ch["Наименование товара"].astype(str).apply(lambda x: (x.replace('не исп ', '')))
        df_ch=df_ch.loc[(df_ch['Тип'] == 'Продажа')]
        df_ch['Дата'] = pd.to_datetime(df_ch['Дата/Время чека'], \
                                       format='%d.%m.%Y %H:%M:%S')
        df_ch['id'] = df_ch['Магазин'].astype(int).astype(str)+df_ch['Касса'].astype(int).astype(str)+df_ch['Чек'].astype(int).astype(str)+df_ch['Дата'].astype(str)+df_ch['Смена'].astype(str)
        df_ch['Штрихкод'] = df_ch['Штрихкод'].astype(str)      
        df_ch = df_ch.merge(spr, on=['Штрихкод'], how="left")
        
        combined_ch = pd.concat([combined_ch, df_ch])
        del df_ch
table=pd.DataFrame()
for nsi in spr_list:
    print(nsi)
    combined_for_count_2023 = combined_ch.copy()
    combined_for_count_2023['Дата'] = combined_for_count_2023['Дата'].dt.date
    combined_for_count_2023['Стоимость позиции'] = combined_for_count_2023['Стоимость позиции'].astype(str).apply(
        lambda x: (x.replace(',', '.'))).astype(float)
    combined_for_count_2023['Количество'] = combined_for_count_2023['Количество'].astype(str).apply(
        lambda x: (x.replace(',', '.'))).astype(float)  
    df_cheki_shash_2 = combined_for_count_2023[['id','Номенклатура']]
    df_cheki_shash_2=df_cheki_shash_2.loc[df_cheki_shash_2['Номенклатура']==nsi]
    df_cheki_shash_2=df_cheki_shash_2.drop(columns=['Номенклатура'])
    df_cheki_shash_2.drop_duplicates()
    df_cheki_shash_2['Нужен чек']="Y" 
    combined_for_count_2023 = combined_for_count_2023.merge(df_cheki_shash_2, on=['id'], how="left")
    combined_for_count_2023 = combined_for_count_2023.loc[combined_for_count_2023['Нужен чек'] == 'Y']
    agg_func_count_2023 = {'id': ['count', 'nunique'], 'Количество': ['sum']}
    table_count_2023 = combined_for_count_2023.groupby(['Магазин 1C', 'Дата', 'Номенклатура'], as_index=False).agg(
        agg_func_count_2023)
    table_count_2023.columns = ['_'.join(col).rstrip('_') for col in table_count_2023.columns.values]
    table_count_2023.columns = ['Магазин', 'Дата', 'Номенклатура', 'Позиций', 'Чеков', 'Количество']
    table_count_2023['Шашлык']=nsi
    table_count_2023['Задвоение']=np.where(table_count_2023['Номенклатура']==nsi,'y','n')
    table_count_2023=table_count_2023.loc[table_count_2023['Задвоение']=='n']
    table_count_2023=table_count_2023.drop(columns=['Задвоение'])
    table = pd.concat([table, table_count_2023])
    del combined_for_count_2023
    del table_count_2023
    del df_cheki_shash_2

if  len(spisok_m_number) == 1:

     table.to_csv(r'P:\Фирменная розница\ФРС\Данные из 1 С\Шашлык\2023-Count-TM.txt', sep='\t', index=False,
                            decimal=",")
else:
    table.to_csv(r'P:\Фирменная розница\ФРС\Данные из 1 С\Шашлык\2023-Count.txt', sep='\t', index=False,
                 decimal=",")
