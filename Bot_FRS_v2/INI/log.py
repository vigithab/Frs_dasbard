
from Bot_FRS_v2.INI import ini

PUT = ini.PUT




def log_file(n1, n2, n3,n4, razdel):
    with open(PUT + 'Log\\log_file.txt', 'a') as file:
        if razdel == 1:
            file.write(f'----------------------------------------\n\n')
            n00 = ini.dat_seychas
            n01 = ini.time_seychas
            file.write(f'{n00}  {n01}////---{n1}---{n2}---{n3}---{n4}\n')
            print("запись в лог")

        else:
            n00 = ini.dat_seychas
            n01 = ini.time_seychas
            file.write(f'{n00}  {n01}////---{n1}---{n2}---{n3}---{n4}\n')
            print("запись в лог")

