from aiogram.fsm.state import StatesGroup, State


class StepsForm(StatesGroup):
    get_last_name = State()
    get_first_name = State()
    get_middle_name = State()
    get_phone_number = State()
    get_interest = State()