from aiogram.fsm.state import StatesGroup, State


class StepsForm(StatesGroup):
    get_last_name = State()
    get_first_name = State()
    get_middle_name = State()
    get_birthday = State()
    get_phone_number = State()
    get_email = State()
    get_instagram = State()
    get_class_num = State()
    get_parent_name = State()
    get_parent_phone = State()
    get_interest = State()
