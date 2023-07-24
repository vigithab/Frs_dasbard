import json
import pandas as pd

pd.set_option("expand_frame_repr", False)
pd.set_option('display.max_colwidth', None)




import json
import pandas as pd

# Чтение данных из текстового файла в формате JSON
with open(r'C:\Users\lebedevvv\Desktop\сайт\Заказ 28933.txt', 'r', encoding="utf-8") as file:
    data = json.load(file)

# Функция для извлечения значений из словарей внутри списка
def extract_value(row, key):
    return row[key] if key in row else None

# Создание списка для таблицы
table_data = []

# Проходимся по каждому элементу в списке data
for item in data:
    # Извлекаем значения из вложенного словаря "contacts"
    contacts = item['contacts']
    phone = extract_value(contacts, 'phone')
    name = extract_value(contacts, 'name')
    email = extract_value(contacts, 'email')
    address = extract_value(contacts, 'address')
    apartment = extract_value(contacts, 'apartment')
    floor = extract_value(contacts, 'floor')
    entrance = extract_value(contacts, 'entrance')
    has_elevator = extract_value(contacts, 'has_elevator')

    # Проходимся по каждому продукту в заказе
    for product in item['products']:
        # Извлекаем значения из словаря "products"
        product_id = product['1c_id']
        count = product['count']
        price = product['price']
        price_buy = product['price_buy']
        total = product['total']
        total_without_discount = product['total_without_discount']
        unit_1c_id = product['unit_1c_id']

        # Добавляем данные в список для таблицы
        table_data.append([item['1c_id'], item['status'], item['payment_type'], item['delivery_type'], item['comment'],
                           item['promo'], item['receive_date'], item['receive_interval'], item['contactless'],
                           phone, name, email, address, apartment, floor, entrance, has_elevator,
                           product_id, count, price, price_buy, total, total_without_discount, unit_1c_id])

# Создание таблицы с помощью pandas
columns = ['order_id', 'status', 'payment_type', 'delivery_type', 'comment', 'promo', 'receive_date', 'receive_interval',
           'contactless', 'phone', 'name', 'email', 'address', 'apartment', 'floor', 'entrance', 'has_elevator',
           'product_id', 'count', 'price', 'price_buy', 'total', 'total_without_discount', 'unit_1c_id']
df = pd.DataFrame(table_data, columns=columns)

# Вывод таблицы
print(df)