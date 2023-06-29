import sys
sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON\venv\Lib\site-packages")
sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON")
import os
import selenium
import warnings
import time
import pandas as pd
##import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import shutil
import gc
from Bot_FRS_v2.INI import ini
import  requests
from Bot_FRS_v2.BOT_TELEGRAM import BOT
import tkinter as tk

url = 'https://kalina-malina.ru/'

class KM():
    def __init__(self):

        warnings.filterwarnings('ignore')
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.destroy()
        print("Ширина экрана:", screen_width)
        print("Высота экрана:", screen_height)
        warnings.filterwarnings('ignore')  ##отключаем warnings
        ua = UserAgent()
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")

        # Включение автоматического скачивания файлов без запроса подтверждения
        options.add_experimental_option("prefs", {
            "download.default_directory": ini.PUT_download,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
        options.add_argument("user_agent=" + ua.random)

        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.get(url)
        if screen_width > screen_height:
            print('Горизонтальная')
            self.driver.set_window_size(screen_width,screen_height)
        else:
            print('Вертикальная')
            self.driver.set_window_size(screen_height,screen_width)
    def proverka(self):
        try:
            export_button = self.driver.find_element(By.XPATH,'//*[@id="__layout"]/div/div[3]/footer/div[1]/div/div/div[5]/div/a')
            sel =  export_button.text

            if sel == "8 (800) 700 81 21":
                sel = f"Доступен - {sel} "
            else:
                sel = "Не доступен"

            mes = f"<b>Проверка selenium:</b>\n" \
                  f": -- {sel}\n"

            BOT.BOT().bot_proverka_KM(mes=mes)

        except:
            BOT.BOT().bot_mes_html(mes="Ошибка запроса", silka=0)
        finally:
            self.driver.close()
            self.driver.quit()

r = requests.get(url)
print(r.status_code)
if r.status_code == 200:
    rq = f"Доступен код {r.status_code}"
else:
    rq = f"Не доступен код ошибки {r.status_code}"

mes = f'<b>Проверка сайта kalina-malina.ru</b>\n' \
      f'{ini.dat_seychas} {ini.time_seychas}\n' \
      f'<b>Проверка requests:</b>\n' \
      f": -- {rq}\n"

BOT.BOT().bot_proverka_KM(mes=mes)
kalina_proverka = KM()
kalina_proverka.proverka()