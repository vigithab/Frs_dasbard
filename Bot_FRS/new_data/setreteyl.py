import selenium
import warnings
import time as t
##import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta, time, date
import datetime
import os
import pandas as pd
import gc
from Bot_FRS.inf import memory as memory
from Bot_FRS.bot_telegram import Bot as bot
from Bot_FRS.inf import NASTROYKA as setting


PUT = setting.PUT

class SET:
    def Set_obrabotka(self):
        bot.BOT().bot_mes_html(mes="Получение данных сетретеил....", silka=0)
        def spisok_dat():
            # region СПИСОК ДАТ
            today = datetime.datetime.now()
            tame_Filter = today.strftime("%H:%M:%S")

            spisok_d = [datetime.datetime.now().strftime('%d.%m.%Y')]
            # сохранение файла с датой обновления
            with open(PUT + 'NEW\\дата обновления.txt', 'w') as f:
                f.write(str(today))
            if tame_Filter < setting.time_bot_vrem:
                day_1 = today - timedelta(days=1)
                date_vchera = day_1.strftime('%d.%m.%Y')
                # day_2 = today - timedelta(days=2)
                # date_poz_vchera = day_2.strftime('%d.%m.%Y')
                spisok_d.append(date_vchera)
                # spisok_d.append(date_poz_vchera)

            """start_date = date(2023, 1, 1)  # начальная дата
            end_date = date(2023, 5, 12)  # конечная дата
            delta = timedelta(days=1)  # шаг даты

            dates_list = []
            while start_date < end_date:
                # # преобразование даты в строку в формате 'день.месяц.год' и добавление её в список
                dates_list.append(start_date.strftime('%d.%m.%Y'))
                start_date += delta
                spisok_d = dates_list"""

            #spisok_d = ['06.06.2023']
            print(spisok_d)
            return spisok_d
        # region СКАЧИВАНИЕ С САЙТА
        warnings.filterwarnings('ignore')  ##отключаем warnings
        ua = UserAgent()
        options = webdriver.ChromeOptions()
        options.add_argument("user_agent=" + ua.random)
        driver = webdriver.Chrome(chrome_options=options)
        url = 'http://10.32.2.51:8443/operday/checks'
        driver.get(url)
        t.sleep(3)
        driver.set_window_size(1024, 600)
        driver.maximize_window()
        t.sleep(1)
        id_box = driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/form/div/div[1]/div/input')
        t.sleep(0.5)
        id_box.send_keys('lebedevvv')
        t.sleep(1)
        pass_box = driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/form/div/div[2]/div/input')
        t.sleep(0.5)
        pass_box.send_keys('hCPxMeOdp')
        t.sleep(1)
        print("Вход на сайт...")
        login_button = driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/form/div/button/span[1]')
        t.sleep(0.5)
        login_button.click()
        t.sleep(2)
        def back(pole):
            print("Ввод новойдаты")
            i = 0
            while i < 12:
                pole.send_keys(Keys.BACKSPACE)
                i += 1
        try:
            t.sleep(0.5)
            menu = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, 'appBarLeftButton')))
        except:
            t.sleep(0.5)
            print(menu.text)
        finally:
            t.sleep(0.5)
            menu.click()
        try:
            t.sleep(0.5)
            menu_op_day_cheks = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[3]/div[2]/div[2]/div[2]/div/div/div/div[1]/div[1]/span')))
        except:
            t.sleep(0.5)
            d = "no"
        finally:
            t.sleep(1)
            if d == "no":
                try:
                    menu_op_day = WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div[1]/div/div[2]/div[2]/div[1]/span')))
                finally:
                    t.sleep(2)
                    menu_op_day.click()
                    print("click operday")
                try:
                    menu_op_day_cheks = WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div[1]/div[1]')))
                finally:
                    t.sleep(2)
                    menu_op_day_cheks.click()
                    print("m")
            else:
                t.sleep(1)
                menu_op_day_cheks.click()
        print("Отправлен на скачивание.....")

        spisok_d = spisok_dat()
        for day in spisok_d:
            bot.BOT().bot_mes_html(mes="Скачивание файла :" + str(day), silka=0)
            new_day_1 = day + " 00:00"
            t.sleep(0.5)
            new_day_2 = day + " 23:59"
            try:
                t.sleep(1)
                menu_data_n = WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/div/div[1]/div[2]/div[2]/div[1]/div/div/div[1]/div/div/div/input')))
            finally:
                back(menu_data_n)
                t.sleep(1)
                print("вводим данные")
                menu_data_n.send_keys(new_day_1)
            t.sleep(2)
            try:
                t.sleep(0.5)
                menu_data_k = WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/div/div[1]/div[2]/div[2]/div[1]/div/div/div[2]/div/div/div/input')))
            finally:
                t.sleep(0.5)
                menu_data_k.clear()
                t.sleep(0.5)
                back(menu_data_k)
                t.sleep(1)
                print("вводим данные")
                menu_data_k.send_keys(new_day_2)
            t.sleep(2)
            # endregion
            try:
                t.sleep(1)
                menu_primenit = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div[2]/div/div/div/div[1]/div[2]/div[3]/button[2]/span[1]')))
            finally:
                t.sleep(1)
                menu_primenit.click()
            t.sleep(1)
            down = ""
            try:
                t.sleep(1)
                dowload = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '/html/body/div/div/div/div[2]/div/div/div/div[1]/div[2]/div[3]/div[1]/div/div/button/span[1]')))
            except:
                down = "no"
            finally:
                if down == "no":
                    print("нет кнопки")
                else:
                    t.sleep(0.5)
                    dowload.click()

                try:
                    dowload_all = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[3]/ul/li[2]')))
                finally:
                    t.sleep(0.5)
                    dowload_all.click()
                    t.sleep(2)
                    x = ""
                try:
                    t.sleep(1)
                    dowload_yes = WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[3]/div/div[3]/button[2]/span[1]')))
                except:
                    x = "no"
                finally:
                    if x == "no":
                        print("но")
                    else:
                        t.sleep(1)
                        dowload_yes.click()
                        t.sleep(0.5)


            folder_path = setting.PUT_download  # путь до папки, которую необходимо мониторить
            partial_name = "PurchasePositions"  # подстрока, которую необходимо найти
            found_file = False
            bot.BOT().bot_mes_html(mes=str(day)+ " - Ожидание файла.... ", silka=0)
            while not found_file:
                for filename in os.listdir(folder_path):
                    if partial_name in filename and filename.endswith(".xlsx"):
                        # найден файл, удовлетворяющий условиям
                        print(f"Найден файл: {filename}")
                        found_file = True

                        t.sleep(0.7)
                        path_download = setting.PUT_download

                        files = os.listdir(path_download) # путь до папки, которую необходимо мониторить
                        #print(files, " и ", path_download)
                        for f in files:
                            #d = len(f)
                            file_name = f[0:17]
                            file = path_download + "\\" + f
                            if str(file_name) == "PurchasePositions":
                                try:
                                    df = pd.read_excel(file, skiprows=1)
                                    memory.MEMORY().mem_total(x="Фаил загружен: " + os.path.basename(file))

                                    d = df['Дата/Время чека'][1]
                                    new_filename = d[0:10] + ".xlsx"

                                    df.to_excel(PUT + "Selenium\\Оригинальные файлы\\" + new_filename, index=False)
                                    del df
                                    gc.collect()
                                    os.remove(file)

                                except Exception as e:
                                    with open(PUT + "NEW\\error_log.txt", "a") as f:
                                        f.write(f"Ошибка при открытии файла {str(day)}: {str(e)}\n")
                                    t.sleep(60)
                                    os.remove(file)
                                    SET().Set_obrabotka()
                                    bot.BOT().bot_mes_html(mes=str(day) + "Ошибка при скачивании возврат", silka=0)
                                    #continue  # продолжить выполнение цикла

                # Проверьте, был ли найден файл. Если нет, подождите несколько секунд и повторите попытку
                if not found_file:
                    print(f"Файл {partial_name} не найден. Ожидание...")
                    t.sleep(2)  # задержка в 1 секунд перед следующей попыткой поиска файла


        driver.close()
        driver.quit()
        #SET().History()
        return
    # Загрузка с сайта сетретейл
#SET().Set_obrabotka()