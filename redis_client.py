import redis

# Подключение к Redis
client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

print()
# Установка и получение строки
client.set("user:name", "Иван")
name = client.get("user:name")
print("Имя пользователя: ", name)

# Установка строки с TTL (время жизни)
client.setex("session:123", 3600, "active")  # 1 час
session = client.get("session:123")
print("Сессия: ", session)

# Работа с числами (строки, интерпретируемые как числа)
client.set("counter", 0)
client.incr("counter")        # +1
client.incrby("counter", 5)   # +5
client.decr("counter")        # -1
counter = client.get("counter")
print("Счётчик:", counter)

# Очистим список для чистого теста
client.delete("tasks")
# Работа со списками
print()
client.lpush("tasks", "task1", "task2")
client.rpush("tasks", "task3", "task4")

tasks = client.lrange("tasks", 0, -1)
print("Задания: ", tasks)

first = client.lpop("tasks")
last = client.rpop("tasks")
print("Первый элемент:", first)
print("Последний элемент:", last)
tasks = client.lrange("tasks", 0, -1)
print("Задания: ", tasks)

# Получение длины списка
length = client.llen("tasks")
print("Оставшееся количество задач:", length)

# Получение элемента по индексу
second = client.lindex("tasks", 1)
print("Элемент с индексом 1:", second)
tasks = client.lrange("tasks", 0, -1)
print("Задания: ", tasks)


print()
# Работа с множестами
client.sadd("tags", "python", "redis", "database")
client.sadd("languages", "python", "java", "javascript")

is_member = client.sismember("tags", "python")
print("Есть ли python в tags:", is_member)

all_tags = client.smembers("tags")
print("Все теги:", all_tags)

intersection = client.sinter("tags", "languages")
print("Одинаковые элементы':", intersection)
union = client.sunion("tags", "languages")
print("Элементы вместе без повтора:", union)
difference = client.sdiff("tags", "languages")
print("Теги без общих:", difference)


print()
# Работа с хэшами
client.hset("user:1000", mapping={
    "name": "Иван",
    "age": 30,
    "sity": "Москва"
})

name = client.hget("user:1000", "name")
print("Имя: ", name)
all_data = client.hgetall("user:1000")
print("Все данные:", all_data)

exists = client.hexists("user:1000", "email")
print("Сеществование поля email:", exists)

keys = client.hkeys("user:1000")
value = client.hvals("user:1000")
print("Все ключи:", keys)
print("Все значения:", value)


print()
# Упорядоченные множества
client.zadd("leaderboard", {
    "player1": 100,
    "player2": 200,
    "player3": 50,
})

top_players = client.zrange("leaderboard", 0, -1, withscores=True)
print("TOP ALL Players: ", top_players)

players_by_score = client.zrangebyscore("leaderboard", 100, 200)
print("Players(100-200): ", players_by_score)

rank = client.zrank("leaderboard", "player2")
print("RANK Player2 - ", rank)