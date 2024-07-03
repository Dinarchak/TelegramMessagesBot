from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Найти")]
    ],
    resize_keyboard=True
)

filters_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Текст'), KeyboardButton(text='Пользователь')],
        [KeyboardButton(text='Даты'), KeyboardButton(text='Хештеги')],
        [KeyboardButton(text='Чат'), KeyboardButton(text='...')],
        [KeyboardButton(text='Найти')],
    ],
    resize_keyboard=True
)
