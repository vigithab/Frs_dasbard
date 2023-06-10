
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


