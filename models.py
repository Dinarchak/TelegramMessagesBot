from tortoise.models import Model
from tortoise import fields

class Message(Model):
    id = fields.IntField(primary_key=True)
    sender = fields.ForeignKeyField('user.User', related_name='messages')
    date = fields.DatetimeField()
    text = fields.TextField()


class User(Model):
    id = fields.IntField(primary_key=True)
    first_name = fields.CharField(max_length=255)
    last_name = fields.CharField(max_length=255)
