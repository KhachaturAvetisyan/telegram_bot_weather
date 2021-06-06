from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from config import TOKEN, TOKEN_OWM

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class reg_city(StatesGroup):
    city = State()


@dp.message_handler(commands=['start'])
async def process_start_command(msg: types.Message):
    await msg.answer("Привет!\nНапиши мне город!")
    await reg_city.city.set()

@dp.message_handler(state=reg_city.city)
async def answer_city(message: types.Message, state: FSMContext):
    answer = message.text
    # await state.update_data(answer1=answer)
    print(answer)
    # user_data = await state.get_data()
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp)
