import pymysql

# Замените следующие данные на свои реквизиты для подключения к MySQL
db_config = {
    "host": "45.147.179.148",
    "database": "",  # Это поле можно оставить пустым
    "user": "root",
    "password": "fA%^E2snXgT6"
}

# Подключение к MySQL
conn = pymysql.connect(**db_config)

# Получение списка баз данных
cursor = conn.cursor()
cursor.execute("SHOW DATABASES;")
databases = [row[0] for row in cursor.fetchall()]

print("Список баз данных:")
print(databases)

"""# Выбор базы данных (здесь мы выбираем первую базу из списка)
selected_database = databases[0]
cursor.execute(f"USE {selected_database};")

# Получение списка таблиц в выбранной базе данных
cursor.execute("SHOW TABLES;")
tables = [row[0] for row in cursor.fetchall()]

print(f"Список таблиц в базе данных {selected_database}:")
print(tables)"""

# Закрываем курсор и соединение
cursor.close()
conn.close()