import zipfile
import pandas as pd
import os
import shutil
import datetime as dt
import warnings
import numpy as np
papki={r'\\rtlfranch3\Данные из 1С\Для Дашборда\Чеки 1 С':r'C:\Users\soldatovas\Desktop\Задача\111.Конец товара\Чеки',\
       r'\\rtlfranch3\Данные из 1С\Для Дашборда\Списания':r'C:\Users\soldatovas\Desktop\Задача\111.Конец товара\Списания',\
       r'\\rtlfranch3\Данные из 1С\Для Дашборда\Движение товаров':r'C:\Users\soldatovas\Desktop\Задача\111.Конец товара\Движение',\
       r'\\rtlfranch3\Данные из 1С\Для Дашборда\Дегустации':r'C:\Users\soldatovas\Desktop\Задача\111.Конец товара\Дегустации',\
       r'\\rtlfranch3\Данные из 1С\Для Дашборда\ЗО ден':r'C:\Users\soldatovas\Desktop\Задача\111.Конец товара\ЗО ден',\
       r'\\rtlfranch3\Данные из 1С\Для Дашборда\Остатки КХВ':r'C:\Users\soldatovas\Desktop\Задача\111.Конец товара\Остаток',\
       r'\\rtlfranch3\Данные из 1С\Для Дашборда\Отчет по продажам':r'C:\Users\soldatovas\Desktop\Задача\111.Конец товара\Продажи',\
       r'\\rtlfranch3\Данные из 1С\Для Дашборда\Себес':r'C:\Users\soldatovas\Desktop\Задача\111.Конец товара\Себес',\
       r'\\rtlfranch3\Данные из 1С\Для Дашборда\ЗО':r'C:\Users\soldatovas\Desktop\Задача\111.Конец товара\ЗО нед',\
       r'\\rtlfranch3\Данные из 1С\Для Дашборда\НСИ магазин':r'C:\Users\soldatovas\Desktop\Задача\111.Конец товара\НСИ магазины',\
       r'\\rtlfranch3\Данные из 1С\Для Дашборда\Движение товаров П7':r'C:\Users\soldatovas\Desktop\Задача\111.Конец товара\Движение нед'}
def copyr(papka,papka_to):
    files=os.listdir(papka)
    for f in files:
        file=papka+'\\'+f
        file_to=papka_to+'\\'+f
        print(file)
        print(file_to)
        shutil.copy2(file,file_to)

########        os.remove(file)


    
def turbo_extracter(path):
    for fail in os.listdir(path):
        file= path+'\\'+fail
        File_zip_path = zipfile.ZipFile(file, 'r')
        File_zip_path.extractall(path)
        File_zip_path.close()
        os.remove(file)  

for item in papki.items():
    copyr(item[0],item[1])
    turbo_extracter(item[1])


warnings.filterwarnings('ignore')  ########отключаем warnings###########

pathCh = r'C:\Users\soldatovas\Desktop\Задача\111.Конец товара\Чеки'
file = r'C:\Users\soldatovas\Desktop\Задача\111.Конец товара\Чеки\Статистика чеков по часам (детально) - идеальный отчёт по чекам СNEw (TXT).txt'
print(file)
print(pathCh)
mesyac = 'Июнь'
god = '2023'

###################################################################################
##############Соединение двух старых в один новый
path_chek_all_1 = r'P:\Фирменная розница\ФРС\Данные из 1 С\Чеки NEW\2023\Май'
path_chek_all_2 = r'P:\Фирменная розница\ФРС\Данные из 1 С\Чеки NEW\2023\Июнь'
chek_all_1 = os.listdir(path_chek_all_1)
chek_all_2 = os.listdir(path_chek_all_2)
combined_chek_all_1 = pd.DataFrame()
combined_chek_all_2 = pd.DataFrame()
combined_chek_all = pd.DataFrame()
for chek_old_1 in chek_all_1:
    file_chek_1 = path_chek_all_1 + '\\' + chek_old_1
    print(file_chek_1)
    df_chek_all_1 = pd.read_csv(file_chek_1, sep='\t', parse_dates=['Дата'], dayfirst=True)
    df_chek_all_1 = df_chek_all_1[['Номенклатура', 'Кол-во']]
    combined_chek_all_1 = pd.concat([combined_chek_all_1, df_chek_all_1], axis=0)
