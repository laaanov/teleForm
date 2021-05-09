import telebot
from telebot import types

token = '1837504157:AAEbY4VlnY2fFsIk1FCiRb4O5pfYI2guYKQ' # t.me/ilyalanovbot

bot = telebot.TeleBot(token) # Инициализируем бота

keyboard = telebot.types.ReplyKeyboardMarkup(True) # Логика основной кливиатуры
keyboard.row('🔴 Обычный ответ', '🔵 Мультистраничный ответ')

multipage = telebot.types.InlineKeyboardMarkup(row_width=2) # Логика мультистраничной клавиатуры (⬅️ и ➡️)
backbtn = telebot.types.InlineKeyboardButton(text='⬅️', callback_data='back')
forwardbtn = telebot.types.InlineKeyboardButton(text='➡️', callback_data='forward')
multipage.add(backbtn, forwardbtn)

multipage_back = telebot.types.InlineKeyboardMarkup() # Логика мультистраничной клавиатуры (⬅️)
multipage_back.add(telebot.types.InlineKeyboardButton(text='⬅️', callback_data='back_one'))

multipage_forward = telebot.types.InlineKeyboardMarkup() # Логика мультистраничной клавиатуры (➡️)
multipage_forward.add(telebot.types.InlineKeyboardButton(text='➡️', callback_data='forward_one'))

@bot.message_handler(commands=['start']) # Команда /start
def send_welcome(message):
    bot.send_message(message.chat.id, f'*Добрый день.* Я простой бот автоответчик созданный Ильей Лановым. 🤚' + 
    '\n\nУ бота всего одна команда: /start _(показывает это сообщение)_' +
    '\n\n_А для ответа на вопросы, выберите их из меню ниже._', reply_markup=keyboard, parse_mode='Markdown')

@bot.message_handler(content_types=['text']) # Логика ответов на сообщения
def main(message):
    if message.text == '🔴 Обычный ответ': # Обычный ответ
        bot.send_message(message.chat.id, 
        'Здесь может любой ваш текст.' +
        '\n\n*И жирный*, _и курсивный_, `и даже такой.` 😮' +
        '\n😱 А еще могут быть эмодзи. *Сколько угодно!* 😱', parse_mode='Markdown')
    if message.text == '🔵 Мультистраничный ответ': # Мультистраничный ответ
        bot.send_message(message.chat.id, 'Это первая страница с текстом. 🏌️‍♂️', reply_markup=multipage_forward)    

@bot.callback_query_handler(func=lambda call: True) # Ответы с мультистраничной клавиатуры
def query_handler(call):
    bot.answer_callback_query(callback_query_id=call.id)
    answer = ''
    if call.data == 'forward_one':
        answer = 'А тут - вторая. 🏄‍♀️'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=answer, reply_markup=multipage)
    elif call.data == 'back_one':
        answer = 'А тут - вторая. 🏄‍♀️'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=answer, reply_markup=multipage)   
    elif call.data == 'forward':
        answer = 'А здесь уже третья страница. 🏊‍♂️'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=answer, reply_markup=multipage_back)
    elif call.data == 'back':
        answer = 'Это первая страница с текстом. 🏌️‍♂️'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=answer, reply_markup=multipage_forward)

bot.polling(none_stop=True)