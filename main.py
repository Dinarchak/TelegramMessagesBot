from aiogram import Bot, Dispatcher
from tortoise import Tortoise
from settings import config
import asyncio

from handlers import (save_message_router,
                      search_router,
                      commands_router
                      )

bot = Bot(token=config['token'])
dp = Dispatcher()

dp.include_routers(search_router, commands_router, save_message_router)


async def main():
    await Tortoise.init(
            db_url=config['db_url'],
            modules={'user': ['models']}
            )

    await Tortoise.generate_schemas()

    # удалить вебхуки и перейти на пулинг и общение с пользователем через getUpdates
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
