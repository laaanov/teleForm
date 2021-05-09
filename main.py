import telebot
from telebot import types

token = '1837504157:AAEbY4VlnY2fFsIk1FCiRb4O5pfYI2guYKQ' # t.me/ilyalanovbot
channelid = '-1001486961983' # Просто лень создавать новый канал для теста заявок ¯\_(ツ)_/¯

bot = telebot.TeleBot(token) # Инициализируем бота

keyboard = telebot.types.ReplyKeyboardMarkup(True) # Логика основной кливиатуры
keyboard.row('🔴 Обычный ответ', '🔵 Мультистраничный ответ')
keyboard.row('ℹ️ Оставить заявку')

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
    if message.text == 'ℹ️ Оставить заявку': # Запрос на то, чтобы оставить заявку
        request_message = bot.send_message(message.chat.id, 
        '*🔥 Заинтересованы в наших услугах?*' +
        '\n\nОставьте заявку уже сейчас!' +
        '\nКстати, пример получения заявки можно посмотреть в @spatixtest' +
        '\n\n*Пример заполнения заявки:*' +
        '\n1. Ваше имя.' +
        '\n2. Ваш пол.' +
        '\n3. Да и впринципе все что угодно. :)', parse_mode='Markdown')
        bot.register_next_step_handler(request_message, create_request)

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

def create_request(message): # Отправка заявки
    if message.text == '🔴 Обычный ответ' or '🔵 Мультистраничный ответ' or 'ℹ️ Оставить заявку':
        bot.send_message(message.chat.id, '✅ Мы получили вашу заявку. Спасибо!')
        bot.send_message(channelid, 
        '❗️ *Новая заявка!*\n\n*Пользователь:* @{0}\n\n*Текст заявки:*\n{1}'
        .format(message.from_user.username, message.text), parse_mode='Markdown')   
    else:
        bot.clear_step_handler(message)
        bot.send_message(message.chat.id, '⛔️ *Ошибка!* Запустите функцию отправки заявки заново.', parse_mode='Markdown')

bot.polling(none_stop=True)