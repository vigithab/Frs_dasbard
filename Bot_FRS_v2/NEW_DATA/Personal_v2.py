import sys
sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON\venv\Lib\site-packages")
sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON")

import pandas as pd
import time
from Bot_FRS_v2.INI import ini
from Bot_FRS_v2.INI import Float
from Bot_FRS_v2.GooGL_TBL import Google as g
from Bot_FRS_v2.BOT_TELEGRAM import BOT

pd.set_option("expand_frame_repr", False)
pd.set_option('display.max_colwidth', None)
PUT = ini.PUT

class new_data():
    def __init__(self):
        self.week_number,self.start_of_week_str,self.end_of_week_str = ini.weck()
        self.service = g.service
        try:
            self.date_weck = pd.read_excel(
                "https://docs.google.com/spreadsheets/d/13tsxHb82mRcyQiYn78EGh7uV_6sUiq1zcAW3mo2aIFQ/export?exportFormat=xlsx",
                skiprows=1)
            BOT.BOT().bot_mes_html(mes="✅ Персонал - Файл получен...", silka=0)
        except:
            try:
                BOT.BOT().bot_mes_html(mes="📛 Персонал - Ошибка, при скачивании...", silka=0)
                time.sleep(360)
                BOT.BOT().bot_mes_html(mes="🟡 Персонал - Повторное скачивание...", silka=0)
                self.date_weck = pd.read_excel(
                    "https://docs.google.com/spreadsheets/d/13tsxHb82mRcyQiYn78EGh7uV_6sUiq1zcAW3mo2aIFQ/export?exportFormat=xlsx",
                    skiprows=1)
                BOT.BOT().bot_mes_html(mes="🟡 Персонал - Файл получен(2 попытка)...", silka=0)
            except:
                BOT.BOT().bot_mes_html(mes="📛 Персонал - Что то не так, отмена.", silka=0)
                return
    def __googl_sheet(self):
            name = "Укомплектованность ФРС"
            id_tbl = "13tsxHb82mRcyQiYn78EGh7uV_6sUiq1zcAW3mo2aIFQ"
            start = "A1"
            sheet_name = "ПЕРСОНАЛ"
            zagolovok_name = f'Данные будут перезаписаны для недели №{self.week_number+1}, перезапись каждые 2 часа'
            # Записываем дату в ячейку A1
            values = [[str(zagolovok_name)]]
            range_ = f'{sheet_name}!{start}'

            # Запись данных в таблицу
            body = {'values': values}
            result = self.service.spreadsheets().values().update(spreadsheetId=id_tbl, range=range_,
                                                            valueInputOption='RAW',
                                                            body=body).execute()
            # ссылка
            Goole_url = f'https://docs.google.com/spreadsheets/d/{id_tbl}'
            print(f'Ссылка на таблицу укомплектовоность персонала:\n  {Goole_url}')
            return

    def tudey(self):

        self.date_weck["Неделя"] = self.week_number
        self.date_weck = self.date_weck[["Неделя"] + self.date_weck.columns[:-1].tolist()]
        self.date_weck["Первый день недели"] = self.start_of_week_str

        ln = ["Плановая численность",  "Фактическая численность",  "Принято",  "Уволено",  "Кол-во вакансий",  "Медосмотр" , "Стажеровка",  "Студентов работает"]
        Float.FLOAT().float_colms(name_data=self.date_weck,name_col=ln)
        self.date_weck.to_csv(PUT + "Персонал\\data_new\\" +
                         str(self.week_number) + ".csv",
                         encoding="utf-8",
                         sep=';', index=False,
                         decimal=".")
        self.__googl_sheet()
        BOT.BOT().bot_mes_html(mes="✅ Обработан персонал", silka=0)
        return

if __name__ == '__main__':
    new = new_data()
    new.tudey()