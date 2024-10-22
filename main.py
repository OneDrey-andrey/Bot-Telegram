import os
import random
import boto3
from telebot import TeleBot, types

# Получение токена бота из переменной среды
TOKEN = os.getenv('TOKEN')

# Создание бота
bot = TeleBot(TOKEN)

# Настройки S3
S3_BUCKET = os.getenv('S3_BUCKET')
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton("🔥ПРОГНОЗ🔥")
    keyboard.add(button)
    bot.send_message(message.chat.id, 'Нажмите кнопку, чтобы получить 🔥ПРОГНОЗ🔥:', reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == "🔥ПРОГНОЗ🔥")
def send_screenshot(message):
    # Получаем список файлов из бакета
    response = s3_client.list_objects_v2(Bucket=S3_BUCKET)
    files = [obj['Key'] for obj in response.get('Contents', [])]

    # Фильтруем файлы, которые не являются изображениями
    image_files = [f for f in files if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    if not image_files:
        bot.send_message(message.chat.id, 'Прогнозы закончились, ожидайте.')
        return

    # Выбираем случайный файл изображения
    random_image = random.choice(image_files)

    # Загружаем изображение с S3
    image_url = f'https://{S3_BUCKET}.s3.amazonaws.com/{random_image}'
    bot.send_photo(message.chat.id, image_url)

if __name__ == '__main__':
    bot.polling()
