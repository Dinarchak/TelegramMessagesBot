from aiogram.filters import CommandStart
from aiogram import types as atp, Router
import keyboards as kb

commands_router = Router(name='commands')


@commands_router.message(CommandStart())
async def start(message: atp.Message):
    await message.answer('Привет долбаеб', reply_markup=kb.start)