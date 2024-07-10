from aiogram import Router, F
from aiogram import types as atp
from aiogram.fsm.context import FSMContext
from models import Message, Hashtag, User, Chat
from settings import bot
from states import Form

from tortoise.expressions import Q

find_messages_router = Router(name='find_messages')