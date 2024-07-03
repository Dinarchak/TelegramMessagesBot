from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,  KeyboardButtonRequestChat

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Найти")]
    ],
    resize_keyboard=True
)

select_chat_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Выберите группу',
                           request_chat=KeyboardButtonRequestChat(request_id=1,
                                                                  chat_is_channel=False,
                                                                  chat_is_forum=False)
                           )
        ]
    ],
    resize_keyboard=True
)

filters_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Текст'), KeyboardButton(text='Пользователь')],
        [KeyboardButton(text='Даты'), KeyboardButton(text='Хештеги')],
        [KeyboardButton(text='...')],
        [KeyboardButton(text='Найти')],
        [KeyboardButton(text='Назад')],
    ],
    resize_keyboard=True
)

additional_filters = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Изображение'), KeyboardButton(text='Файл'), KeyboardButton(text='Ссылка')],
            [KeyboardButton(text='Найти')],
        [KeyboardButton(text='Назад')],
    ],
    resize_keyboard=True
)
