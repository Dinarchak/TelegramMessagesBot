from aiogram import Router, F
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER
from aiogram import types as atp
from aiogram.fsm.context import FSMContext

from models import Chat, User
from states import Form
import keyboards as kb

import typing as tp

search_router = Router(name='search_filters')


@search_router.message(F.text.lower() == 'найти')
async def listen_filters(message: atp.Message, state: FSMContext):
    await state.set_state(Form.enter_chat)
    await message.answer('В каком чате оно было отправлено?', reply_markup=kb.select_chat)


@search_router.message(Form.enter_chat)
async def set_chat(message: atp.Message, state: FSMContext):
    chat_id = message.chat_shared.chat_id
    chat = await Chat.get_or_none(chat_id=chat_id)
    if chat is None:
        await state.set_state(Form.enter_chat)
        await message.answer('Меня еще не добавили в этот чат', reply_markup=kb.select_chat)
    else:
        await state.update_data(enter_chat=chat_id)
        await state.set_state(Form.enter_values)
        await message.answer('Я есть в этом чате, применить фильтры?', reply_markup=kb.filters)


@search_router.my_chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def my_chat_member_handler(chat_member: atp.ChatMemberUpdated):
    await Chat.create(chat_id=chat_member.chat.id)


@search_router.message(Form.enter_values)
async def set_params(message: atp.Message, state: FSMContext):
    message_state_dict = {
        'текст': (Form.enter_text, 'Какой текст должено содержать искомое сообщение?', kb.filters_kb),
        'пользователь': (Form.enter_username, 'Кто отправлял это сообщение?', kb.filters_kb),
        'даты': (Form.enter_date, 'В какой промежуток времени оно было отправлено?', kb.filters_kb),
        'хештеги': (Form.enter_hashtags, 'Какие хештеги были прикреплены к сообщению?', kb.filters_kb),
        '...': (Form.boolean_params, 'У сообщения есть дополнительные признаки?', kb.additional_filters)
    }
    next_state = message_state_dict.get(message.text.lower(), None)
    if not next_state:
        await state.set_state(next_state[0])
        await message.answer(next_state[1], reply_markup=next_state[2])
    else:
        await state.set_state(Form.enter_values)
        await message.answer('Нажми на кнопки', reply_markup=kb.filters)


@search_router.message(Form.enter_username)
async def enter_username(message: atp.Message, state: FSMContext):
    user = User.get_or_none(username=message.text)
    if user:
        await state.update_data(enter_username=message.text)
        await message.answer(f'Сообщение было отправлено пользователем{user.first_name} {user.last_name}')
    else:
        await message.answer('У меня нет сохранений от этого пользователя')
    await state.set_state(Form.enter_values)


@search_router.message(Form.enter_date)
async def enter_date(message: atp.Message, state: FSMContext):
    pass


@search_router.message(Form.enter_hashtags)
async def  enter_hashtags(message: atp.Message, state: FSMContext):
    hashtags = message.text.split(', ', ' ')
    valid_hashtags:tp.List[str]  = []
    for hashtag in hashtags:
        if all(i.isalpha() or i == '_' for i in hashtag) and hashtag[0] == '#':
            valid_hashtags.append(hashtag)

    await state.update_data(enter_hashtags=valid_hashtags)
    await state.set_state(Form.enter_values)
    await message.answer('Хештеги записаны')


@search_router.message(Form.enter_text)
async def enter_text(message: atp.Message, state: FSMContext):
    await state.set_state(Form.enter_values)
    await message.answer('Запомню, у сообщения есть еще какие-то признаки?', reply_markup=kb.filters)


@search_router.message(Form.boolean_params)
async def show_more_filters(message: atp.Message, state: FSMContext):
    message_state_dict = {
        'файл': (Form.with_file, lambda state_, value: state_.update_data(with_file=value)),
        'изображение': (Form.with_image, lambda state_, value: state_.update_data(with_image=value)),
        'ссылка': (Form.with_link, lambda state_, value: state_.update_data(with_link=value))
    }
    filter = message_state_dict.get(message.text.lower(), None)
    if filter:
        filter[1](state_=state, value=True)
        message.answer()