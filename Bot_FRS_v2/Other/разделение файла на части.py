python
import csv
import os


def split_file(file_path, chunk_size):
    file_name = os.path.basename(file_path)
    file_dir = os.path.dirname(file_path)

    # Открытие оригинального файла для чтения
    with open(file_path, "r") as input_file:
        reader = csv.reader(input_file)
        header = next(reader)  # Считывание заголовка

        # Создание новых файлов частей и запись данных
        i = 0
        current_chunk_size = 0
        output_file = None

        for row in reader:
            # Создание новой части, когда размер текущей части превышает указанный размер
            if current_chunk_size + len(",".join(row)) + len("\n") > chunk_size:
                if output_file is not None:
                    output_file.close()

                i += 1
                chunk_filename = f"{file_name}_part{i}.csv"
                chunk_filepath = os.path.join(file_dir, chunk_filename)
                output_file = open(chunk_filepath, "w", newline="")
                writer = csv.writer(output_file)
                writer.writerow(header)
                current_chunk_size = 0

            writer.writerow(row)
            current_chunk_size += len(",".join(row)) + len("\n")

        if output_file is not None:
            output_file.close()

        print(f"Split file into {i} parts.")


# Пример использования
file_path = "путь_к_вашему_файлу.csv"
chunk_size = 20 * 1024 * 1024  # 20 МБ

split_file(file_path, chunk_size)

# Пример использования
file_path = r"C:\Users\Lebedevvv\Desktop\Новая папка (2)\Яндекс Еда.txt"
chunk_size = 19 * 1024 * 1024  # 20 МБ

split_file(file_path, chunk_size)