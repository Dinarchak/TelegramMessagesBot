from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

filters = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Текст'), KeyboardButton(text='Пользователь')],
        [KeyboardButton(text='Даты'), KeyboardButton(text='Хештеги')],
        [KeyboardButton(text='...')],
        [KeyboardButton(text='Найти сообщения')],
        [KeyboardButton(text='Назад')],
    ],
    resize_keyboard=True
)