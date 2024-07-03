from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from settings import config
from aiogram.types import Message

from tortoise import Tortoise
from models import *

from keyboards import start_kb, filters_kb

import asyncio

bot = Bot(token=config['token'])
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Привет долбаеб', reply_markup=start_kb)


@dp.message(F.text.lower() == 'найти')
async def listen_filters(message: Message):
    await message.answer('Укажите фильтры для поиска', reply_markup=filters_kb)



@dp.message()
async def foo(message: Message):
    user = await User.get_or_create(first_name=message.from_user.first_name, last_name=message.from_user.last_name)
    await Message.create(sender=user[0], text=message.text, date=message.date)


async def main():
    await Tortoise.init(
            db_url=config['db_url'],
            modules={'user': ['models']}
            )

    # await Tortoise.generate_schemas()

    # удалить вебхуки и перейти на пулинг и общение с пользователем через getUpdates
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
