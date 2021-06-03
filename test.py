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


@dp.message_handler(commands=['reply'])
async def reply_text(message: types.Message):
	await message.reply(message.get_args(), reply=True)


# @dp.message_handler()
# async def echo_message(msg: types.Message):
#     await bot.send_message(msg.from_user.id, msg.text)


# @dp.message_handler(commands=['weather'])
# async def process_start_command(msg: types.Message):
#     await bot.send_message(msg.from_user.id, "Введите город.") 

#     @dp.message_handler(content_types=['text'])
#     async def print_city(message):
#         # print(message.text)
#         await temp_at_city(message.text)


#     async def temp_at_city(city):
#         try:
#             owm = pyowm.OWM(TOKEN_OWM)
#             mgr = owm.weather_manager()

#             observation = mgr.weather_at_place(city)
#             w = observation.weather

#             temp_cels = w.temperature('celsius')['temp']
#             temp_far = w.temperature('fahrenheit')['temp']

#             await bot.send_message(msg.from_user.id, f"tempriture in celsius = {temp_cels}°C\ntempriture in farengate = {temp_far}°F")
#         except:
#             await bot.send_message(msg.from_user.id, "Я не знаю что это за город !!))")


if __name__ == '__main__':
    executor.start_polling(dp)
