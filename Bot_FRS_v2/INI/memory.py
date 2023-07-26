import sys
sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON\venv\Lib\site-packages")
sys.path.append(r"C:\Users\Lebedevvv\Desktop\FRS\PYTHON")
import psutil


class MEMORY:
    def mem(self, x, text):
        total_memory = x.memory_usage(deep=True).sum()
        print(text + " - Использовано памяти: {:.2f} MB".format(total_memory / 1e6))
    """использование памяти датафрейм"""
    def mem_total(self,x):
        process = psutil.Process()
        memory_info = process.memory_info()
        total_memory = memory_info.rss
        print(x +" - Использование памяти: {:.2f} MB".format(total_memory / 1024 / 1024))
    """использование памяти программой полная"""
        # Память