for chek_old_2 in chek_all_2:
    file_chek_2 = path_chek_all_2 + '\\' + chek_old_2
    print(file_chek_2)
    df_chek_all_2 = pd.read_csv(file_chek_2, sep='\t', parse_dates=['Дата'], dayfirst=True)
    df_chek_all_2 = df_chek_all_2[['Номенклатура', 'Кол-во']]
    combined_chek_all_2 = pd.concat([combined_chek_all_2, df_chek_all_2], axis=0)

print('готово')

###################################################################################

##########Чеки
ch_files = os.listdir(pathCh)

for ch in ch_files:
    print('Архив с чеками удален')
########    ##Новое имя файла
    f = open(file, 'r', encoding='utf-8')
    file_name_perer = (f.read(99))
    file_name_perer = file_name_perer[39:49]
    filename = str(file_name_perer) + '.txt'
    f.close()
########    ##Обработка файла чеки
    df = pd.read_csv(file, sep='\t', encoding='utf-8', skiprows=7, skipfooter=1)
    df_1 = pd.read_csv(file, sep='\t', encoding='utf-8', skiprows=7, skipfooter=1)
    df_1.columns = ['Магазин', 'Номер чека', 'Номенклатура', 'Дата чека', 'Номер кассы', 'Выручка', 'Кол-во',
                    'Кол-во вес']
    df_1 = df_1[['Номенклатура', 'Кол-во']]
    combined_chek_all = pd.concat([combined_chek_all_2, df_1, combined_chek_all_1], axis=0)
    combined_chek_all['Кол-во'] = combined_chek_all['Кол-во'].str.replace(r'\xa0', '').str.replace(',', '.')
    combined_chek_all['Кол-во'] = combined_chek_all['Кол-во'].astype(float)
    agg_func_chek_all = {'Кол-во': ['median']}

    table_chek_all = combined_chek_all.groupby(['Номенклатура'], as_index=False).aggregate(agg_func_chek_all)

    table_chek_all.columns = table_chek_all.columns.droplevel(0)
    table_chek_all.columns = ['Номенклатура', 'Кол-во мед.']

    df.columns = ['Магазин', 'Номер чека', 'Номенклатура', 'Дата чека', 'Номер кассы', 'Выручка', 'Кол-во',
                  'Кол-во вес']
    df['Дата'] = df['Дата чека'].str.split(' ').str.get(0)
    df['Время'] = df['Дата чека'].str.split(' ').str.get(1)
    df['Номер чека'] = df['Номер чека'].astype('str')
    df.drop(columns=['Дата чека'], axis=1, inplace=True)
    warnings.filterwarnings('ignore')
    df['id'] = df['Номер кассы'].astype(str) + df['Дата'].astype(str) + df['Магазин'] + df['Номер чека'].astype(str)
    df['Выручка'] = df['Выручка'].astype(str)
    df['Выручка'] = df['Выручка'].apply(lambda x: (x.replace(',', '.').replace(u'\xa0', u'')))
    df['Выручка'] = df['Выручка'].astype(float)
    print('Объединение')
    table_1 = df.merge(table_chek_all[['Номенклатура', 'Кол-во мед.']], on='Номенклатура', how='left')
    table_1['Кол-во мед.'] = table_1['Кол-во мед.'].astype(str)
    table_1['Кол-во мед.'] = table_1['Кол-во мед.'].apply(lambda x: (x.replace(',', '.').replace(u'\xa0', u'')))
    table_1['Кол-во'] = table_1['Кол-во'].astype(str)
    table_1['Кол-во'] = table_1['Кол-во'].apply(lambda x: (x.replace(',', '.').replace(u'\xa0', u'')))
    table_1['Количество строк промежуток'] = table_1['Кол-во'].astype(float) // table_1['Кол-во мед.'].astype(float)
    table_1['Количество строк'] = np.where(table_1['Количество строк промежуток'] < 1, 1,
                                           table_1['Количество строк промежуток'])

    table_1.drop(columns=['Кол-во мед.', 'Количество строк промежуток'], axis=1, inplace=True)
    table_1.to_csv(pathCh +"\\" +filename, encoding='utf-8', sep='\t', index=False, decimal=',')

    print(filename, ' готов')
    ########Копируем чеки на Public
    shutil.copy2(pathCh +"\\"+ filename, 'P:\\Фирменная розница\\ФРС\\Данные из 1 С\\Чеки NEW\\2023\\Июнь\\')
    shutil.copy2(pathCh +"\\"+ filename, 'C:\\Users\\soldatovas\\Desktop\\Задача\\Чеки\\Для переработки\\')
    os.remove(file)
    print(file, ' удален')
