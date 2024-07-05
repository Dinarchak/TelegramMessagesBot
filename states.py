from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    enter_chat = State()
    enter_values = State()
    boolean_params = State()
    end = State()

    enter_text = State()
    enter_username = State()
    enter_date = State()
    enter_hashtags = State()

    with_file = State()
    with_link = State()
    with_image = State()







