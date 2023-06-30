
from datetime import datetime, timedelta, time, date
import os
import pandas as pd
import gc
import datetime
import time
from Bot_FRS_v2.INI import memory
from Bot_FRS_v2.INI import ini
from Bot_FRS_v2.NEW_DATA.SET_SD import run_NEW_DATA_sd
from Bot_FRS_v2.NEW_DATA import SORT_FILE
from Bot_FRS_v2.BOT_TELEGRAM import BOT
from Bot_FRS_v2.NEW_DATA import SETRETEYL as set
from Bot_FRS_v2.INI import rename
from Bot_FRS_v2.INI import Float
from Bot_FRS_v2.NEW_DATA import GRUP_FILE
from Bot_FRS_v2.INI import log
from Bot_FRS_v2.RASSILKA import Voropaev
from Bot_FRS_v2.NEW_DATA import Personal_v2


class finrez_obrabotka():
    def __init__(self):
        pd.set_option("expand_frame_repr", False)
        pd.set_option('display.max_colwidth', None)

        self.PUT = ini.PUT

    def a(self):
        for files in os.listdir(self.PUT + "Финрез\\Исходник\\"):
            FINREZ = pd.read_excel(self.PUT + "Финрез\\Исходник\\" + files, sheet_name="Динамика ТТ исходник")
            print( FINREZ)

            FINREZ = FINREZ.loc[FINREZ['дата'] >= "2022-01-01"]

            FINREZ = rename.RENAME().Rread(name_data=FINREZ, name_col="магазин")
            print(FINREZ)



finrez_obrabotka = finrez_obrabotka()
finrez_obrabotka.a()