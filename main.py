import datetime
from pyowm import OWM, commons

from aiogram.types import user
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from config import TOKEN, TOKEN_OWM

# pyowm weather
owm = OWM(TOKEN_OWM)
mgr = owm.weather_manager()

# firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# aiogram telegram_bot
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(msg: types.Message):
    print(type(msg.from_user.id))
    await bot.send_message(msg.from_user.id, "Привет!")


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь!)", reply=False)


def is_place(city, command):
    try:
        observation = mgr.weather_at_place(city)
        return None, True
    except commons.exceptions.APIRequestError:
        return f"Вы не написали название города, пожалуйста напишите рядом с комондой {command} название города.", False

    except:
        return f"Я не знаю что это за город, пожалуйста напишите рядом с комондой {command} название города !!", False


def weather_at_place(city, command=""):
    error_text, flag = is_place(city, command)
    if flag:

        observation = mgr.weather_at_place(city)
        w = observation.weather

        # Температура
        temp = w.temperature('celsius')
        temp_cels = temp['temp']
        temp_feels = temp['feels_like']
        temp_max = temp['temp_max']
        temp_min = temp['temp_min']
        # Скорость ветра
        wind = w.wind()['speed']
        # Влажность
        humi = w.humidity
        # Статус
        status = w.status
        # Время
        time = datetime.datetime.fromtimestamp(w.reference_time())
        # Давление
        pressure = w.pressure['press']
        # Видимость
        vis_dis = w.visibility_distance
        # Продолжительность дня
        sunrise_time = datetime.datetime.fromtimestamp(w.sunrise_time())
        sunset_time = datetime.datetime.fromtimestamp(w.sunset_time())
        length_of_the_day = sunset_time - sunrise_time


        code_to_smile = {
            "Clear": "Ясно \U00002600",
            "Clouds": "Облачно \U00002601",
            "Rain": "Дождь \U00002614",
            "Drizzle": "Дождь \U00002614",
            "Thunderstorm": "Гроза \U000026A1",
            "Snow": "Снег \U0001F328",
            "Mist": "Туман \U0001F32B"
        }

        return(
            f"Время прогноза: {time}\n"
            f"В городе {city.capitalize()} температура: {temp_cels}C°, ощущается как: {temp_feels}C°\n"
            f"Максимальная температура: {temp_max}C°, минимальная температура: {temp_min}C°.\n"
            f"Скорость ветера: {wind}м/с\n"
            f"Влажность: {humi}%\n"
            f"Давление: {pressure} мм.рт.ст\n"
            f"Восход солнца: {sunrise_time}\nЗакат солнца: {sunset_time}\nПродолжительность дня: {length_of_the_day}\n"
            f"Видимость: {vis_dis} м\n"
            f"Статус: {code_to_smile[status]}" 
        )

    else:
        return error_text    


@dp.message_handler(commands=['weather_at_place'])
async def process_start_command(msg: types.Message):
    city = msg.get_args()
    await msg.reply(weather_at_place(city, "/weather_at_place"), reply=False)


@dp.message_handler(commands=['set_place'])
async def process_start_command(msg: types.Message):
    city = msg.get_args().capitalize()

    error_text, flag = is_place(city, "/set_place")

    if flag:
        doc_ref = db.collection(u'user').document(str(msg.from_user.id))
        doc_ref.set({
            u'city': city
        })

        await msg.reply(f"Город {city} добавлен в избранные.", reply=False)

    else:
        await msg.reply(error_text, reply=False)


@dp.message_handler(commands=['weather'])
async def process_start_command(msg: types.Message):
    users_ref = db.collection(u'user')
    result = users_ref.document(str(msg.from_user.id)).get()

    if result.exists:
        await msg.reply(weather_at_place(result.to_dict()['city']), reply=False)
    else:
        await msg.reply("У вас нету избранного города, пожалуйста довте спощю команды /set_place.", reply=False)

if __name__ == '__main__':
    executor.start_polling(dp)
