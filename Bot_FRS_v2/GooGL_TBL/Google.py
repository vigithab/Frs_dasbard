import sys
import time
sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON\venv\Lib\site-packages")
sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON")
import pandas as pd
import gspread
from gspread_dataframe import get_as_dataframe
import numpy as np
import pandas
from datetime import datetime
import google.auth
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from googleapiclient.discovery import build
from Bot_FRS_v2.INI import ini

PUT = ini.PUT
# авторизациz
creds = service_account.Credentials.from_service_account_file(PUT + 'BOT\\key\\client_secret.json')
service = build('sheets', 'v4', credentials=creds)

class tbl:
    def new_taybl(self, name_tabl, name_list):
        # Создание новой таблицы
        spreadsheet = {
            'properties': {
                'title': name_tabl,  # Название таблицы
                'locale': 'ru_RU'
            },
            'sheets': [
                {
                    'properties': {
                        'title': name_list,  # Название листа
                        'gridProperties': {
                            'rowCount': 300,  # Количество строк в таблице
                            'columnCount': 20  # Количество столбцов в таблице
                        }
                    }
                }
            ]
        }

        spreadsheet = service.spreadsheets().create(body=spreadsheet).execute()
        spreadsheet_id = spreadsheet['spreadsheetId']

        # Установка общего доступа к таблице по ссылке
        file_id = spreadsheet['spreadsheetId']
        permission = {
            'type': 'anyone',
            'role': 'reader',
            'allowFileDiscovery': False
        }
        drive_service = build('drive', 'v3', credentials=creds)
        share_res = drive_service.permissions().create(
            fileId=file_id,
            body=permission,
            fields='id'
        ).execute()

        # Вывод ссылки на таблицу
        Goole_url = f'https://docs.google.com/spreadsheets/d/{file_id}'
        print(f'Ссылка на таблицу - {name_tabl}: {Goole_url}')
        tbl().Info()
        return
    # создание новой таблицы
    def Info(self):
        # Параметры авторизации
        # creds = service_account.Credentials.from_service_account_file('C:\\Users\\lebedevvv\\Desktop\\PYTHON PROJECT\\DASH_FRS\\Progect\\client_secret.json')
        service = build('drive', 'v3', credentials=creds)
        # Выполняем запрос к Google Drive API для получения списка файлов таблиц Google Sheets
        results = service.files().list(q="mimeType='application/vnd.google-apps.spreadsheet' and trashed = false").execute()
        items = results.get('files', [])
        alltbl = []

        if not items:
            print('No files found.')
        else:
            # Для каждого файла в полученных результатах
            for item in items:
                # Добавляем идентификатор файла в список alltbl
                alltbl.append(item['id'])
                # Выводим название файла и его идентификатор (может быть закомментировано)
                # print(u'{0} ({1})'.format(item['name'], item['id']))

        # Создаем список списков с названием таблиц и их идентификатором
        table_info = [[item['name'], item['id']] for item in items]

        # Создаем DataFrame из списка списков table_info с указанием столбцов 'Название' и 'ID'
        df = pd.DataFrame(table_info, columns=['Название', 'ID'])

        # Добавляем столбец со ссылкой на таблицу
        def create_link(table_id):
            return f'https://docs.google.com/spreadsheets/d/{table_id}'

        df['Ссылка'] = df['ID'].apply(create_link)

        # Сохраняем DataFrame df в Excel-файле
        df.to_excel(PUT + 'BOT\\Goole\\Таблицы_Googl.xlsx', index=False)

        # Возвращаем значения alltbl, service и creds
        return alltbl, service, creds
    # инфо по созданым таблицам
    def record(self, name,name_df,sheet_name, zagolovok=None, zagolovok_name=None):
            tbl_id = tbl().tbl_id(name=name)
            start = "A1"
            if zagolovok ==1:
                # Записываем дату в ячейку A1
                values = [[str(zagolovok_name)]]
                range_ = f'{sheet_name}!{start}'

                # Запись данных в таблицу
                body = {'values': values}
                result = service.spreadsheets().values().update(spreadsheetId=tbl_id, range=range_,
                                                                valueInputOption='RAW',
                                                                body=body).execute()
                start = "A2"
            # Имя листа, на который нужно записать данные
            sheet_name = sheet_name
            # Диапазон
            range_ = f'{sheet_name}!{start}'
            del_dat = f'{sheet_name}!{start}:Z'
            # Очистка данных в листе перед записью
            result = service.spreadsheets().values().clear(
                spreadsheetId=tbl_id, range=del_dat).execute()
            # аголовки добавить
            zagolovok = list(name_df.columns.values)
            # Преобразование в массив
            values = [zagolovok] + name_df.values.tolist()
            # Запись данных в таблицу
            body = {'values': values}
            result = service.spreadsheets().values().update(spreadsheetId=tbl_id, range=range_, valueInputOption='RAW', body=body).execute()
            # ссылка
            Goole_url = f'https://docs.google.com/spreadsheets/d/{tbl_id}'
            print(f'Ссылка на таблицу - {name[:-13] + " - "} :  {Goole_url}')

            return Goole_url
    # запись данных в таблицу
    def dele(self):
        alltbl,service,creds= tbl().Info()
        alltbl = ["1EGp5OvPyr5jmWB2sy0ZkUEeW4UWKFQ-dBsdolGg2Mm4"]

        for i in alltbl:
            file_id = i
            response = service.files().delete(fileId=file_id).execute()
            print("удаление " ,i)
    # удаление таблиц
    def tbl_id(self, name):
        tbl().Info()
        # получение ключей
        dat = pd.read_excel(PUT + 'BOT\\Goole\\Таблицы_Googl.xlsx')
        keys_dict = dict(zip(dat.iloc[:, 0], dat.iloc[:, 1]))
        tbl_id = keys_dict.get(name)

        return tbl_id
    # поиск ключей таблиц
    def dostup(self):
        # Путь к файлу с учетными данными
        credentials_file = PUT + 'BOT\\key\\client_secret.json'

        # Идентификатор (ID) существующей таблицы, к которой нужно предоставить доступ
        spreadsheet_id = '1AQRPnFgoA_UJniGKhSe4dd_jZDinUoG7PHN-WwsFNQ8'

        # Создание объекта сервиса для работы с Google Drive API
        credentials = service_account.Credentials.from_service_account_file(credentials_file)
        drive_service = build('drive', 'v3', credentials=credentials)

        # Установка разрешений доступа для редактирования
        drive_service.permissions().create(
            fileId=spreadsheet_id,
            body={
                'type': 'user',
                'role': 'writer',
                'emailAddress': 'erterwertwertwert@gmail.com'
            }
        ).execute()

        # Вывод сообщения об успешном предоставлении доступа
        print('Доступ к таблице предоставлен.')
    # предоставление доступа к таблице
    def new(self):
        Ln_New = ['Турова А.С', 'Баранова Л.В', 'Геровский И.В', 'Изотов В.В', 'Томск', 'Павлова А.А', 'Бедарева Н.Г', 'Сергеев А.С', 'Карпова Е.Э']
        for i in Ln_New:
            # Создание новой таблицы
            spreadsheet = {
                'properties': {
                    'title': i +"_Текущий месяц",
                    'locale': 'ru_RU'
                },
                'sheets': [
                    {
                        'properties': {
                            'title': i +"_Текущий месяц",
                            'gridProperties': {
                                'rowCount': 300,
                                'columnCount': 20
                            }
                        }
                    }
                ]
            }

            spreadsheet = service.spreadsheets().create(body=spreadsheet).execute()
            spreadsheet_id = spreadsheet['spreadsheetId']

            # Заполнение таблицы данными из файла Excel
            df = pd.read_excel("C:\\Users\\lebedevvv\\Desktop\\DASHBRD_SET\\Bot\\temp\\1.xlsx")

            values = df.values.tolist()
            range_ = i +"_Текущий месяц" + '!A1:D' + str(len(values))
            body = {'values': values}

            result = service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id, range=range_, valueInputOption='USER_ENTERED', body=body).execute()

            print(f"{result.get('updatedCells')} ячеек обновлено.")

            # Установка общего доступа к таблице по ссылке
            file_id = spreadsheet['spreadsheetId']
            permission = {
                'type': 'anyone',
                'role': 'reader',
                'allowFileDiscovery': False
            }
            drive_service = build('drive', 'v3', credentials=creds)
            share_res = drive_service.permissions().create(
                fileId=file_id,
                body=permission,
                fields='id'
            ).execute()

            # Вывод ссылки на таблицу
            Goole_url = f'https://docs.google.com/spreadsheets/d/{file_id}'
            print(f'Ссылка на таблицу - {i} :  {Goole_url}')
        return

