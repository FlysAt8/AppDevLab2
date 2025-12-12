import redis

# Подключение к Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Проверяем
try:
    r.ping()
    print("Успешное подключение к Redis")
except redis.ConnectionError:
    print("Не удалось подключиться к Redis")

    