# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Настройки среды
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Рабочая директория
WORKDIR /app

# Копируем код (включая requirements.txt) и ставим зависимости
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

# Команда запуска (Railway определит как процесс контейнера)
CMD ["python", "main.py"]

