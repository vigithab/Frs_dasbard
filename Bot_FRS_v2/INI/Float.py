import sys
sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON\venv\Lib\site-packages")
sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON")


class FLOAT:
    def float_colms(self, name_data, name_col):
        for i in name_col:
            name_data.loc[:, i] = (name_data[i].astype(str)
                                              .str.replace("\xa0", "")
                                              .str.replace(",", ".")
                                              .fillna(0)
                                              .astype("float")
                                              .round(2))
        return name_data
    """Для нескольких столбцов"""
    def float_colm(self, name_data, name_col):

        name_data.loc[:,  name_col] = (name_data[name_col].astype(str)
                                          .str.replace("\xa0", "")
                                          .str.replace(",", ".")
                                          .fillna(0)
                                          .astype("float")
                                          .round(2))
        return name_data
    """для одного столбца"""
        # перевод в число