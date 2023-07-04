import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import pandas as pd
from Bot_FRS_v2.INI import ini
from Bot_FRS_v2.INI import rename
import numpy as np
import datetime as dt
from datetime import timedelta
import warnings
import gc
import psutil


class avtozakaz_sent():
    def __init__(self):
        self.ya_mail_aps = ini.ya_mail_aps
        self.avtozakaz_mail = ini.avtozakaz_mail
        self.excel_file_path = 'C:\\Users\\Lebedevvv\\Desktop\\FRS\\Автозаказ\\Рассылки по пятницам\\'
        self.format = '.xlsx'
        spqr, sprav_magaz, open_mag = rename.RENAME().magazin_info()
        # Выбор двух столбцов из датафрейма
        open_mag = open_mag[['!МАГАЗИН!', 'Почта магазина']]
        self.dictionary = open_mag.set_index('!МАГАЗИН!')['Почта магазина'].to_dict()



    def sent(self, spisok_email, mes_zagolovok, mes, dataframe):
        for email in spisok_email:
            msg = MIMEMultipart()
            msg['From'] = self.avtozakaz_mail
            msg['To'] = email
            msg['Subject'] = mes_zagolovok

            # Прикрепление текста сообщения
            message = mes
            msg.attach(MIMEText(message))

            # Сохранение датафрейма в файл Excel

            excel_file_path = self.excel_file_path + email + self.format

            dataframe.to_excel(excel_file_path, index=False)

            # Прикрепление файла Excel
            with open(excel_file_path, 'rb') as file:
                attachment = MIMEApplication(file.read(), 'xlsx')
            attachment.add_header('Content-Disposition', 'attachment', filename=email+self.format)
            msg.attach(attachment)

            try:
                mailserver = smtplib.SMTP('smtp.yandex.ru', 587)
                # отладка
                #mailserver.set_debuglevel(True)
                mailserver.ehlo()
                mailserver.starttls()
                mailserver.ehlo()
                mailserver.login(self.avtozakaz_mail, self.ya_mail_aps)
                mailserver.sendmail(self.avtozakaz_mail, email, msg.as_string())
                mailserver.quit()
                print("Письмо успешно отправлено")
            except smtplib.SMTPException:
                print("Ошибка: Невозможно отправить сообщение")
        return
    def data(self):
        #spravochnik_TT=pd.read_excel(r'https://docs.google.com/spreadsheets/d/1qXyD0hr1sOzoMKvMyUBpfTXDwLkh0RwLcNLuiNbWmSM/export?exportFormat=xlsx')
        spqr, sprav_magaz, open_mag = rename.RENAME().magazin_info()
        spravochnik_TT= sprav_magaz[['!МАГАЗИН!','Менеджер','Работают или нет']]
        spravochnik_TT=spravochnik_TT.dropna(subset='Менеджер')
        spravochnik_TT=spravochnik_TT.loc[spravochnik_TT['Работают или нет']=='Действующие']
        spravochnik_TT.columns=['Магазин','Менеджер','Работают или нет']
        spravochnik_TT=spravochnik_TT[['Магазин','Менеджер']]

        replacements=pd.read_excel(r'https://docs.google.com/spreadsheets/d/1SfuC2zKUFt6PQOYhB8EEivRjy4Dz-o4WDL-IR7CT3Eg/export?exportFormat=xlsx')
        rng=len(replacements)
        spr = pd.read_csv(
            r'P:\Фирменная розница\ФРС\Данные из 1 С\Справочные данные\SPQR_NSI.txt',
            sep='\t')
        spr.columns = ['Код товара','Номенклатура','Менеджер Корус','Срок годности','Входит в группу','Ответственный за управление ассортиментом','Упаковка']
        spr=spr.dropna(subset=['Менеджер Корус'])

        spr['Shsh'] = np.where(spr['Номенклатура'].str.contains('Р/К', regex=True), "N",
                               np.where(spr['Входит в группу'].str.contains('200', regex=True),"N" ,
                                        "Y" ))

        spr = spr.dropna(subset='Входит в группу')
        spr = spr[['Код товара','Номенклатура', 'Входит в группу', 'Shsh']]
        spr["Номенклатура"] = spr["Номенклатура"].astype(str).apply(lambda x: (x.replace('Не исп ', '')))
        spr["Номенклатура"] = spr["Номенклатура"].astype(str).apply(lambda x: (x.replace('не исп ', '')))

        def mem_total(x):
            process = psutil.Process()
            memory_info = process.memory_info()
            total_memory_usage = memory_info.rss
            print(x +" - Использование памяти: {:.2f} MB".format(total_memory_usage / 1024 / 1024))
        time_n=dt.datetime.now()
        time_n=time_n.strftime('%H:%M:%S')

        warnings.filterwarnings("ignore")
        pd.set_option("expand_frame_repr", False)
        pd.set_option('display.max_colwidth', None)

        def float_colm(name_data, name_col):
            name_data[name_col] = (name_data[name_col].astype(str).str.replace("\xa0", "").str.replace(",", ".").fillna(0).astype("float").round(2))

        chek_all=pd.DataFrame()
        dvizh_all=pd.DataFrame()
        ost_all=pd.DataFrame()
        ######0.Получаем список дат последних n дней#####################
        spisok_dat=[]
        spisok_dvizh=[]


        path_dvizh=r'P:\Фирменная розница\ФРС\Данные из 1 С\Движение' # Путь до движения
        path_ost=r'P:\Фирменная розница\ФРС\Данные из 1 С\Остаток по дням\2023' # Путь до остатков

        segodnya=dt.date.today()  # Текущая дата
        vchera=segodnya-timedelta(days=1)
        vchera=vchera.strftime("%d.%m.%Y")
        ost_file=path_ost+'\\'+vchera+'.txt'


        combined_cor=pd.DataFrame()
        n = int(71)
        for i in range(1,n):
            day=segodnya-timedelta(days=i)
            day=day.strftime("%d.%m.%Y")
            dvizh=path_dvizh+'\\'+day+'.txt'
            spisok_dvizh.append(dvizh)
        ##############################################0.1 Соединяем остатки
        df_ost=pd.read_csv( ost_file,sep="\t", encoding='utf-8' ,parse_dates=['Дата'],dayfirst=True)
        df_ost=df_ost[['Магазин','Номенклатура','Дата','Начальный остаток','Конечный остаток']]
        rename.RENAME().Rread(name_data=df_ost,name_col="Магазин")
        """for i in range(rng):
            df_ost['Магазин'] = df_ost['Магазин'].str.replace(replacements['НАЙТИ'][i],
                                                         replacements['ЗАМЕНИТЬ'][i],
                                                         regex=False)"""
        df_ost = df_ost.dropna(subset=['Номенклатура'])
        df_ost['Номенклатура'] = df_ost['Номенклатура'].astype(str).apply(lambda x: (x.replace('Не исп ', '')))
        df_ost = pd.merge(df_ost, spr, on=['Номенклатура'], how='left')
        df_ost = df_ost.loc[df_ost['Shsh'] == 'Y']
        df_ost.drop(columns=['Shsh', 'Входит в группу', 'Код товара'], axis=1, inplace=True)
        df_ost=df_ost[['Магазин','Номенклатура','Дата','Конечный остаток']]
        df_ost['Дата']=df_ost['Дата'].astype('datetime64[ns]')
        df_ost['Конечный остаток']=df_ost['Конечный остаток'].astype(str).str.replace("\xa0", "").str.replace(",", ".").fillna(0).astype("float").round(2)
        df_ost['Отрицательное']=np.where(np.greater(0,df_ost['Конечный остаток']),'Y','N')
        df_ost=df_ost.loc[df_ost['Отрицательное']!='N']
        agg_func_ost = {'Номенклатура':['nunique']}
        table_ost = df_ost.groupby(['Магазин'], as_index=False).agg(agg_func_ost )
        table_ost.columns = ['_'.join(col).rstrip('_') for col in table_ost.columns.values]
        table_ost.columns = ['Магазин', 'Количество отрицательных']
        table_ost=table_ost.sort_values([ 'Количество отрицательных'], ascending=[False])
        print(table_ost.head())
        mem_total(x='Остатки  ')
        ################################################0.2 Соединяем движение
        for f_dvizh in spisok_dvizh:
            print(f_dvizh)
            df_dvizh=pd.read_csv( f_dvizh,sep="\t", encoding='utf-8' ,parse_dates=['Дата'],dayfirst=True)
            df_dvizh = pd.merge(df_dvizh, spr, on=['Номенклатура'], how='left')
            df_dvizh = df_dvizh.loc[df_dvizh['Shsh'] == 'Y']
            df_dvizh.drop(columns=['Shsh', 'Входит в группу', 'Код товара'], axis=1, inplace=True)
            df_dvizh = df_dvizh.melt(id_vars=['ТТ', 'Дата', 'Операция', 'Номер операции', 'Номенклатура'], \
                                        value_vars=['Начальный остаток', 'Приход', 'Количество', 'Расход'], \
                                        var_name='Тип операции', value_name='Количество_шт')
            df_dvizh['Дата'] = df_dvizh['Дата'].dt.date
            df_dvizh = df_dvizh.loc[df_dvizh['Операция'] == 'Инвентаризация']
            dvizh_all = pd.concat([dvizh_all,df_dvizh],axis=0)
            del df_dvizh
            gc.collect()
        #2.Получить начальный остаток

        dvizh_melt_inventi = dvizh_all[['ТТ', 'Дата', 'Номер операции']]
        #Получаем список ао кол-ву товаров в инвенте и дате
        agg_func_dvizh = {'Номер операции':['count']}
        table_dvizh = dvizh_melt_inventi.groupby(['ТТ','Дата'], as_index=False).agg(agg_func_dvizh )
        table_dvizh.columns = ['_'.join(col).rstrip('_') for col in table_dvizh.columns.values]
        table_dvizh.columns = ['Магазин','Дата', 'Количество товаров в инвенте']
        table_dvizh=table_dvizh.loc[table_dvizh['Количество товаров в инвенте']>100]
        table_dvizh=table_dvizh.sort_values([ 'Количество товаров в инвенте'], ascending=[False])
        #Получаем список по  максимальному колву кол-ву товаров в инвенте и дате
        agg_func_max = {'Дата':['max']}
        table_max_invent = table_dvizh.groupby(['Магазин'], as_index=False).agg(agg_func_max )
        table_max_invent.columns = ['_'.join(col).rstrip('_') for col in table_max_invent.columns.values]
        table_max_invent.columns = ['Магазин', 'Дата']
        table_max_invent=table_max_invent.sort_values([ 'Дата'], ascending=[True])
        table_max_invent=pd.merge(table_max_invent,table_dvizh,on=['Магазин','Дата'],how='left')
        data=pd.merge(spravochnik_TT,table_max_invent,on=['Магазин'],how='left')
        data=pd.merge(data,table_ost,on=['Магазин'],how='left')
        data['Сегодня']=segodnya
        data['Сегодня']=data['Сегодня'].astype('datetime64[ns]')
        data['Дата']=data['Дата'].astype('datetime64[ns]')
        print(data)

        data['Возраст инвентаризации']=(data['Сегодня']-data['Дата'])/ np.timedelta64 ( 1 , 'D')
        data['Тема']=np.where(np.greater_equal(data['Возраст инвентаризации'],31),'полную инвентаризацию',
                              np.where(np.greater_equal(data['Количество отрицательных'],25),'выборочную инвентаризацию','ХЗ'))
        data=data.loc[data['Тема']!='ХЗ']
        # df_ost фрейм с отрицательными остатками
        print(data)
        print(df_ost)

        spip_mag = data["Магазин"].unique().tolist()
        print(spip_mag)
        for i in spip_mag:
            # письмо
            data = data.loc[data["Магазин"] == i]

            data_invet = data["Дата"].min()

            data_kol_otric = data["Количество отрицательных"].min()
            data_tema = data["Тема"].unique()

            # отправка
            df_ost = df_ost.loc[df_ost["Магазин"] == i]


            mes =\
                f'Добрый день!\n'\
                f'В магазине {i} последняя полная инвентаризация была проведена {data_invet}, количество отрицательных остатков составляет {data_kol_otric} товаров.\n'\
                f'Для корректной работы автозаказа необходимо провести {data_tema}'\
                f'Список товаров с отрицательными остатками находится во вложении'\
                f''\
                f'Данное письмо создано автоматически, отвечать на него не нужно'

            spisok = ["lebedevvv@volcov.ru"]
            mes_zagolovok = f'Инвентаризация {i}'


            emai1 = seldictionary.get(i)

            print(emai1)
            avtozakaz_sent = avtozakaz_sent()
            avtozakaz_sent.sent(spisok_email=spisok, mes_zagolovok=mes_zagolovok, mes=mes, dataframe=df_ost)


