import os
import telebot
import youtube_dl

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
        # Параметры для youtube_dl
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',  # Загружаем лучшее видео и аудио
            'outtmpl': 'downloads/%(id)s.%(ext)s',  # Путь для сохранения
            'quiet': True,  # Без лишних выводов
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_file = ydl.prepare_filename(info_dict)  # Получаем путь к файлу

        # Отправляем видео пользователю
        with open(video_file, 'rb') as video:
            bot.send_video(message.chat.id, video)

        # Удаляем видео после отправки
        os.remove(video_file)

    except Exception as e:
        bot.reply_to(message, f"Ошибка при скачивании: {e}")

bot.infinity_polling()  # Используем infinity_polling для Railway
