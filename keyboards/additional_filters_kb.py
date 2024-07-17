from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

additional_filters = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Изображение'), KeyboardButton(text='Файл'), KeyboardButton(text='Ссылка')],
            [KeyboardButton(text='Найти сообщения')],
        [KeyboardButton(text='Назад')],
    ],
    resize_keyboard=True
)