##Средний чек
combined = pd.DataFrame()
slash = '\\'
path_cheki_public = 'P:\\Фирменная розница\\ФРС\\Данные из 1 С\\Чеки NEW\\2023\\' + mesyac + '\\'
pathKuda = ('P:\\Фирменная розница\\ФРС\Данные из 1 С\\Данные по чекам\\Месяцы\\')
files = os.listdir(path_cheki_public)

for file in files:
    fil = path_cheki_public + file
    print(file)
    data = pd.read_csv(fil, sep='\t', decimal=',')
    combined = pd.concat([combined, data], axis=0)
combined['Выручка'] = combined['Выручка'].astype(str)
combined['Выручка'] = combined['Выручка'].apply(lambda x: (x.replace(',', '.').replace(u'\xa0', u'')))
combined['Выручка'] = combined['Выручка'].astype(float)
cards = ['Подарочная карта КМ 500р+ конверт', 'Подарочная карта КМ 1000р+ конверт', 'подарочная карта КМ 500 НОВАЯ',
         'подарочная карта КМ 1000 НОВАЯ']
combined['Убрать'] = np.where(combined['Номенклатура'].isin(cards), 'y', 'n')
combined = combined.loc[combined['Убрать']=='n']

########################Группировка для ср.чека
print('Файл собран')
agg_func_count = {'Выручка': ['sum'], 'id': ['count', 'nunique'], 'Количество строк': ['sum']}
table = combined.groupby(['Магазин', 'Дата'], as_index=False).agg(agg_func_count)
table.columns = ['_'.join(col).rstrip('_') for col in table.columns.values]
table.columns = ['Магазин', 'Дата', 'Выручка', 'Позиций', 'Чеков', 'Количество строк']
table['Средний чек'] = table['Выручка'] / table['Чеков']
table['SKU в чеке'] = table['Позиций'] / table['Чеков']
table['Длина'] = table['Количество строк'] / table['Чеков']
table.to_excel(pathKuda + '\\' + god + '-' + mesyac + '.xlsx', index=False)
##    my_report = sv.analyze(table)
##    my_report.show_html()
##Конец чеков



##############Обработка 'движения'#####################################
pathDv = r'C:\Users\soldatovas\Desktop\Задача\111.Конец товара\Движение'
dv_files = os.listdir(pathDv)
print(dv_files)
for dv in dv_files:
    print(dv, ' начат')
    mes = 'Движение ' + str(dv)+'готово'
#########################Конец 'движения'######################################

################################Обработка остатков
path_ostatok = r'C:\Users\soldatovas\Desktop\Задача\111.Конец товара\Остаток'


ostatok_files = os.listdir(path_ostatok)
for ostatok in ostatok_files:
    fileostatok = r'C:\Users\soldatovas\Desktop\Задача\111.Конец товара\Остаток\Остатки на складах КХВ - АЗ (TXT).txt'
    print(ostatok, ' начат')
    print('Архив с остатком')
    stroka = open(fileostatok, 'r', encoding='utf-8')
    new_name = (stroka.read(99))
    new_name = new_name[54:64]
    stroka.close()
    df = pd.read_csv(fileostatok, sep='\t', encoding='utf-8', skiprows=7, skipfooter=1)
    df.columns = ['Магазин', 'Номенклатура', 'Дата', 'Начальный остаток', 'Приход', 'Расход', 'Конечный остаток',
                  'Конечный остаток себестоимость', 'Начальный остаток себестоимость']
    df = df.dropna(subset=['Дата'])
    df = df.reset_index(drop=True)
    df.to_csv(path_ostatok +"\\"+ new_name + '.txt', encoding='utf-8', sep='\t', index=False)
    
    shutil.copy2(path_ostatok +"\\"+ new_name + '.txt',
                 'P:\\Фирменная розница\\ФРС\\Данные из 1 С\\Остаток по дням\\2023\\')
    shutil.copy2(path_ostatok +"\\"+ new_name + '.txt',
                 'C:\\Users\\soldatovas\\Desktop\\Задача\\12.Корректность 1С\\Остаток')
    shutil.copy2(path_ostatok +"\\"+ new_name + '.txt',
                 'C:\\Users\\soldatovas\\Desktop\\Задача\\-----------ALL together---------------\\Остатки')
    os.remove(fileostatok)
    mes = str(ostatok)+ ' удален'
