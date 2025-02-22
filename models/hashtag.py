from tortoise.models import Model
from tortoise import fields


class Hashtag(Model):
    id = fields.IntField(primary_key=True)
    text = fields.CharField(max_length=255, unique=True)