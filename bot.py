import os
import telebot
from pytube import YouTube

# Токен бота
TOKEN = os.getenv("BOT_TOKEN")  # Переменная окружения на Railway
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Отправь мне ссылку на YouTube-видео, и я скачаю его для тебя.")

@bot.message_handler(func=lambda message: message.text.startswith("https://www.youtube.com") or message.text.startswith("https://youtu.be"))
def download_video(message):
    url = message.text
    bot.reply_to(message, "Загружаю видео, подожди...")

    try:
        yt = YouTube(url)

        # Выбираем поток с наилучшим качеством (MP4)
        video = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first()

        # Загружаем видео
        file_path = video.download()

        # Отправляем видео пользователю
        with open(file_path, "rb") as video_file:
            bot.send_video(message.chat.id, video_file)

        # Удаляем видео после отправки
        os.remove(file_path)

    except Exception as e:
        bot.reply_to(message, f"Ошибка при скачивании: {e}")

bot.infinity_polling()  # Используем infinity_polling для Railway
