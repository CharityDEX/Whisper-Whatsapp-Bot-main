# Python 3.11 (slim)
FROM python:3.11-slim

# Устанавливаем рабочий каталог
WORKDIR /app

# Обновляем списки пакетов и устанавливаем необходимые зависимости
RUN apt-get update \
    && apt-get install -y ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл с зависимостями
COPY requirements.txt .

# Обновляем pip и устанавливаем зависимости
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Копируем остальные файлы проекта
COPY . .

# Команда по умолчанию при запуске контейнера
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7729"]
