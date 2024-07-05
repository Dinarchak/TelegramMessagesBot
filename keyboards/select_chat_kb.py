from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    KeyboardButtonRequestChat)


select_chat = ReplyKeyboardMarkup(
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