import psycopg2

# Установка параметров подключения к базе данных
conn = psycopg2.connect(
    host="10.32.2.13",
    port="5432" ,
    database="docs",
    user="postgres",
    password="postgres"
)

# Создание курсора
cursor = conn.cursor()

# Выполнение запроса на получение названий всех баз данных
cursor.execute("SELECT datname FROM pg_catalog.pg_database")

# Извлечение результатов запроса
database_names = [row[0] for row in cursor.fetchall()]

# Закрытие курсора и соединения
cursor.close()
conn.close()

# Вывод названий баз данных
for database_name in database_names:
    print(database_name)