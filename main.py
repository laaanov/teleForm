import telebot
from telebot import types

token = '1837504157:AAEbY4VlnY2fFsIk1FCiRb4O5pfYI2guYKQ' # t.me/ilyalanovbot

bot = telebot.TeleBot(token) # Инициализируем бота

keyboard = telebot.types.ReplyKeyboardMarkup(True) # Логика основной кливиатуры
keyboard.row('🔴 Обычный ответ')

@bot.message_handler(commands=['start']) # Команда /start
def send_welcome(message):
    bot.send_message(message.chat.id, f'*Добрый день.* Я простой бот автоответчик созданный командой Spatix. 🤚' + 
    '\n\nУ бота всего одна команда: /start _(показывает это сообщение)_' +
    '\n\n_А для ответа на вопросы, выберите их из меню ниже._', reply_markup=keyboard, parse_mode='Markdown')

@bot.message_handler(content_types=['text']) # Логика ответов на сообщения
def main(message):
    if message.text == '🔴 Обычный ответ': # Обычный ответ
        bot.send_message(message.chat.id, 
        'Здесь может любой ваш текст.' +
        '\n\n*И жирный*, _и курсивный_, `и даже такой.` 😮' +
        '\n😱 А еще могут быть эмодзи. *Сколько угодно!* 😱', parse_mode='Markdown')

bot.polling(none_stop=True)