import telebot
from pytube import YouTube
import os

TOKEN = os.getenv("BOT_TOKEN")  # Railway хранит токен в переменных окружения
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
        video = yt.streams.get_highest_resolution()
        file_path = video.download()

        with open(file_path, "rb") as video_file:
            bot.send_video(message.chat.id, video_file)

        os.remove(file_path)  # Удаляем видео после отправки

    except Exception as e:
        bot.reply_to(message, f"Ошибка при скачивании: {e}")

bot.infinity_polling()  # Используем infinity_polling для Railway
