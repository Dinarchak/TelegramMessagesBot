from tortoise.models import Model
from tortoise import fields


class Message(Model):
    id = fields.IntField(primary_key=True)
    chat = fields.ForeignKeyField(model_name='user.Chat', related_name='chat')
    message_id = fields.IntField(unique=True)
    sender = fields.ForeignKeyField('user.User', related_name='messages')
    date = fields.DatetimeField()
    text = fields.TextField()
    has_image = fields.BooleanField(default=False)
    has_document = fields.BooleanField(default=False)
    has_link = fields.BooleanField(default=False)
    hashtags = fields.ManyToManyField(model_name='user.Hashtag', on_delete=fields.OnDelete.NO_ACTION)