from aiogram import Router, F
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER
from aiogram import types as atp
from aiogram.fsm.context import FSMContext
from tortoise.expressions import Q

from models import Chat, User, Hashtag, Message
from states import Form
import keyboards as kb

from settings import bot

import time

search_router = Router(name='search_filters')


@search_router.message(F.text.lower() == 'найти')
async def listen_filters(message: atp.Message, state: FSMContext):
    await state.set_state(Form.enter_chat)
    await message.answer('В каком чате оно было отправлено?', reply_markup=kb.select_chat)


@search_router.message(F.text.lower() == 'назад')
async def go_back(message: atp.Message, state: FSMContext):
    cur_state = await state.get_state()
    if cur_state in [
        Form.enter_values,
        Form.enter_username,
        Form.enter_date,
        Form.enter_hashtags,
        Form.enter_text]:
        await state.set_state(Form.enter_chat)
        await message.answer('Выберите чат', reply_markup=kb.select_chat)
    elif cur_state == Form.boolean_params:
        await state.set_state(Form.enter_values)
        await message.answer('Фильтры', reply_markup=kb.filters)


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
        'текст': (Form.enter_text, 'Какой текст должено содержать искомое сообщение?', kb.filters),
        'пользователь': (Form.enter_username, 'Кто отправлял это сообщение?', kb.filters),
        'даты': (Form.enter_date,
                 'В какой промежуток времени оно было отправлено? Введите сообщение в формате от ... до ...' \
                 ', а вместо троиточий укажите желаемое время с точностью до часа',
                 kb.filters),
        'хештеги': (Form.enter_hashtags, 'Какие хештеги были прикреплены к сообщению?', kb.filters),
        '...': (Form.boolean_params, 'У сообщения есть дополнительные признаки?', kb.additional_filters),
    }

    if message.text.lower() == 'найти сообщения':
        await find_messages(message, state)
        return

    next_state = message_state_dict.get(message.text.lower(), None)
    if next_state:
        await state.set_state(next_state[0])
        await message.answer(next_state[1], reply_markup=next_state[2])
    else:
        await state.set_state(Form.enter_values)
        await message.answer('Нажми на кнопки', reply_markup=kb.filters)


@search_router.message(Form.enter_username)
async def enter_username(message: atp.Message, state: FSMContext):
    username = None
    for entity in message.entities:
        if entity.type == 'mention':
            username = message.text[entity.offset + 1:entity.offset + entity.length]
            break
    print(username)
    user = await User.get_or_none(username=username)
    if user:
        await state.update_data(enter_username=username)
        await message.answer(f'Сообщение было отправлено пользователем {user.first_name} {user.last_name}',
                             reply_markup=kb.filters)
    else:
        await message.answer('У меня нет сохранений от этого пользователя', reply_markup=kb.filters)
    await state.set_state(Form.enter_values)


@search_router.message(Form.enter_date)
async def enter_date(message: atp.Message, state: FSMContext):
    text = message.text.replace(' ', '')
    a, b = text.find('от'), text.find('до')
    if b == -1:
        b = len(text)

    time1, time2 = text[a + 3: b], text[b + 3:]
    time_after = time_before = None
    print(time1, time2, len(time1), len(time2))
    try:
        if len(time1) > 0:
            time_after = time.strptime(time1, '%d.%m.%Y')
        if len(time2) > 0:
            time_before = time.strptime(time2, '%d.%m.%Y')
    except:
        await message.answer('Неверный формат сообщения')
        await state.set_state(Form.enter_date)
        return

    await state.update_data(enter_date=(time_after, time_before))
    await message.answer('Временные рамки установлены', reply_markup=kb.filters)
    await state.set_state(Form.enter_values)


@search_router.message(Form.enter_hashtags)
async def enter_hashtags(message: atp.Message, state: FSMContext):
    hashtags = message.text.replace(' ', '').split('#')

    await state.update_data(enter_hashtags=hashtags[1:])
    await state.set_state(Form.enter_values)
    await message.answer('Хештеги записаны', reply_markup=kb.filters)


@search_router.message(Form.enter_text)
async def enter_text(message: atp.Message, state: FSMContext):
    await state.set_state(Form.enter_values)
    await state.update_data(enter_text=message.text)
    await message.answer('Запомню, у сообщения есть еще какие-то признаки?', reply_markup=kb.filters)


@search_router.message(Form.boolean_params)
async def show_more_filters(message: atp.Message, state: FSMContext):
    message_state_dict = {
        'файл': (Form.with_file,
                 lambda state_, value: state_.update_data(with_file=value),
                 'К сообщению прикреплен файл'),
        'изображение': (Form.with_image,
                        lambda state_, value: state_.update_data(with_image=value),
                        'К сообщение прикреплено изображение'),
        'ссылка': (Form.with_link,
                   lambda state_, value: state_.update_data(with_link=value),
                   'В сообщении есть ссылка'),
    }

    bool_filter = message_state_dict.get(message.text.lower(), None)
    if bool_filter:
        await bool_filter[1](state_=state, value=True)
        await message.answer(bool_filter[2], reply_markup=kb.additional_filters)


async def find_messages(message: atp.Message, state: FSMContext):
    """
    data = {
        enter_chat: int,
        username: str(ник пользователя),
        enter_date: (Datetime, Datetime),
        enter_hashtags: [string],
        enter_text: str,
        with_file: bool,
        with_image: bool,
        with_link: bool
    }
    """

    params = {}

    data = await state.get_data()
    await state.clear()

    if 'enter_username' in data:
        params['sender'] = await User.get(username=data['enter_username'])

    if 'enter_chat' in data:
        params['chat'] = await Chat.get(chat_id=data['enter_chat'])

    if 'enter_date' in data:
        date = data['enter_date']
        if date[0]:
            params['date__gt'] = date[0]
        if date[1]:
            params['date__lt'] = date[1]

    for db_key, data_key in zip(['text__contains', 'has_image', 'has_link', 'has_document'], ['enter_text', 'with_image', 'with_link', 'with_file']):
        if data_key in data:
            params[db_key] = data[data_key]

    messages = []

    if 'enter_hashtags' in data:
        hashtags = await Hashtag.filter(text__in=data['enter_hashtags'])

        for tag in hashtags:
            messages += await tag.messages.filter(**params)
        messages = set(messages)
    else:
        messages = await Message.filter(**params)

    message_ids = []
    for i in messages:
        if not len(message_ids) or not len(message_ids[-1]) % 100:
            message_ids.append([])
        message_ids[-1].append(i.message_id)

    for i in message_ids:
        await bot.forward_messages(chat_id=message.chat.id,
                                   from_chat_id=data['enter_chat'],
                                   message_ids=i)
    await message.answer("Вот все сообщения, подошедшие под фильтры", reply_markup=kb.start)

