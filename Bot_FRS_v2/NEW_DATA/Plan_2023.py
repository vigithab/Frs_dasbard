import pandas as pd
from Bot_FRS_v2.INI import rename
from Bot_FRS_v2.INI import Float
from Bot_FRS_v2.INI import ini
from datetime import datetime, timedelta



# Получение текущей даты
current_date = datetime.now().date()
# Создание списка дат на год
dates = []
for month in range(1, 13):
    date = current_date.replace(month=month, day=1)
    dates.append(date.strftime('%d.%m.%Y'))

# Вывод списка дат
print(dates)
# Создание словаря с числами на основе списка дат
slov_sales = {}
number = 59
for date in dates:
    slov_sales[date] = number
    number += 1
slov_sales['магазин'] = 5
slov_sales['Проверка'] = 777
slov_sales = {value: key for key, value in slov_sales.items()}

# Создание словаря с числами на основе списка дат
slov_check = {}
number = 98
for date in dates:
    slov_check[date] = number
    number += 1
slov_check['магазин'] = 5
slov_check['Проверка'] = 777
slov_check = {value: key for key, value in slov_check.items()}

# Создание словаря с числами на основе списка дат
slov_aver = {}
number = 137
for date in dates:
    slov_aver[date] = number
    number += 1
slov_aver['магазин'] = 5
slov_aver['Проверка'] = 777
slov_aver = {value: key for key, value in slov_aver.items()}



# Переименование столбцов на основе словаря
plan = pd.read_excel(ini.PUT + "♀Планы\\Исходник\\2023.xlsx", skiprows=4, nrows=136)


rename.RENAME().Rread(name_col="Магазин изм.",name_data=plan,name="dd")

# Пронумеровать столбцы
plan.columns = range(1, len(plan.columns) + 1)
plan[777] = plan[5]
plan= plan.loc[plan[5].notnull()]
# Продажи
plan_sales = plan[[5,777, 59,60,61,62,63,64,65,66,67,69,69,70]]
plan_sales= plan_sales.rename(columns=slov_sales)
plan_sales["Показатель"] = "Выручка"
plan_sales = plan_sales.melt(
                id_vars=["магазин", "Проверка","Показатель"],
                var_name="дата",
                value_name="ПЛАН").reset_index(drop=True)

# Чеки
plan_check = plan[[5,777,98,99,100,101,102,103,104,105,106,107,108,109]]
plan_check= plan_check.rename(columns=slov_check)
plan_check["Показатель"] = "Кол чеков"
plan_check =plan_check.melt(
                id_vars=["магазин", "Проверка","Показатель"],
                var_name="дата",
                value_name="ПЛАН").reset_index(drop=True)


# средний Чеки
plan_aver= plan[[5,777,137,138,139,140,141,142,143,144,145,146,147,148]]
plan_aver= plan_aver.rename(columns=slov_aver)
plan_aver["Показатель"] = "Средний чек"
plan_aver = plan_aver.melt(
                id_vars=["магазин", "Проверка","Показатель"],
                var_name="дата",
                value_name="ПЛАН").reset_index(drop=True)

plan = pd.DataFrame()
plan = pd.concat([plan, plan_check], axis=0).reset_index(drop=True)
plan = pd.concat([plan, plan_aver], axis=0).reset_index(drop=True)
plan = pd.concat([plan, plan_sales], axis=0).reset_index(drop=True)
plan = plan.round(2)
print(plan)

plan.to_excel("C:\\Users\\Lebedevvv\\Desktop\\FRS\\DATA_copy\\♀Планы\\Планы ДЛЯ ДАШБОРДА.xlsx", index=False)
