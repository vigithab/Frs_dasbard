import requests


url = 'http://10.32.2.51:8443/operday/checks'

# Выполняем GET-запрос
response = requests.get(url)

# Проверяем статус-код ответа
if response.status_code == 200:
    # Выводим содержимое ответа
    print(response.text)
else:
    # В случае ошибки выводим сообщение
    print(f'Ошибка при выполнении запроса: {response.status_code}')