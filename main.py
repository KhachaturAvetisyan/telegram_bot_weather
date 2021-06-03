import pyowm
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
    print(msg.get_args())
    try:
        owm = pyowm.OWM(TOKEN_OWM)
        mgr = owm.weather_manager()

        observation = mgr.weather_at_place(msg.get_args())
        w = observation.weather

        temp_cels = w.temperature('celsius')['temp']
        temp_far = w.temperature('fahrenheit')['temp']

        await msg.reply(f"tempriture in celsius = {temp_cels}°C\ntempriture in farengate = {temp_far}°F", reply=False)
    except pyowm.commons.exceptions.APIRequestError:
        await msg.reply("Вы не написали город пожалуйста напишхите рядом с комондой /weather название города. ))", reply=False)
    except:
        await msg.reply("Я не знаю что это за город !!))", reply=False)


if __name__ == '__main__':
    executor.start_polling(dp)
