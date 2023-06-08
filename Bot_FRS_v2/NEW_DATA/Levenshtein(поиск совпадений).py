import pandas as pd
from fuzzywuzzy import fuzz, process
import pandas as pd
from Bot_FRS_v2.INI import ini

pd.set_option("expand_frame_repr", False)
pd.set_option('display.max_colwidth', None)

PUT = ini.PUT
# Загрузка датафрейма с номенклатурой
df = pd.read_csv(PUT + "Справочники\\номенклатура\\Справочник номеклатуры.txt", sep = "\t", encoding="utf-8")

print(df)
# Задайте строку, для которой нужно найти похожие значения
query = "Грудка куриная ГРИЛЬ, шт"

# Получите список всех значений из столбца "владелец"
owners = df["Владелец"].unique()

# Используйте функцию process.extract() для получения 10 наиболее похожих значений
matches = process.extract(query, owners, limit=10)

# Выведите результаты
for match in matches:
    print(match[0])





