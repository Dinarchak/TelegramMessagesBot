from aiogram import Dispatcher
from tortoise import Tortoise
from settings import config, bot
import asyncio

from handlers import (save_message_router,
                      search_router,
                      commands_router,
                      find_messages_router
                      )

dp = Dispatcher()

dp.include_routers(search_router, commands_router, save_message_router, find_messages_router)


async def main():
    await Tortoise.init(
            db_url=config['db_url'],
            modules={'user': ['models.chat', 'models.hashtag', 'models.message', 'models.user']}
            )

    await Tortoise.generate_schemas()

    # удалить вебхуки и перейти на пулинг и общение с пользователем через getUpdates
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
