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
    await state.set_state(Form.enter_chat)
    await message.answer('В каком чате оно было отправлено?', reply_markup=select_chat_kb)


@dp.message(Form.boolean_params)
async def show_more_filters(message: Message, state: FSMContext):
    message_state_dict = {
        'файл': (Form.with_file, lambda state, value: state.update_data(with_file=value)),
        'изображение': (Form.with_image, lambda state, value: state.update_data(with_image=value)),
        'ссылка': (Form.with_link, lambda state, value: state.update_data(with_link=value))
    }
    filter = message_state_dict.get(message.text.lower(), None)
    if filter:
        filter[1](state=state, value=True)
        message.answer()


@dp.message(Form.enter_chat)
async def set_chat(message: Message, state: FSMContext):
    chat_id = message.chat_shared.chat_id
    chat = await Chat.get_or_none(chat_id=chat_id)
    if chat is None:
        await state.set_state(Form.enter_chat)
        await message.answer('Меня еще не добавили в этот чат', reply_markup=select_chat_kb)
    else:
        await state.update_data(enter_chat=chat_id)
        await state.set_state(Form.enter_values)
        await message.answer('Я есть в этом чате, применить фильтры?', reply_markup=filters_kb)



@dp.message(Form.enter_values)
async def set_params(message: Message, state: FSMContext):
    message_state_dict = {
        'текст': (Form.enter_text, 'Какой текст должено содержать искомое сообщение?', filters_kb),
        'пользователь': (Form.enter_username, 'Кто отправлял это сообщение?', filters_kb),
        'даты': (Form.enter_date, 'В какой промежуток времени оно было отправлено?', filters_kb),
        'хештеги': (Form.enter_hashtags, 'Какие хештеги были прикреплены к сообщению?', filters_kb),
        '...': (Form.boolean_params, 'У сообщения есть дополнительные признаки?', additional_filters)
    }
    next_state = message_state_dict.get(message.text.lower(), None)
    if not next_state:
        await state.set_state(next_state[0])
        await message.answer(next_state[1], reply_markup=next_state[2])
    else:
        await state.set_state(Form.enter_values)
        await message.answer('Нажми на кнопки', reply_markup=filters_kb)


@dp.message(Form.enter_text)
async def enter_text(message: Message, state: FSMContext):
    await state.set_state(Form.enter_values)
    await message.answer('Запомню, у сообщения есть еще какие-то признаки?', reply_markup=filters_kb)


@dp.message(Form.enter_username)
async def enter_username(message: Message, state: FSMContext):
    user = User.get_or_none(username=message.text)
    if not user:
        await state.update_data(enter_username=message.text)
        await message.answer(f'Сообщение было отправлено пользователем{user.first_name} {user.last_name}')
    else:
        await message.answer('У меня нет сохранений от этого пользователя')
    await state.set_state(Form.enter_values)


@dp.message(Form.enter_date)
async def enter_date(message: Message, state: FSMContext):
    pass


@dp.message(Form.enter_hashtags)
async def  enter_hashtags(message: Message, state: FSMContext):
    hashtags = message.text.split(', ', ' ')
    valid_hashtags:tp.List[str]  = []
    for hashtag in hashtags:
        if all(i.isalpha() or i == '_' for i in hashtag) and hashtag[0] == '#':
            valid_hashtags.append(hashtag)

    await state.update_data(enter_hashtags=valid_hashtags)
    await state.set_state(Form.enter_values)
    await message.answer('Хештеги записаны')
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
