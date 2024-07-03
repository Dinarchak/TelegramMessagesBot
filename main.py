from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from settings import config

from aiogram.types import Message
from tortoise import Tortoise, connections

from models import *

import asyncio

bot = Bot(token=config['token'])
dp = Dispatcher()
conn = None

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Привет долбаеб')

@dp.message()
async def foo(message: Message):
    global conn

    await message.answer(f'{message.from_user.first_name} {message.from_user.last_name} {message.text}')
    user = await User.get_or_create(first_name=message.from_user.first_name, last_name=message.from_user.last_name, using_db=conn)
    await Message.create(sender=user[0], text=message.text, date=message.date, using_db=conn)


async def main():
    # удалить вебхуки и перейти на пулинг и общение с пользователем через getUpdates
    global conn

    await Tortoise.init(
            db_url=config['db_url'],
            modules={'user': ['models']}
            )

    conn = connections.get('default')
    print(conn)

    # await Tortoise.generate_schemas()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    print('Бот запущен')

if __name__ == '__main__':
    asyncio.run(main())
