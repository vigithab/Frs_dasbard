import sys
sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON\venv\Lib\site-packages")
sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON")

##########Отчет формировать по средней цене
import pandas as pd
import warnings
import datetime as dt
import numpy as np
from datetime import timedelta
import locale
from Bot_FRS_v2.INI import ini
from Bot_FRS_v2.INI import log
from Bot_FRS_v2.BOT_TELEGRAM import BOT

pd.set_option("expand_frame_repr", False)
pd.set_option('display.max_colwidth', None)

try:
    warnings.filterwarnings('ignore')
    locale.setlocale(category=locale.LC_ALL,locale="Russian"  )
    nachalo = dt.datetime.now()

    # начало шашлычного сезона
    pervoe_aprelya='2023-04-01'
    pervoe_aprelya=dt.datetime.strptime(pervoe_aprelya, "%Y-%m-%d")
    segodnya=dt.datetime.now()
    n=(segodnya-pervoe_aprelya).days
    n=int(n)

    path_cheks=r'P:\Фирменная розница\ФРС\Данные из 1 С\Чеки Set' # Путь до чеков
    path_prod=r'P:\Фирменная розница\ФРС\Данные из 1 С\Отчет по продажам\По дням\2023'
    path_to=r'P:\Фирменная розница\ФРС\Данные из 1 С\Шашлык'
    path_ost=r'P:\Фирменная розница\ФРС\Данные из 1 С\Остаток по дням\2023' # Путь до остатков
    path_zo=r'P:\Фирменная розница\ФРС\Данные из 1 С\ЗО\2023'
    spisok_ost=[]
    spisok_chekov=[]
    spisok_prod=[]
    spisok_zo=[]
    spisok_dat=[]
    for i in range(1,n):
        day=segodnya-timedelta(days=i)
        day=day.strftime("%d.%m.%Y")
        chek=path_cheks+'\\'+day+'.txt'
        ost = path_ost + '\\' + day + '.txt'
        prod=path_prod+'\\'+day+'.txt'
        zo=path_zo+'\\'+day+'.txt'
        spisok_dat.append(day)
        spisok_chekov.append(chek)
        spisok_ost.append(ost)
        spisok_prod.append(prod)
        spisok_zo.append(zo)
    ##input("Relax maan")
    spisok_shash=['Купаты Барбекю, охл, 0,5 кг','Купаты куриные, охл, 0,5 кг','Колбаски для гриля Улитка, охл, 0,5 кг',\
                  'Колбаски для гриля Ассорти, охл, 0,5 кг','Сердце цыпленка-бройлера (шашлык из сердечек), охл, 0,4 кг',\
                  'Шашлык из индейки в маринаде, охл, 0,35 кг','Колбаски Свиные с вяленными томатами, вар, в/у, охл, 0,3 кг',\
                  'Колбаски Свиные с сыром, вар, в/у, охл, 0,3 кг','Колбаски для гриля (с соусом Терияки), вар, в/у, охл, 0,3 кг',\
                  'Колбаски для гриля (луковые), вар, в/у, охл, 0,3 кг','Колбаски Мексиканские, охл, в/у, 0,4 кг','Колбаски Нежные, охл, в/у, 0,4 кг']

    spr = pd.read_csv(ini.PUT + "Справочники\\номенклатура\\Справочник номеклатуры.txt",
        sep='\t', skiprows=1)

    spr.columns = ['Владелец', 'Входит в группу', 'Срок годности', 'Классификатор для infovizion', 'Штрихкод']
    spr=spr.dropna(subset='Входит в группу')
    spr['Shsh'] = np.where(spr['Владелец'].str.contains('Р/К', regex=True), "N", \
                           np.where(spr['Входит в группу'].str.contains('191.15 Сэндвичи', regex=True), "N", \
                                    np.where(spr['Владелец'].str.contains('Шашл', regex=True), "Y", \
                                             np.where(spr['Входит в группу'].str.contains('100', regex=True), "Y", \
                                                      np.where(spr['Входит в группу'].str.contains('Шашл', regex=True), "Y",
                                                               np.where(spr['Входит в группу'].str.contains(
                                                                   '200.07 Гриль (Шашлык на шпажке)', regex=True), "Y",
                                                                        np.where(spr['Владелец'].isin(spisok_shash), "Y",
                                                                            "N")))))))

    ##input("Relax maan")
    spr['Штрихкод'] = spr['Штрихкод'].astype(str)
    spr = spr.dropna(subset='Входит в группу')
    spr["Владелец"] = spr["Владелец"].astype(str).apply(lambda x: (x.replace('Не исп ', '')))
    spr["Владелец"] = spr["Владелец"].astype(str).apply(lambda x: (x.replace('не исп ', '')))
    spr['Входит в группу'] = spr['Входит в группу'].astype(str).apply(lambda x: (x.replace(' ВЫВЕДЕННЫЕ', '')))
    spr = spr[['Владелец', 'Входит в группу', 'Штрихкод','Shsh']]
    spr.columns = ['Номенклатура', 'Входит в группу', 'Штрихкод','Shsh']
    spr_shash=spr.copy()
    spr_shash = spr_shash.loc[spr_shash['Shsh'] == "Y"]
    spr_shash_nech=spr_shash[['Номенклатура','Shsh']]
    spr_shash['Штрихкод']=spr_shash['Штрихкод'].astype(str)
    spr_shash_nech=spr_shash_nech.drop_duplicates()
    spr = spr[['Номенклатура', 'Входит в группу', 'Штрихкод']]
    spr_list=spr_shash['Номенклатура'].drop_duplicates().to_list()


    time_nachalo=dt.datetime.now()
    warnings.filterwarnings('ignore')

    combined=pd.DataFrame()

    replacements=pd.read_excel(r'https://docs.google.com/spreadsheets/d/1SfuC2zKUFt6PQOYhB8EEivRjy4Dz-o4WDL-IR7CT3Eg/export?exportFormat=xlsx')
    rng=len(replacements)


    def float_colm(name_data, name_col):
        name_data[name_col] = (name_data[name_col].astype(str)\
                                              .str.replace("\xa0", "")\
                                              .str.replace(",", ".")\
                                              .fillna("0")\
                                              .astype("float")\
                                              .round(2))

    mes='Начато продажи '+str(dt.datetime.now().strftime('%H:%M:%S'))
    print(mes)
    ##input("Relax maan")
    ###############################################Продажи##########################################
    for file in spisok_prod :
        df=pd.read_csv(file,sep="\t",encoding='utf-8',decimal=",",dayfirst=True,parse_dates=["Дата"])
        df.columns=['Номенклатура','Группа','Магазин','Дата','Кол-во продаж','Вес продаж','Себестоимость','Выручка','Прибыль','Списания, руб','Списания, кг']
        df=df.dropna(subset=['Дата'])
        df=df.reset_index(drop=True)

        for i in range(rng):
            df['Магазин'] = df['Магазин'].replace(replacements['НАЙТИ'][i],\
                                                            replacements['ЗАМЕНИТЬ'][i],\
                                                            regex=False)
        df["Номенклатура"]=df["Номенклатура"].astype(str).apply(lambda x:(x.replace('Не исп ','')))
        df["Себестоимость"]=df["Себестоимость"].astype(str).apply(lambda x:(x.replace(',','.').replace(u'\xa0', u''))).astype(float)
        df["Кол-во продаж"]=df["Кол-во продаж"].astype(str).apply(lambda x:(x.replace(',','.').replace(u'\xa0', u''))).astype(float)
        df["Вес продаж"]=df["Вес продаж"].astype(str).apply(lambda x:(x.replace(',','.').replace(u'\xa0', u''))).astype(float)
        df= df.merge(spr_shash_nech, on=['Номенклатура'], how="left")
        df=df.loc[df['Shsh'] == "Y"]
        combined=pd.concat([combined,df])
        combined['Дата']=pd.to_datetime(combined['Дата'],dayfirst=True)
        combined["Выручка"]=combined["Выручка"].astype(str).apply(lambda x:(x.replace(',','.').replace(u'\xa0', u''))).astype(float)
    agg_func_count_vesprodazh = {'Вес продаж':['sum']}
    table_vesprodazh =combined.groupby(['Магазин','Дата','Номенклатура',], as_index=False).agg(agg_func_count_vesprodazh)
    table_vesprodazh.columns=['_'.join(col).rstrip('_') for col in table_vesprodazh.columns.values]
    table_vesprodazh.columns=['Магазин','Дата','Номенклатура','Вес продаж']
    agg_func_count = {'Себестоимость':['sum'],'Кол-во продаж':['sum']}
    table =combined.groupby(['Магазин','Дата','Номенклатура',], as_index=False).agg(agg_func_count)
    table.columns=['_'.join(col).rstrip('_') for col in table.columns.values]
    table.columns=['Магазин','Дата','Номенклатура','Себестоимость','Кол-во']
    table['Себестоимость за ед.']=table['Себестоимость']/table['Кол-во']
    table = table.loc[table['Себестоимость за ед.']>0]
    agg_func_count_2 = {'Себестоимость за ед.':['mean']}
    table_2 =table.groupby(['Магазин','Номенклатура','Дата'], as_index=False).agg(agg_func_count_2)
    table_2.columns=['_'.join(col).rstrip('_') for col in table_2.columns.values]
    table_2.columns=['Магазин','Номенклатура','Дата','Себестоимость за единицу товара']
    table_2['Себестоимость за единицу товара']=table_2['Себестоимость за единицу товара'].round(3)
    ###############################################################OSTATKI@@@@@@@
    mes='Начато остатки'+str(dt.datetime.now().strftime('%H:%M:%S'))
    print(mes)
    combined_ost_all=pd.DataFrame()
    combined_ost=pd.DataFrame()

    for f_ost in spisok_ost :
        df_ost=pd.read_csv(f_ost,sep="\t",dayfirst=True,parse_dates=["Дата"])
        df_ost=df_ost[['Магазин','Номенклатура','Дата','Начальный остаток','Конечный остаток']]
        for i in range(rng):
            df_ost['Магазин'] = df_ost['Магазин'].replace(replacements['НАЙТИ'][i],\
                                                        replacements['ЗАМЕНИТЬ'][i],\
                                                        regex=False)
        df_ost["Номенклатура"]=df_ost["Номенклатура"].astype(str).apply(lambda x:(x.replace('Не исп ','')))
        df_ost["Конечный остаток"]=df_ost["Конечный остаток"].astype(str).apply(lambda x:(x.replace(',','.').replace(u'\xa0', u''))).astype(float)
        df_ost["Начальный остаток"]=df_ost["Начальный остаток"].astype(str).apply(lambda x:(x.replace(',','.').replace(u'\xa0', u''))).astype(float)
        df_ost= df_ost.merge(spr_shash_nech, on=['Номенклатура'], how="left")
        df_ost=df_ost.loc[df_ost['Shsh'] == "Y"]
        combined_ost=pd.concat([combined_ost,df_ost])
        df_ost=pd.DataFrame()
    combined_ost_all=pd.concat([combined_ost_all,combined_ost])
    combined_ost=pd.DataFrame()
    agg_func_count_ost = {'Начальный остаток':['sum'],'Конечный остаток':['sum']}
    table_ost =combined_ost_all.groupby(['Магазин','Дата','Номенклатура',], as_index=False).agg(agg_func_count_ost)
    table_ost.columns=['_'.join(col).rstrip('_') for col in table_ost.columns.values]
    table_ost.columns=['Магазин','Дата','Номенклатура','Начальный остаток','Конечный остаток']
    combined_ost_all=pd.DataFrame()
    ###########ЗО###########
    ##input("Relax maan")


    # заявлено отгружено
    combined_zo=pd.DataFrame()
    for f_zo in spisok_zo :
        df_zo=pd.read_csv(f_zo,sep="\t",dayfirst=True,parse_dates=["Дата"])
        for i in range(rng):
                df_zo['Магазин'] = df_zo['Магазин'].replace(replacements['НАЙТИ'][i],\
                                                            replacements['ЗАМЕНИТЬ'][i],\
                                                            regex=False)
        df_zo["Номенклатура"]=df_zo["Номенклатура"].astype(str).apply(lambda x:(x.replace('Не исп ','')))
        df_zo["Отгружено"]=df_zo["Отгружено"].astype(str).apply(lambda x:(x.replace(',','.').replace(u'\xa0', u''))).astype(float)
        df_zo["Заказано"]=df_zo["Заказано"].astype(str).apply(lambda x:(x.replace(',','.').replace(u'\xa0', u''))).astype(float)
        df_zo['Месяц']= pd.to_datetime(df_zo["Дата"]).dt.month
        df_zo= df_zo.merge(spr_shash_nech, on=['Номенклатура'], how="left")
        df_zo=df_zo.loc[df_zo['Shsh'] == "Y"]
        combined_zo=pd.concat([combined_zo,df_zo])
    agg_func_count_zo = {'Заказано':['sum'],'Отгружено':['sum']}
    table_ch_zo =combined_zo.groupby(['Магазин','Дата','Номенклатура',], as_index=False).agg(agg_func_count_zo)
    table_ch_zo.columns=['_'.join(col).rstrip('_') for col in table_ch_zo.columns.values]
    table_ch_zo.columns=['Магазин','Дата','Номенклатура','Заказано','Отгружено']
    #########################Чеки###########
    ##input("Relax maan")
    print('Начато чеки ',dt.datetime.now().strftime('%H:%M:%S'))
    combined_ch=pd.DataFrame()


    for f_ch in spisok_chekov:
        df_ch=pd.read_csv(f_ch,sep='\t')
        df_ch=df_ch[['Тип','Дата/Время чека','Магазин','Касса','Смена','Чек','Сумма чека','Сумма скидки чека','Штрихкод',\
                     'Наименование товара','Количество','Цена','Процент скидки','Сумма скидки','Стоимость позиции','Магазин 1C']]
        for i in range(rng):
            df_ch['Магазин 1C'] = df_ch['Магазин 1C'].replace(replacements['НАЙТИ'][i],\
                                                        replacements['ЗАМЕНИТЬ'][i],\
                                                        regex=False)
        df_ch["Наименование товара"]=df_ch["Наименование товара"].astype(str).apply(lambda x:(x.replace('Не исп ','')))
        df_ch.loc[(df_ch['Тип']=='Продажа')]
        df_ch['Дата']=pd.to_datetime(df_ch['Дата/Время чека'],\
               format='%d.%m.%Y %H:%M:%S')
        df_ch['Дата']=df_ch['Дата'].dt.date.astype('datetime64[ns]')
        df_ch['ID']=df_ch['Магазин'].astype(int).astype(str)+\
                     df_ch['Касса'].astype(str).apply(lambda x:(x.replace(',','.').replace(u'\xa0', u''))).astype(int).astype(str)+\
                     df_ch['Чек'].astype(str).apply(lambda x:(x.replace(',','.').replace(u'\xa0', u''))).astype(int).astype(str)+\
                     df_ch['Дата'].astype(str)+\
                     df_ch['Смена'].astype(str).apply(lambda x:(x.replace(',','.').replace(u'\xa0', u''))).astype(int).astype(str)
        df_ch["Стоимость позиции"]=df_ch["Стоимость позиции"].astype(str).apply(lambda x:(x.replace(',','.').replace(u'\xa0', u''))).astype(float)
        df_ch["Количество"]=df_ch["Количество"].astype(str).apply(lambda x:(x.replace(',','.').replace(u'\xa0', u''))).astype(float)
        df_ch["Сумма скидки"]=df_ch["Сумма скидки"].astype(str).apply(lambda x:(x.replace(',','.').replace(u'\xa0', u''))).astype(float)
        df_ch['Штрихкод']=df_ch['Штрихкод'].astype(str)
        df_ch= df_ch.merge(spr_shash, on=['Штрихкод'], how="left")
        df_ch=df_ch.loc[df_ch['Shsh'] == "Y"]
        combined_ch=pd.concat([combined_ch,df_ch])
    agg_func_count_ch = {'ID':['nunique']}
    table_ch_1 =combined_ch.groupby(['Магазин 1C','Дата','Наименование товара',], as_index=False).agg(agg_func_count_ch)
    table_ch_1.columns=['_'.join(col).rstrip('_') for col in table_ch_1.columns.values]
    table_ch_1.columns=['Магазин','Дата','Номенклатура','Чеков']
    ##############Начало сращивания определяем все позиции конкат по магазину номенклатуле началу месяца
    table_ch_base=table_ch_1[['Магазин','Дата','Номенклатура']]
    table_zo_base=table_ch_zo[['Магазин','Дата','Номенклатура']]
    table_ost_base=table_ost[['Магазин','Дата','Номенклатура']]
    table_base=pd.concat([table_ch_base,table_zo_base,table_ost_base])
    table_base.drop_duplicates()
    table_base= table_base.merge(table_ch_1, on=['Магазин','Дата','Номенклатура'], how="left")
    table_base= table_base.merge(table_2, on=['Магазин','Дата','Номенклатура'], how="left")
    table_base= table_base.merge(table_ch_zo, on=['Магазин','Дата','Номенклатура'], how="left")
    table_base= table_base.merge(table_ost, on=['Магазин','Дата','Номенклатура'], how="left")
    table_base= table_base.merge(table_vesprodazh, on=['Магазин','Дата','Номенклатура'], how="left")
    table_base['Себестоимоcть остатка']=table_base['Конечный остаток'].astype(float)*table_base['Себестоимость за единицу товара']
    table_base.columnns=['ТТ','Дата	','Номенклатура	','Чеков','Себестоимость за единицу товара','Заказано',\
                         'Отгружено','Количество отгрузок','Начальный остаток','Конечный остаток']
    table_base.drop_duplicates(inplace=True)
    spisok_col=[]
    spisok_col=['Чеков','Заказано','Отгружено','Начальный остаток' ,'Конечный остаток', 'Себестоимость за единицу товара','Себестоимоcть остатка']
    for col in spisok_col:
        float_colm(table_base, col)
    print('Начато сохранение ',dt.datetime.now().strftime('%H:%M:%S'))
    table_base.to_csv(path_to+"\\"+"data.txt",encoding='utf-8',index=False,sep="\t",decimal=",")
    log.LOG().log_new_data(name_txt="Шашлычный data")
except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    mes = f"Ошибка при скачивании : {exc_type.__name__} на строке {exc_tb.tb_lineno}: {e}\n"
    log.LOG().log_new_data(name_txt="Шашлычный data", e=mes)
    BOT.BOT().bot_mes_html(mes="Ошибка при шашлычного data", silka=0)