#####################################################Отчет по продажам
path_to = 'P:\\Фирменная розница\\ФРС\\Данные из 1 С\\Отчет по продажам\\По дням\\2023\\'
pathPR = r'C:\Users\soldatovas\Desktop\Задача\111.Конец товара\Продажи'

prodazhi_files = os.listdir(pathPR)

for prodazhi in prodazhi_files:
    print(prodazhi, ' начат ')
    file_prodazhi = pathPR + '\\'+prodazhi
    df = pd.read_csv(file_prodazhi, sep='\t', encoding='utf-8', skiprows=8, skipfooter=1)
    df.columns = ['Номенклатура', 'Группа', 'Магазин', 'Дата', 'Кол-во продаж', 'Вес продаж', 'Себестоимость',
                  'Выручка', 'Прибыль', 'Списания, руб', 'Списания, кг']
    df = df.dropna(subset=['Дата'])
    df = df.reset_index(drop=True)
    spisok_dat_prod=df['Дата'].drop_duplicates().to_list()
    for day in spisok_dat_prod:
        table_prod=df.copy()
        table_prod=table_prod.loc[table_prod['Дата']==day]
        destination_prod=path_to+day+'.txt'
        table_prod.to_csv(destination_prod, encoding='utf-8', sep='\t', index=False)
###########################ЗО############################

                 ##############ЗО неделя###############
warnings.filterwarnings('ignore')
p = r'C:\Users\soldatovas\Desktop\Задача\111.Конец товара\ЗО нед'
p2 = 'P:\\Фирменная розница\\ФРС\\Данные из 1 С\\ЗО\\2023\\'
c = os.listdir(p2)
f = os.listdir(p)
for fs in f:
    file_zo_txt = ('Заявлено_Отгружено - с артикулом поставщика 80_20NEW(Д48) (TXT)' + '.txt')
    fileplace = p +'\\'+ file_zo_txt
    df = pd.read_csv(fileplace, sep='\t', encoding='utf-8', skiprows=6, skipfooter=1)
    df.columns = ['Номенклатура', 'Магазин', 'Дата', 'Заказано', 'Отгружено']
    spisok_dat_zo_nedelya= df['Дата'].drop_duplicates().to_list()
    for day in spisok_dat_zo_nedelya:
        df_copy_zo_ned=df.copy()
        day=str(day)
        distination_zo_ned=p2+day+'.txt'
        df_copy_zo_ned['Дата']=df_copy_zo_ned['Дата'].astype(str)
        df_copy_zo_ned=df_copy_zo_ned.loc[df_copy_zo_ned['Дата']==day]
        df_copy_zo_ned.to_csv (distination_zo_ned, encoding='utf-8', sep='\t', index=False,decimal=',')
                ##############ЗО день###############
file_zo_den_txt = ('Заявлено_Отгружено - с артикулом поставщика 80_20NEW(Д48) (TXT).txt')
path_zo_den = r'C:\Users\soldatovas\Desktop\Задача\111.Конец товара\ЗО ден'
for file_zo_den in os.listdir(path_zo_den):
    fileplace_zo_den = path_zo_den + '\\' + file_zo_den_txt
    df_zo_den = pd.read_csv(fileplace_zo_den, sep='\t', encoding='utf-8', skiprows=7, skipfooter=1)
    df_zo_den.columns = ['Номенклатура', 'Магазин', 'Дата', 'Заказано', 'Отгружено']
    spisok_dat_zo_den= df_zo_den['Дата'].drop_duplicates().to_list()
    for day in spisok_dat_zo_den:
        df_copy_zo_den=df_zo_den.copy()
        day=str(day)
        distination_zo_den=p2+day+'.txt'
        df_copy_zo_den['Дата']=df_copy_zo_den['Дата'].astype(str)
        df_copy_zo_den=df_copy_zo_den.loc[df_copy_zo_den['Дата']==day]
        df_copy_zo_den.to_csv (distination_zo_den, encoding='utf-8', sep='\t', index=False,decimal=',')