class tbl_bot():
    # поиск ключей таблиц
    def tbl_id(self, name):
        dat = pd.read_excel(PUT + 'BOT\\Goole\\Таблицы_Googl.xlsx')
        keys_dict = dict(zip(dat.iloc[:, 0], dat.iloc[:, 1]))
        tbl_id = keys_dict.get(name)
        return tbl_id

    def sheet(self,name_tbl, df, sheet_name, one_stroka = None):
        tbl_id = tbl_bot().tbl_id(name=name_tbl)
        zagolovok_name = one_stroka
        # Записываем дату в ячейку A1
        values = [[str(zagolovok_name)]]
        range_ = f'{sheet_name}!B1'
        # Запись данных в таблицу
        body = {'values': values}
        result = service.spreadsheets().values().update(spreadsheetId=tbl_id, range=range_,
                                                        valueInputOption='RAW',
                                                        body=body).execute()

        time.sleep(2)
        zagolovok_name = f'Данные обновлены дата: {ini.dat_seychas} время: {ini.time_seychas}'
        # Записываем дату
        values = [[str(zagolovok_name)]]
        range_ = f'{sheet_name}!B2'
        # Запись данных в таблицу
        body = {'values': values}
        result = service.spreadsheets().values().update(spreadsheetId=tbl_id, range=range_,
                                                        valueInputOption='RAW',
                                                        body=body).execute()

        # Диапазон
        range_ = f'{sheet_name}!A3'
        del_dat = f'{sheet_name}!A3:Z'
        # Очистка данных в листе перед записью
        result = service.spreadsheets().values().clear(
            spreadsheetId=tbl_id, range=del_dat).execute()
        # аголовки добавить
        zagolovok = list(df.columns.values)
        # Преобразование в массив
        values = [zagolovok] + df.values.tolist()
        # Запись данных в таблицу
        body = {'values': values}
        result = service.spreadsheets().values().update(spreadsheetId=tbl_id, range=range_, valueInputOption='RAW',
                                                        body=body).execute()
        # ссылка
        Goole_url = f'https://docs.google.com/spreadsheets/d/{tbl_id}'
        print(f'Ссылка на таблицу - {name_tbl} :  {Goole_url}')

        return Goole_url

    def Last_day (self,name_tbl, df, sheet_name, one_stroka = None):
        tbl_id = tbl_bot().tbl_id(name=name_tbl)
        zagolovok_name = one_stroka
        # Записываем дату
        values = [[str(zagolovok_name)]]
        range_ = f'{sheet_name}!A1'
        # Запись данных в таблицу
        body = {'values': values}
        result = service.spreadsheets().values().update(spreadsheetId=tbl_id, range=range_,
                                                        valueInputOption='RAW',
                                                        body=body).execute()

        time.sleep(2)
        zagolovok_name = f'Данные обновлены дата: {ini.dat_seychas} время: {ini.time_seychas}'
        # Записываем дату
        values = [[str(zagolovok_name)]]
        range_ = f'{sheet_name}!A2'
        # Запись данных в таблицу
        body = {'values': values}
        result = service.spreadsheets().values().update(spreadsheetId=tbl_id, range=range_,
                                                        valueInputOption='RAW',
                                                        body=body).execute()

        # Диапазон
        range_ = f'{sheet_name}!A3'
        del_dat = f'{sheet_name}!A3:Z'
        # Очистка данных в листе перед записью
        result = service.spreadsheets().values().clear(
            spreadsheetId=tbl_id, range=del_dat).execute()
        # аголовки добавить
        zagolovok = list(df.columns.values)
        # Преобразование в массив
        values = [zagolovok] + df.values.tolist()
        # Запись данных в таблицу
        body = {'values': values}
        result = service.spreadsheets().values().update(spreadsheetId=tbl_id, range=range_, valueInputOption='RAW',
                                                        body=body).execute()
        # ссылка
        Goole_url = f'https://docs.google.com/spreadsheets/d/{tbl_id}'
        print(f'Ссылка на таблицу - {name_tbl} :  {Goole_url}')

        return Goole_url

    def svodniy_itog(self,name_tbl, df, sheet_name, one_stroka = None):
        tbl_id = tbl_bot().tbl_id(name=name_tbl)
        time.sleep(2)
        zagolovok_name = f'Данные обновлены дата: {ini.dat_seychas} время: {ini.time_seychas}'
        print(zagolovok_name)
        # Записываем дату
        values = [[str(zagolovok_name)]]
        if name_tbl =="Количество магазинов сети" or "Планы_2023":
            range_ = f'{sheet_name}!A1'
        else :
            range_ = f'{sheet_name}!C1'
        # Запись данных в таблицу
        body = {'values': values}
        result = service.spreadsheets().values().update(spreadsheetId=tbl_id, range=range_,
                                                        valueInputOption='RAW',
                                                        body=body).execute()
        # Диапазон
        range_ = f'{sheet_name}!A2'
        del_dat = f'{sheet_name}!A2:Z'
        # Очистка данных в листе перед записью
        result = service.spreadsheets().values().clear(
            spreadsheetId=tbl_id, range=del_dat).execute()
        # аголовки добавить
        zagolovok = list(df.columns.values)
        # Преобразование в массив
        values = [zagolovok] + df.values.tolist()
        # Запись данных в таблицу
        body = {'values': values}
        result = service.spreadsheets().values().update(spreadsheetId=tbl_id, range=range_, valueInputOption='RAW',
                                                        body=body).execute()
        # ссылка
        Goole_url = f'https://docs.google.com/spreadsheets/d/{tbl_id}'
        print(f'Ссылка на таблицу - {name_tbl} :  {Goole_url}')

        return Goole_url


if __name__ == '__main__':
    #plan = plan()
    #tbl().dele()
    #tbl().new()
    """ln = ['Планы_2023']
    for i in ln:
        tbl().new_taybl(name_tabl= i, name_list="Планы_2023")"""
    #tbl().record(name="Карпова Е.Э_Прошлый день")
    #tbl().dostup()
    #tbl().stil()
    #tbl().Info()
