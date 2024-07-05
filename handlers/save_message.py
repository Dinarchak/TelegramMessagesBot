from aiogram import types as atp
from models import User, Message
from aiogram import Router

save_message_router = Router(name='save_messages')


@save_message_router.message()
async def foo(message: atp.Message):
    if message.text is not None:
        user = await User.get_or_create(first_name=message.from_user.first_name,
                                        last_name=message.from_user.last_name,
                                        user_id=message.from_user.id,
                                        username=message.from_user.username)
        await Message.create(sender=user[0], text=message.text, date=message.date)
#        await message.answer(message.text)
