from aiogram import Router, F
from aiogram import types as atp
from aiogram.fsm.context import FSMContext


find_messages_router = Router(name='find_messages')


@find_messages_router.message(F.text.lower() == 'найти сообщения')
async def find_messages(message: atp.Message, state: FSMContext):
    data = await state.get_data()
    print(data)
    await state.clear()


