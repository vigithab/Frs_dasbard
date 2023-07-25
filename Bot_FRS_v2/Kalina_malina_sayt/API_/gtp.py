import pandas as pd
import requests
#import API_.Grups_name as groop
from tabulate import tabulate

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
            #df['image_blur_hash_grups'] = df['groups'].apply(lambda x: ', '.join(item['image_blur_hash'] for item in x))
            #df['image_grups'] = df['groups'].apply(lambda x: ', '.join(item['image'] for item in x))
            df['id_grups'] = df['groups'].apply(lambda x: ', '.join(str(item['id']) for item in x))
            df.drop(columns=['groups'], inplace=True)
            df.drop(columns=['delivery_dates'], inplace=True)



            # Проверяем, что данные не пусты
            if not data:
                print("Данные не найдены.")
                return
            return df
        else:
            print(f"Ошибка при выполнении запроса: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print("Ошибка при выполнении запроса:", e)


# Пример использования функции для запроса списка категорий
url_categories = f"https://admin.kalina-malina.wearefullstack.ru/api/v1/products?search_text=Бифидокефир \"Капелька\" 3,2% 200 г"
x = get_data_and_print_table_2(url_categories)
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
x.rename(columns=translation_dict, inplace=True)
headers = x.columns.tolist()
print(tabulate(x, headers=headers, tablefmt='grid', numalign="center"))
x.to_excel(r"C:\Users\borsh\Desktop\Python\группа2.xlsx", index=False)




