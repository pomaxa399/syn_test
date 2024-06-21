from aiogram import Bot, html
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from core.utils.statesform import StepsForm


async def get_start(message: Message, state: FSMContext) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Привет, {html.bold(message.from_user.full_name)}, пройди анкетирование! Введи свою фамилию!")
    await state.set_state(StepsForm.get_last_name)

