from aiogram import Bot, Dispatcher, F
from aiogram.filters import (CommandStart,
                             ChatMemberUpdatedFilter,
                             IS_NOT_MEMBER,
                             IS_MEMBER)
from aiogram.types import Message, ChatMemberUpdated
from aiogram.fsm.context import FSMContext

from tortoise import Tortoise
from models import *

from settings import config
from keyboards import start_kb, filters_kb, additional_filters, select_chat_kb
from states import Form

import asyncio

bot = Bot(token=config['token'])
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Привет долбаеб', reply_markup=start_kb)


@dp.message(F.text.lower() == 'найти')
async def listen_filters(message: Message, state: FSMContext):
    await state.set_state(Form.start)
    await message.answer('В каком чате оно было отправлено?', reply_markup=select_chat_kb)


@dp.message(F.text == '...')
async def show_more_filters(message: Message):
    await message.answer('Дополнительные фильтры', reply_markup=additional_filters)


@dp.message(Form.start)
async def set_chat(message: Message, state: FSMContext):
    chat_id = message.chat_shared
    # найти чат в базе данных, если его нет, то отказать в поиске


@dp.message(Form.enter_values)
async def set_params(message: Message, state: FSMContext):
    message_state_dict = {
        'текст': (Form.enter_text, 'Какой текст должено содержать искомое сообщение?'),
        'пользователь': (Form.enter_username, 'Кто отправлял это сообщение?'),
        'даты': (Form.enter_date, 'В какой промежуток времени оно было отправлено?'),
        'хештеги': (Form.enter_hashtags, 'Какие хештеги были прикреплены к сообщению')
    }
    next_state = message_state_dict.get(message.text, None)
    if not next_state:
        await state.set_state(next_state[0])
        await message.answer(next_state[1], reply_markup=filters_kb)
    else:
        await state.set_state(Form.enter_values)
        await message.answer('Нажми на кнопки', reply_markup=filters_kb)


@dp.message(Form.enter_text)
async def enter_text(message: Message, state: FSMContext):
    await state.set_state(Form.enter_values)
    await message.answer('Запомню, у сообщения есть еще какие-то признаки?', reply_markup=filters_kb)


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
