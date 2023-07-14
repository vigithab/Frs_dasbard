import re
import sys
sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON\venv\Lib\site-packages")
sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON")
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import selenium
import warnings
import time
import pandas as pd
##import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.by import By
import shutil
import gc
from Bot_FRS_v2.BOT_TELEGRAM import BOT
from Bot_FRS_v2.INI import ini
import tkinter as tk
from fake_useragent import UserAgent


class Koreus():
    def __init__(self):
        self.path_download = r"C:\Users\Lebedevvv\Downloads"
        def del_shlak():
            # Получение списка файлов в папке
            files = os.listdir(self.path_download)
            for file in files:
                if file.endswith(".csv") and re.search('orders', file):
                    file_path = os.path.join(self.path_download, file)
                    os.remove(file_path)
            else:
                print("нет файлов для удаления")
            return
        del_shlak()
        BOT.BOT().bot_mes_html(mes="Скрипт Корус запущен", silka=0)
        url = "https://ims2.korusconsulting.ru/app/6bcf9b4e1db44acc82d5a1946998609f/orderitems"
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
        #options.add_argument("--headless")
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
        print("")
        self.driver.get(url)
        print("ход на сайт Корус")
        time.sleep(5)
        if screen_width > screen_height:
            self.driver.set_window_size(screen_width, screen_height)
            print('Горизонтальная')
        else:
            print('Вертикальная')
            self.driver.set_window_size(screen_height, screen_width)


    def del_kusok(self):
        # Получение списка файлов в папке
        files = os.listdir(self.path_download)

        # Проверка каждого файла и удаление файлов с расширением ".crdownload" и содержащих "orders" в названии
        for file in files:
            if file.endswith(".crdownload") and re.search('orders', file):
                file_path = os.path.join(self.path_download, file)
                os.remove(file_path)
        return

    def zagruxka(self):
        try:

            time.sleep(5)
            print("1")
            self.id_box = self.driver.find_element(By.ID, 'input-23')
            print("2")
            self.id_box.send_keys('soldatovas@volcov.ru')
            time.sleep(5)
            pass_box = self.driver.find_element(By.XPATH,
                                           '/html/body/div/div/div[1]/div/div/span/form/div/div[1]/span[2]/div/div[2]/div[1]/div/input')
            pass_box.send_keys('volcov22')
            time.sleep(10)
            login_button = self.driver.find_element(By.XPATH, '/html/body/div/div/div[1]/div/div/span/form/div/div[2]/button/span')
            login_button.click()
            time.sleep(2)



            print(1)
            filter_button = self.driver.find_element(By.XPATH, '/html/body/div/div/div[1]/main/div/div/div/div[1]/button[1]')
            filter_button.click()
            print(1)
            time.sleep(7)
            export_button = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[1]/main/div/div/div/div[1]/button[3]')
            export_button.click()
            print(1)

            wait = WebDriverWait(self.driver,timeout=90, poll_frequency=2)
            download_button = wait.until(EC.presence_of_element_located(
                (By.XPATH, '//a[contains(@class, "v-btn--is-elevated") and contains(., "Скачать")]')))
            download_button.click()
            print("1 кнопка нажата")
            while sum("orders" in file.lower() and file.endswith(".csv") for file in os.listdir(self.path_download)) != 1:
                print("Ждем")
                time.sleep(0.5)
            time.sleep(60)
            filter_button_scroll = self.driver.find_element(By.XPATH,
                                                       '/html/body/div/div[1]/div[1]/main/div/div/div/div[2]/div/div[10]/div/div/div')
            time.sleep(5)
            filter_button_scroll.click()
            time.sleep(5)
            cheker_izmen = self.driver.find_element(By.XPATH, '/html/body/div/div[3]/div/div[4]')
            print(1)
            cheker_izmen.click()
            time.sleep(7)
            export_button = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[1]/main/div/div/div/div[1]/button[3]')
            print(1)
            export_button.click()
            # Переделать на ожидание
            wait = WebDriverWait(self.driver, timeout=90, poll_frequency=2)
            download_button = wait.until(EC.presence_of_element_located(
                (By.XPATH, '//a[contains(@class, "v-btn--is-elevated") and contains(., "Скачать")]')))
            # time.sleep(30)
            # Переделать на ожидание
            # button = self.driver.find_element(By.XPATH, '/html/body/div/div[3]/div/div/div[1]/a/span')
            download_button.click()
            print("2 кнопка нажата")
            while sum("orders" in file.lower() and file.endswith(".csv") for file in os.listdir(self.path_download)) != 2:
                print("Ждем")
                time.sleep(0.5)

            print("ОК2")
            BOT.BOT().bot_mes_html(mes="Корус скачан", silka=0)


        except Exception as e:
            BOT.BOT().bot_mes_html(mes="Неудача, повтор", silka=0)
            Koreus().del_kusok()
            time.sleep(30)
            print(e)
            self.driver.close()
            time.sleep(30)
            start = Koreus()
            start.zagruxka()

        finally:
            self.driver.close()
            self.driver.quit()
        return


start = Koreus()
start.zagruxka()
path_download = start.path_download
#path_download =r"C:\Users\Lebedevvv\Downloads"

files=os.listdir(path_download)
print(files,  " и ", path_download)
for f in files :
    nachalo=f[:6]
    file=path_download+"\\"+f
    if str(nachalo)=="orders" :
        razmer=os.path.getsize(file)
        print(razmer)
        df=pd.read_csv(file,sep=";")
        dataZ=df["Дата заказа"][0]
        new_filename=dataZ+".csv"
        if int(razmer)>=int(10000000):
            path_to="P:\\Фирменная розница\\ФРС\\Данные из 1 С\\Корректировки\\Все товары\\2023\\"
        else :
            path_to="P:\\Фирменная розница\\ФРС\\Данные из 1 С\\Корректировки\\Только корректировки\\"
        shutil.copy2(file,path_to+new_filename)
        print(f, "переименован в ", new_filename, "и перенесен."," в ", path_to)
        os.remove(file)
        print(file, " удален")
    else :
        next
        gc.collect()

time.sleep(60)
combined=pd.DataFrame()
slash="\\"
path=("P:\\Фирменная розница\\ФРС\\Данные из 1 С\\Корректировки\\Все товары\\2023\\")
files=(os.listdir(path))
allfiles=len(files)
#counter=0
for file in files :
    fil=path+file
    print(file)
    data=pd.read_csv(fil,sep=";",decimal=',')
    agg_func_count = {'Наименование товара': ['count']}
    table = data.groupby(['Магазин/Склад получатель', 'Дата заказа'], as_index=False).agg(agg_func_count)
    del data
    table.columns = ['_'.join(col).rstrip('_') for col in table.columns.values]
    table.columns = ['Магазин', 'Дата', 'Количество']
    combined=pd.concat([combined,table])
    del table
    gc.collect()
gc.collect()
pathKuda=("C:\\Users\\lebedevvv\\Desktop\\FRS\\Автозаказ\\Списания ежедневные\\Коректировки\\Корректировки2023.xlsx")
combined.to_excel(pathKuda,index=False)
print("BCE")
BOT.BOT().bot_mes_html(mes="Скрипт Корус успешно завершен",silka=0)