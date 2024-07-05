from tortoise.models import Model
from tortoise import fields

class Message(Model):
    id = fields.IntField(primary_key=True)
    sender = fields.ForeignKeyField('user.User', related_name='messages')
    date = fields.DatetimeField()
    text = fields.TextField()


class User(Model):
    id = fields.IntField(primary_key=True)
    user_id = fields.IntField(unique=True)
    first_name = fields.CharField(max_length=255)
    last_name = fields.CharField(max_length=255)
    username = fields.CharField(max_length=255)


class Chat(Model):
    id = fields.IntField(primary_key=True)
    chat_id = fields.IntField(unique=True)
