from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    start = State()
    enter_values = State()
    set_bool_params = State()
    end = State()

    enter_text = State()
    enter_username = State()
    enter_date = State()
    enter_hashtags = State()

    boolean_params = State()





