from aiogram import types as atp
from models import User, Message, Hashtag
from aiogram import Router

save_message_router = Router(name='save_messages')


@save_message_router.message()
async def foo(message: atp.Message):

    text_ = '' if message.text is None else message.text
    hashtags_, has_link_ = [], False
    entities = [] if message.entities is None else message.entities
    for entity in entities:
        if entity.type == 'hashtag':
            hashtag = await Hashtag.get_or_create(text=message.text[entity.offset:entity.offset + entity.length])
            hashtags_.append(hashtag)
        else:
            has_link_ = has_link_ or entity.type == 'text_link'

    user = await User.get_or_create(first_name=message.from_user.first_name,
                                    last_name=message.from_user.last_name,
                                    user_id=message.from_user.id,
                                    username=message.from_user.username)
    message_object = await Message.create(sender=user[0],
                                          text=text_,
                                          date=message.date,
                                          has_image=(message.photo is not None),
                                          has_document=(message.document is not None),
                                          has_link=has_link_)

    await message_object.hashtags.add(*hashtags_)

    if message.text:
        await message.answer(message.text)
