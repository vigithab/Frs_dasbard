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
import shutil
import gc
from Bot_FRS_v2.BOT_TELEGRAM import BOT

class Koreus():
    def __init__(self):
        BOT.BOT().bot_mes_html(mes="Скрипт Корус запущен", silka=0)
        self.driver = webdriver.Chrome()


    def zagruxka(self):
        try:
            self.driver.get('https://ims2.korusconsulting.ru/app/6bcf9b4e1db44acc82d5a1946998609f/orderitems')
            warnings.filterwarnings('ignore')
            time.sleep(5)
            self.id_box = self.driver.find_element(By.ID, 'input-23')
            self.id_box.send_keys('soldatovas@volcov.ru')
            time.sleep(5)
            pass_box = self.driver.find_element(By.XPATH,
                                           '/html/body/div/div/div[1]/div/div/span/form/div/div[1]/span[2]/div/div[2]/div[1]/div/input')
            pass_box.send_keys('volcov22')
            time.sleep(10)
            login_button = self.driver.find_element(By.XPATH, '/html/body/div/div/div[1]/div/div/span/form/div/div[2]/button/span')
            login_button.click()
            time.sleep(7)
            print(1)
            filter_button = self.driver.find_element(By.XPATH, '/html/body/div/div/div[1]/main/div/div/div/div[1]/button[1]')
            filter_button.click()
            print(1)
            time.sleep(7)
            export_button = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[1]/main/div/div/div/div[1]/button[3]')
            export_button.click()
            print(1)
            time.sleep(30)
            # Переделать на ожидание
            button = self.driver.find_element(By.XPATH, '/html/body/div/div[3]/div/div/div[1]/a/span')
            print("ОК")
            time.sleep(10)
            button.click()

            ##button_click('/html/body/div/div[3]/div/div/div[1]/a/span')
            time.sleep(10)
            filter_button_scroll = self.driver.find_element(By.XPATH,
                                                       '/html/body/div/div[1]/div[1]/main/div/div/div/div[2]/div/div[10]/div/div/div')
            time.sleep(10)
            filter_button_scroll.click()
            time.sleep(10)
            cheker_izmen = self.driver.find_element(By.XPATH, '/html/body/div/div[3]/div/div[4]')
            print(1)
            cheker_izmen.click()
            time.sleep(7)
            export_button = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[1]/main/div/div/div/div[1]/button[3]')
            print(1)
            export_button.click()
            # Переделать на ожидание
            time.sleep(30)
            print("ОК 2")
            dowload_button = self.driver.find_element(By.XPATH, '/html/body/div/div[3]/div/div/div[1]/a/span')
            dowload_button.click()
            BOT.BOT().bot_mes_html(mes="Корус скачан", silka=0)


        except Exception as e:
            print(e)
            self.driver.close()
            BOT.BOT().bot_mes_html(mes="Неудача, повтор", silka=0)
            time.sleep(30)
            start = Koreus()
            start.zagruxka()

        finally:
            self.driver.close()
            self.driver.quit()
            time.sleep(30)
        return


start = Koreus()
start.zagruxka()

path_download=r"C:\Users\Lebedevvv\Downloads"
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
pathKuda=("C:\\Users\\Lebedevvv\\Desktop\\FRS\\Автозаказ\\Корректировки2023.xlsx")
combined.to_excel(pathKuda,index=False)
print("BCE")
BOT.BOT().bot_mes_html(mes="Скрипт Корус успешно завершен",silka=0)