import datetime

from pyowm import OWM, commons
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN, TOKEN_OWM

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(msg: types.Message):
    await bot.send_message(msg.from_user.id, "Привет!\nНапиши мне что-нибудь!")


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!", reply=False)


# @dp.message_handler()
# async def echo_message(msg: types.Message):
#     await bot.send_message(msg.from_user.id, msg.text)


@dp.message_handler(commands=['weather'])
async def process_start_command(msg: types.Message):
    # print(msg.get_args())
    try:
        city = msg.get_args()
        owm = OWM(TOKEN_OWM)
        mgr = owm.weather_manager()
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
        time = w.reference_time('iso')
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

        await msg.reply(
            f"Время: {time}\n"
            f"В городе {city.capitalize()} температура: {temp_cels}C°, ощущается как: {temp_feels}C°\n"
            f"Максимальная температура: {temp_max}C°, минимальная температура: {temp_min}C°.\n"
            f"Скорость ветера: {wind}м/с\n"
            f"Влажность: {humi}%\n"
            f"Давление: {pressure} мм.рт.ст\n"
            f"Восход солнца: {sunrise_time}\nЗакат солнца: {sunset_time}\nПродолжительность дня: {length_of_the_day}\n"
            f"Видимость: {vis_dis} м\n"
            f"Статус: {code_to_smile[status]}", 
            reply=False)

    except commons.exceptions.APIRequestError:
        await msg.reply("Вы не написали город пожалуйста напишхите рядом с комондой /weather название города. ))", reply=False)

    except:
        await msg.reply("Я не знаю что это за город !!))", reply=False)


if __name__ == '__main__':
    executor.start_polling(dp)