###############################Списания################################
path_sp=r'C:\Users\soldatovas\Desktop\Задача\111.Конец товара\Списания'
path_sp_to='C:\\Users\\soldatovas\\Desktop\\Задача\\Списания\\Спис\\2023'
files=os.listdir(path_sp)
print(files)
x = 'Регистратор.Причина списания'
y = 'Причина списания'
for filezip in files:
    extracted_file=path_sp+'\\'+'МОЙ-Ц (TXT).txt'
    g=open(extracted_file,'r',encoding='utf-8')
    file_name_spis=(g.read(99))
    file_name_spis=file_name_spis[52:75]
    filename_spis=str(file_name_spis)+'.txt'
    g.close()
    dist_spis=path_sp_to+'\\'+filename_spis
    dist_spis_public=r'P:\Фирменная розница\ФРС\Данные из 1 С\Списания\2023'
    extracted_file_2=path_sp+'\\'+'МОЙ-Ц (TXT).txt'
    with open(extracted_file, 'r',encoding='utf-8') as file :
          filedata = file.read()
    filedata = filedata.replace(x, y)
    with open(extracted_file_2, 'w',encoding='utf-8') as file:
          file.write(filedata)
    shutil.copy2(extracted_file,dist_spis)
    


    df_spis = pd.read_csv(extracted_file, sep='\t', encoding='utf-8', skiprows=5, skipfooter=1)
    df_spis.columns = ['Магазин', 'Аналитика хозяйственной операции','Причина списания', 'Дата', 'Номенклатура', 'Единица', 'Сумма','Сумма без НДС','Количество','Количество вес']
    df_spis['Дата f'] = df_spis['Дата'].str.split(' ').str.get(0)
    spisok_dat=df_spis['Дата f'].drop_duplicates().to_list()
    for day in spisok_dat :
        ###вычисляем месяц
        day_date=dt.datetime.strptime(day, '%d.%m.%Y')

        df_t=df_spis.copy(deep=True)
        df_t=df_t.loc[df_t['Дата f']==str(day)]
        df_t.drop(columns=['Дата f','Сумма без НДС'],axis=1,inplace=True)
        dist_spis=dist_spis_public+'\\'+day+'.txt'
        df_t.to_csv(dist_spis, encoding='utf-8', sep='\t', index=False, decimal=',')
    os.rename(extracted_file, path_sp +filename_spis)
###############################Себестоимость################################
path_sebes = r'C:\Users\soldatovas\Desktop\Задача\111.Конец товара\Себес'
path_sebes_to = 'C:\\Users\\soldatovas\\Desktop\\Задача\\Отчет по продажам\За месяц\\2023'
files_sebes = os.listdir(path_sebes)
print(files_sebes)
for filezip_sebes in files_sebes:
    extracted_file_sebes = path_sebes + '\\' + 'Себес.- Солдатов А.С. месяц (TXT).txt'
    sebes_file = open(extracted_file_sebes, 'r', encoding='utf-8')
    file_name_sebes = (sebes_file.read(99))
    file_name_sebes = file_name_sebes[52:75]
    filename_sebes = str(file_name_sebes) + '.txt'
    sebes_file.close()
    dist_sebes = path_sebes_to + '\\' + filename_sebes
    shutil.copy2(extracted_file_sebes, dist_sebes)

    os.rename(extracted_file_sebes, path_sebes + '\\' + filename_sebes)

