import pandas as pd
from Bot_FRS_v2.INI import ini

pd.set_option("expand_frame_repr", False)
pd.set_option('display.max_colwidth', None)

PUT = ini.PUT
# справочник штрих кода с нси
x = pd.read_csv(PUT + "Справочники\\номенклатура\\Справочник номеклатуры.txt", sep="\t",encoding="utf-8")
# добавлеие скю
y = pd.read_excel(PUT + "Справочники\\номенклатура\\Добавить номенклатуру.xlsx")
# справочник групп продактов
prodct = pd.read_excel("https://docs.google.com/spreadsheets/d/1dNt8qpZL_ST8aF_iBqV7oVQvH1tsExMd6uLCiC_UtfQ/export?exportFormat=xlsx" )
# загрузка крупной группы
grup = pd.read_csv(PUT + "Справочники\\номенклатура\\Список.txt", sep="\t",encoding="utf-8")
grup  = grup .drop("Входит в группу", axis=1)
grup = grup.rename(columns={"Входит в группу.1": "Входит в группу","Группа для доставки (Справочник \"Номенклатура\")":"Старшая группа"})
print(grup )
union = pd.concat([x,y],axis=0).reset_index(drop=True)
#union =union.loc[union["Владелец"] == "Пирожное Боровикова Муссовое Праздничное 60 г"]

#union = union.loc[union["Входит в группу"] ==  "Кондитерские изделия КМ"]
union = union.merge(prodct,on=["Входит в группу"], how="left")
print(union)
#union = union.merge(grup[["Входит в группу","Старшая группа"]],on=["Входит в группу"], how="left")
union["Входит в группу"] = union["Входит в группу"].str.replace(" ВЫВЕДЕННЫЕ", "")
union["Входит в группу"] = union["Входит в группу"].str.replace("Выведено  ","")
union["Входит в группу"] = union["Входит в группу"].str.replace("Выведено ","")
union = union.loc[union["Владелец"].notnull()]

union.to_csv(PUT + "Справочники\\номенклатура\\обработаный справочник.csv", sep=";", encoding="utf-8", index=False)

print(union)