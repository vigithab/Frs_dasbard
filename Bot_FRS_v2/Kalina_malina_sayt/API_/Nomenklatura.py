import json
import time

import pandas as pd

import requests


pd.set_option("expand_frame_repr", False)
pd.set_option('display.max_colwidth', None)

def get_data_and_print_table_2(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame.from_dict(data["data"])
            # Преобразовываем столбец 'farmer' из словаря в отдельные столбцы
            farmer_df = pd.json_normalize(df['farmer'])
            # Добавляем новые столбцы к основной таблице df
            df = pd.concat([df, farmer_df], axis=1)
            # Удаляем столбец 'farmer', если не нужен
            df.drop(columns=['farmer'], inplace=True)

            # Извлекаем значения 'title' из словарей в столбце 'groups' и объединяем их в строку, разделенную запятыми
            df['title_grups'] = df['groups'].apply(lambda x: ', '.join(item['title'] for item in x))
            df['image_blur_hash_grups'] = df['groups'].apply(lambda x: ', '.join(item['image_blur_hash'] for item in x))
            df['image_grups'] = df['groups'].apply(lambda x: ', '.join(item['image'] for item in x))
            df['id_grups'] = df['groups'].apply(lambda x: ', '.join(str(item['id']) for item in x))
            df.drop(columns=['groups'], inplace=True)
            df.drop(columns=['delivery_dates'], inplace=True)

            print(df)


            # Проверяем, что данные не пусты
            if not data:
                print("Данные не найдены.")
                return
            return df
        else:
            print(f"Ошибка при выполнении запроса: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print("Ошибка при выполнении запроса:", e)



data_df = pd.DataFrame()
ln = list(range(1,217))
for i in ln:
    try:
        time.sleep(1)
        # Пример использования функции для запроса списка категорий
        url_categories = f"https://admin.kalina-malina.ru/api/v1/products/?page={i}&assortment_date=24.07.2023&limit=15"
        x = get_data_and_print_table_2(url_categories)

        data_df = pd.concat([data_df, x], axis=0).reset_index(drop=True)

        # Удаление дубликатов по всем столбцам
        data_df = data_df.drop_duplicates().reset_index(drop=True)
        print(f"____________________________________________________{i}")
    except Exception as e:
        print(f"Ошибка при обработке страницы {i}: {e}")
translation_dict = {
    'id': 'идентификатор',
    'image': 'изображение',
    'image_blur_hash': 'хеш_размытия_изображения',
    'title': 'заголовок',
    'slug': 'идентификатор_в_ссылке',
    'rating': 'рейтинг',
    'unit': 'единица_измерения',
    'weight': 'вес',
    'in_stock': 'в_наличии',
    'price': 'цена',
    'price_discount': 'скидочная_цена',
    'price_unit': 'единица_измерения_цены',
    'date_supply': 'дата_поставки',
    'delivery_in_country': 'доставка_в_страну',
    'by_preorder': 'предзаказ',
    'cooking': 'приготовление',
    'available_count': 'доступное_количество',
    'can_buy': 'можно_купить',
    'favorited': 'в_избранном',
    'name': 'наименование',
    'title_grups': 'заголовок_группы',
    'image_blur_hash_grups': 'хеш_размытия_изображения_группы',
    'image_grups': 'изображение_группы',
    'id_grups': 'идентификатор_группы'
}

data_df.rename(columns=translation_dict, inplace=True)
data_df.to_excel(r"C:\Users\lebedevvv\Desktop\FRS\PYTHON\Bot_FRS_v2\Kalina_malina_sayt\1.xlsx", index=False)