print('good')
###################
path_degus = r'C:\Users\soldatovas\Desktop\Задача\111.Конец товара\Дегустации'
print(path_degus)
path_degus_to = 'P:\\Фирменная розница\\ФРС\\Данные из 1 С\\Дегустации\\'
print(path_degus_to)
files_degus = os.listdir(path_degus)
print(files_degus)
for filezip_degus in files_degus: 
    extracted_file_degus = path_degus + '\\' + 'Отчет по дегустациям - X (TXT).txt'
    degus_file = open(extracted_file_degus, 'r', encoding='utf-8')
    file_name_degus = (degus_file.read(99))
    file_name_degus = file_name_degus[21:44]
    filename_degus = str(file_name_degus) + '.txt'
    degus_file.close()
    dist_degus = path_degus_to + '\\' + filename_degus
    shutil.copy2(extracted_file_degus, dist_degus)
    os.rename(extracted_file_degus, path_degus + '\\' + filename_degus)
print('good')
###############################Движ "Париж"##########################


replacements = pd.read_excel(r'https://docs.google.com/spreadsheets/d/1SfuC2zKUFt6PQOYhB8EEivRjy4Dz-o4WDL-IR7CT3Eg/export?exportFormat=xlsx')
spravochnik_TT=pd.read_excel(r'https://docs.google.com/spreadsheets/d/1qXyD0hr1sOzoMKvMyUBpfTXDwLkh0RwLcNLuiNbWmSM/export?exportFormat=xlsx')
spravochnik_TT=spravochnik_TT[['!МАГАЗИН!','Менеджер']]
spravochnik_TT['Это магазин']='y'
spravochnik_TT['ТТ']=spravochnik_TT['!МАГАЗИН!']
spravochnik_TT.columns=['Магазин','Менеджер','Это магазин','ТТ']
rng = len(replacements)

def dvizh(file):

    df=pd.read_csv(file,skiprows=6, sep="\t")

    df.columns=['Магазин','Номенклатура','Начальный остаток','Приход','Количество','Расход']
    for i in range(rng):
    
        df['Магазин'] = df['Магазин'].replace(replacements['НАЙТИ'][i],
                                                        replacements['ЗАМЕНИТЬ'][i],
                                                        regex=False)
    data=pd.merge(df,
              spravochnik_TT,
              on='Магазин',
              how='left' )

    data["ТТ"] = data["ТТ"].ffill()
    data["Номенклатура"] = data["Номенклатура"].ffill()
    data["Номенклатура"] = data["Номенклатура"].ffill()
    data = data.loc[data['Это магазин']!="y"]
    data.drop(columns=['Это магазин','Менеджер'],axis=1,inplace=True)
    data.columns=['Регистратор','Номенклатура','Начальный остаток','Приход','Количество','Расход','ТТ']
    data=data.loc[data["Регистратор"]!='Итого']
    data['Операция']=data["Регистратор"].str.split(" ").str.get(0)
    data['Номер']=data["Регистратор"].str.split("от").str.get(0).astype(str)
    data['Номер операции']=data["Номер"].str.split(" ").str.get(-2).astype(str)
    data['Дата']=data["Регистратор"].str.split("от").str.get(1)
    data['Дата']=data['Дата'].str.strip(" ")
    data['Дата'] = np.where(data['Дата'].str.count("") == 19, data['Дата'].apply(lambda x: (x.replace(' ', ' 0'))),data['Дата'])
    data.drop(columns=['Номер',"Регистратор"],axis=1,inplace=True)
    data['Операция']=data['Операция'].apply(lambda x:(x.replace('Отчет','Продажа')))
    data=data.loc[(data['ТТ']!='Служебный магазин')|(data['ТТ']!='ФРС')]
    data['Дата для фильтра']=pd.to_datetime(data['Дата'],dayfirst=True)
    data['Дата для фильтра']=data['Дата для фильтра'].dt.strftime('%d.%m.%Y')
    path_to_dvizh=r'P:\Фирменная розница\ФРС\Данные из 1 С\Движение'
    spisok_dat_dvizh=data['Дата для фильтра'].drop_duplicates().to_list()
    print(file)
    
    for day_dvizh in spisok_dat_dvizh:
