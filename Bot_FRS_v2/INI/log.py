import sys
sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON\venv\Lib\site-packages")
sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON")

from Bot_FRS_v2.INI import ini
PUT = ini.PUT




def log_file(n1, n2, n3,n4, razdel):
    with open(PUT + 'Log\\log_file.txt', 'a') as file:
        if razdel == 1:
            file.write(f'----------------------------------------\n\n')
            n00 = ini.dat_seychas
            n01 = ini.time_seychas
            file.write(f'{n00}  {n01}////---{n1}---{n2}---{n3}---{n4}\n')
        else:
            n00 = ini.dat_seychas
            n01 = ini.time_seychas
            file.write(f'{n00}  {n01}////---{n1}---{n2}---{n3}---{n4}\n')

class LOG:
    def log_data(self):
        with open(PUT + 'Log\\Лог_обработки.txt', 'a') as file:
                file.write(f'----------------------------------------\n')
                n00 = ini.dat_seychas
                n01 = ini.time_seychas
                file.write(f'{n00}  {n01}\n')
    def log_obrabotka(self, mes, priznak,name_file):
        with open(PUT + 'Log\\Лог_обработки.txt', 'a') as file:
                file.write(f'{priznak} || Имя файла: {name_file} ||  {mes}\n')
    def log_new_data(self, e = None, name_txt = None):
        with open(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON\Bot_FRS_v2\LOGI\log_new_data.txt", 'a',encoding="utf-8") as file:
                file.write(f'----------------------------------------\n')
                n00 = ini.dat_seychas
                n01 = ini.time_seychas
                if e == None:
                    e = f"Успешно\n"
                    probel = ""
                else:
                    e = e
                    probel = "\n"
                file.write(f'{n00} : {n01} : {name_txt} :{probel} {e}')











