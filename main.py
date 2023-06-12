
import time
start_time = time.time()
user_response = None
timeout = 10

user_input = input("завершить")
while True:
    if user_input.lower() == 'y':
        print("ОСТАНОВЛЕН")
        break
    print(time.time() - start_time > timeout)
    if time.time() - start_time > timeout:
        print("ОСТАНОВЛЕН dhtvz")
        break