##        dlina=len(file)
##        konec=int(dlina)-4
##        dlina=int(dlina)-14
##        n=file[dlina:konec]
        data_dvizh=data.copy()
        day_dvizh=str(day_dvizh)
        data_dvizh['Дата для фильтра']=data_dvizh['Дата для фильтра'].astype(str)
        data_dvizh=data_dvizh.loc[data_dvizh['Дата для фильтра']==day_dvizh]
        data_dvizh.drop(columns=['Дата для фильтра'], axis=1, inplace=True)
        distination_dvizh=r'P:\Фирменная розница\ФРС\Данные из 1 С\Движение'+'\\'+day_dvizh+'.txt'
        data_dvizh.to_csv(distination_dvizh, index=False,sep='\t',decimal=',')


path_dvizh=r'C:\Users\soldatovas\Desktop\Задача\111.Конец товара\Движение нед'
for f in os.listdir(path_dvizh):
    fail_dvizhenie=path_dvizh+'\\'+f
    dvizh(fail_dvizhenie)


##############################НСИ магазины##########################
spisok_fr_vnesh=['Бойко Е.С. ИП','Мушинский Д.Е. ИП','Романов Р.Г. ИП','Руди В.А. ИП',\
                 'Савватеева Е.А. ИП','Успех ООО','Фортуна ООО','Шапова А.С. ИП','Шаповал Н.И. ИП',\
                 'Шилько С.Е. ИП','Юркова Е.Н. ИП','Болдырева Т.П. ИП','Данильченко А.Л. ИП','Еникеева И.А. ИП',\
                 'Пестова С.С. ИП','Степенко О.С. ИП','Трифонов Н.С. ИП']
spisok_fr_vnutre=['Вайдурова Н.А. ИП','Глухова А.Ю. ИП','Железовская Ю.В. ИП','Звягина С.Е. ИП',\
                  'Каримова К.П. ИП','Лихова С.В. ИП','Малетина Т.В. ИП','Миронов А.В. ИП','Пиндюрина Г.В. ИП',\
                  'Потанина Ю.А.','Потеряева Л.А. ИП','Приходько Е.В. ИП','Рудакова А.С. ИП','Соколова О.В. ИП',\
                  'Толоконников М.М. ИП','Уфимцева В.С. ИП','Шерина А.Н. ИП',]

spisok_lavok=['Автолавка','Микромаркет','Экопункт']
path_to=r'P:\Фирменная розница\ФРС\Данные из 1 С\НСИ магазинов'

replacements=pd.read_excel(r'https://docs.google.com/spreadsheets/d/1SfuC2zKUFt6PQOYhB8EEivRjy4Dz-o4WDL-IR7CT3Eg/export?exportFormat=xlsx')
rng=len(replacements)
file_nsi=r'C:\Users\soldatovas\Desktop\Задача\111.Конец товара\НСИ магазины\НСИ МАГАЗИН (TXT).txt'
df_nsi=pd.read_csv(file_nsi,sep='\t',skiprows=6)
df_nsi.columns=['Магазин','Юр.Лицо','Формат магазина','Дата','Дата начала авто-формирования документов',\
                'ID магазина','Площадь торгового зала','Правило ценообразования','Узел 1C','Склад поступления','Выручка 1С','Прибыль 1С']
df_nsi['Принадлежность']=np.where(df_nsi['Юр.Лицо'].isin (spisok_fr_vnesh),"ФР внешняя",\
                                  np.where(df_nsi['Юр.Лицо'].isin (spisok_fr_vnutre),"ФР внутренняя",\
                                           np.where(df_nsi['Формат магазина'].isin (spisok_lavok),"Вендинг",\
                                                    "ФРС")))
for i in range(rng):
                df_nsi['ТТ'] = df_nsi['Магазин'].str.replace(replacements['НАЙТИ'][i],\
                                                        replacements['ЗАМЕНИТЬ'][i],\
                                                        regex=False)
df_nsi=df_nsi.dropna(subset='Юр.Лицо')
spisok_dat=df_nsi['Дата'].drop_duplicates().to_list()

for day in spisok_dat :
    
    df=df_nsi.copy(deep=True)
    df=df.loc[df_nsi['Дата']==str(day)]
    nsi_distination=path_to+"\\"+day+".txt"
    df.to_csv(nsi_distination,sep='\t',index=False,encoding='utf-8')


