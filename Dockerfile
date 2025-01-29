# Используем базовый образ Python
FROM python:3.9-slim

# Устанавливаем ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Устанавливаем зависимости Python
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

# Копируем все файлы проекта
COPY . /app/

# Запуск вашего бота
CMD ["python", "bot.py"]
