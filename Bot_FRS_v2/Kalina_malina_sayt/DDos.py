import asyncio
import aiohttp
import time

# Функция для отправки асинхронных запросов и измерения времени ответа
async def send_request(session, url):
    try:
        start_time = time.time()
        async with session.get(url) as response:
            end_time = time.time()
            response_time = end_time - start_time
            print(f"Потоки: {url} выполнены, статус: {response.status}, время ответа: {response_time:.2f} сек")
            return response_time
    except aiohttp.ClientError as e:
        print(f"Потоки: {url} ошибка при отправке запроса: {e}")
        return None

# Определите URL-адрес, который вы хотите протестировать
url = "https://kalina-malina.ru/"

# Запуск асинхронных запросов с постепенным увеличением количества потоков до 49
async def main():
    for num_threads in range(15, 50):
        print(f"\nТестирование с {num_threads} потоками:")
        async with aiohttp.ClientSession() as session:
            tasks = []
            for _ in range(num_threads):
                tasks.append(send_request(session, url))
            # Отправка асинхронных запросов
            responses = await asyncio.gather(*tasks)
            # Здесь вы можете выполнить дополнительные действия с результатами, если необходимо

# Запуск асинхронной программы
loop = asyncio.get_event_loop()
loop.run_until_complete(main())