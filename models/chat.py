from tortoise.models import Model
from tortoise import fields


class Chat(Model):
    id = fields.IntField(primary_key=True)
    chat_id = fields.IntField(unique=True)