import telebot
import requests
import json

bot = telebot.TeleBot('1668003573:AAFXUbOwttrHG7xUFjwhZfRdfdEYIie0MGg')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start')


@bot.message_handler(commands=['weather'])
def weather_message(message):
    bot.send_message(message.chat.id, 'Напишите город:')
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton('°F', callback_data='get-F'),
        telebot.types.InlineKeyboardButton('°C', callback_data='get-C')
    )

    @bot.message_handler(content_types=['text'])
    def send_text(message):
        try:
            resp = requests.get(
                f'http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid=9b6cbef84565796f8f8e2c2d0f05f5e2')
            temp = resp.json()['main']['temp']
            temp_C = float(temp) - 273.15
            temp_F = float(temp) - 273.15 * 9 / 5 + 32

            @bot.callback_query_handler(func=lambda call: True)
            def iq_callback(query):
                data = query.data
                if data.startswith('get-F'):
                    get_F()
                elif data.startswith('get-C'):
                    get_C()

            def get_F():
                return bot.send_message(message.chat.id, f'axpers an ver kal {temp_F}🌡️')

            def get_C():
                return bot.send_message(message.chat.id, f'axpers an ver kal {temp_C}🌡️')

            if temp:
                bot.send_message(message.chat.id, 'Jigyar mi ban ara sranq yan tan ha mek el @ntri inch es uzum',
                                 reply_markup=keyboard)
        except:
            print("chi ashxatuuum")


bot.polling(none_stop=True)
