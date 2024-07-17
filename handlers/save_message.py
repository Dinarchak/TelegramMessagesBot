from aiogram import types as atp
from models import User, Message, Hashtag, Chat
from aiogram import Router, F

save_message_router = Router(name='save_messages')


@save_message_router.message((F.chat.type == 'supergroup') | (F.chat.type == 'group'))
async def foo(message: atp.Message):

    text_ = '' if message.text is None else message.text
    hashtags_, has_link_ = [], False
    entities = []
    if message.entities:
        entities = message.entities
    elif message.caption_entities:
        entities = message.caption_entities
    
    for entity in entities:
        if entity.type == 'hashtag':
            hashtag, _ = await Hashtag.get_or_create(text=message.text[entity.offset + 1:entity.offset + entity.length])
            hashtags_.append(hashtag)
        else:
            has_link_ = has_link_ or entity.type in ['text_link', 'url']

    user = await User.get_or_create(first_name=message.from_user.first_name,
                                    last_name=message.from_user.last_name,
                                    user_id=message.from_user.id,
                                    username=message.from_user.username)
    message_object = await Message.create(sender=user[0],
                                          text=text_,
                                          chat=await Chat.get(chat_id=message.chat.id),
                                          date=message.date,
                                          has_image=(message.photo is not None),
                                          has_document=(message.document is not None),
                                          has_link=has_link_,
                                          message_id=message.message_id)

    await message_object.hashtags.add(*hashtags_)

    if message.text:
        await message.answer(message.text)
