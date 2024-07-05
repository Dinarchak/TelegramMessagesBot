from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Найти")]
    ],
    resize_keyboard=True
)