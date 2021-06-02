import telebot

bot = telebot.TeleBot('1668003573:AAFXUbOwttrHG7xUFjwhZfRdfdEYIie0MGg')

keyboard_1 = telebot.types.ReplyKeyboardMarkup()

btn_1 = telebot.types.KeyboardButton('1')
btn_2 = telebot.types.KeyboardButton('2')
btn_3 = telebot.types.KeyboardButton('3')
btn_4 = telebot.types.KeyboardButton('4')
btn_5 = telebot.types.KeyboardButton('5')
btn_6 = telebot.types.KeyboardButton('6')
btn_7 = telebot.types.KeyboardButton('7')
btn_8 = telebot.types.KeyboardButton('8')
btn_9 = telebot.types.KeyboardButton('9')

btn_count = telebot.types.KeyboardButton('Считать!')

keyboard_1.row(btn_1,btn_2,btn_3)
keyboard_1.row(btn_4,btn_5,btn_6)
keyboard_1.row(btn_7,btn_8,btn_9)
keyboard_1.row(btn_count)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start',reply_markup=keyboard_1)

@bot.message_handler(content_types=['text'])
def go_txt(message):
    if message.text == 'Привет' :
        bot.send_message(message.chat.id , 'Дароу')
    elif message.text == 'Пока' :
        bot.send_message(message.chat.id , 'Прощай')
    elif message.text == 'ха-ха' :
        bot.send_sticker(message.chat.id, 'CAADAgADcwgAAhhC7ggBnQGJ6b93ggI')
    elif message.text == 'Считать!' :
        bot.send_message(message.chat.id, 'Введите первое число : ')
        @bot.message_handler(content_types=['text'])
        def count_1(message):
            firsnum = message
            bot.send_message(message.chat.id, 'Введите второе число : ')
            @bot.message_handler(content_types=['text'])
            def count_2(message):
                secnum = message

                bot.send_message(message.chat.id ,secnum + firsnum )

bot.polling()