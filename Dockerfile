# Берём официальную версию Python с Docker Hub
FROM python:3.13

# Обновим пакеты, установим зависимости для сборки (если понадобятся)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Создаём рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё приложение внутрь контейнера
COPY . .

# Делаем entrypoint.sh исполняемым
RUN chmod +x entrypoint.sh

# Открываем порт приложения (если uvicorn слушает 8000)
EXPOSE 8000

# Точка входа
ENTRYPOINT ["./entrypoint.sh"]
