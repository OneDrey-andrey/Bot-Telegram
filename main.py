import os
import random
import telebot
from telebot import types

# Замените 'YOUR_TELEGRAM_BOT_TOKEN' на ваш фактический токен бота
TOKEN = '8028254505:AAEtGeZ22Vet3HFPdncg7SBX2jxCBKV6jC0'

# Замените 'PATH_TO_SCREENSHOTS_DIRECTORY' на фактический путь к вашей папке скриншотов
SCREENSHOTS_DIR = 'C:\АРБИТРАЖ\mines\screenshot'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton("🔥ПРОГНОЗ🔥")
    keyboard.add(button)
    bot.send_message(message.chat.id, 'Нажмите кнопку, ЧТО БЫ ПОЛУЧИТЬ🔥ПРОГНОЗ🔥:', reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == "🔥ПРОГНОЗ🔥")
def send_screenshot(message):
    # Получаем список всех файлов в папке скриншотов
    files = os.listdir(SCREENSHOTS_DIR)

    # Фильтруем файлы, которые не являются изображениями
    image_files = [f for f in files if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    if not image_files:
        bot.send_message(message.chat.id, 'Прогнозы закончились, ожидайте.')
        return

    # Выбираем случайный файл изображения
    random_image = random.choice(image_files)

    # Отправляем изображение пользователю
    with open(os.path.join(SCREENSHOTS_DIR, random_image), 'rb') as photo:
        bot.send_photo(message.chat.id, photo)

if __name__ == '__main__':
    bot.polling()