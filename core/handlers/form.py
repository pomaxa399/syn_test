import logging
from typing import Dict, Any

from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.keyboards.inline import select_category
from core.utils.statesform import StepsForm

form_router = Router()

user_data: Dict[int, Dict[str, Any]] = {}


@form_router.message(StepsForm.get_last_name)
async def get_first_name(message: Message, state: FSMContext) -> None:
    await message.answer(f'Твоя фамилия: {message.text}, теперь введи имя')
    await state.update_data(last_name=message.text)
    await state.set_state(StepsForm.get_first_name)


@form_router.message(StepsForm.get_first_name)
async def get_middle_name(message: Message, state: FSMContext) -> None:
    await message.answer(f'Твоё имя: {message.text}, теперь введи отчество')
    await state.update_data(first_name=message.text)
    await state.set_state(StepsForm.get_middle_name)


@form_router.message(StepsForm.get_middle_name)
async def get_phone_number(message: Message, state: FSMContext) -> None:
    await message.answer(f'Твоё отчество: {message.text}, теперь напиши свой номер телефона')
    await state.update_data(middle_name=message.text)
    await state.set_state(StepsForm.get_phone_number)


@form_router.message(StepsForm.get_phone_number)
async def get_interest(message: Message, state: FSMContext) -> None:
    await message.answer(f'Твой номер телефона: {message.text}, теперь выбери категорию', reply_markup=select_category)
    await state.update_data(phone_number=message.text)
    await state.set_state(StepsForm.get_interest)


@form_router.callback_query(StepsForm.get_interest, F.data.split('_')[1] != 'other')
async def process_interest(call: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    data = await state.update_data(interest=call.data)
    await call.answer()
    await state.clear()
    await finish_survey(message=call.message, data=data, bot=bot)


@form_router.callback_query(StepsForm.get_interest, F.data.split('_')[1] == 'other')
async def get_other_interest(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.answer("Введите интересующую вас категорию:")
    await state.set_state(StepsForm.get_other_interest)
    await call.answer()


@form_router.message(StepsForm.get_other_interest)
async def set_other_interest(message: Message, state: FSMContext, bot: Bot) -> None:
    data = await state.update_data(interest=message.text)
    await state.clear()
    await finish_survey(message=message, data=data, bot=bot)


async def finish_survey(message: Message, data: Dict[str, Any], bot: Bot) -> None:
    # Собираем данные для текущего пользователя
    current_user_data = {
        'last_name': data.get('last_name'),
        'first_name': data.get('first_name'),
        'middle_name': data.get('middle_name'),
        'phone_number': data.get('phone_number'),
        'interest': data.get('interest'),
        'date': message.date.strftime("%Y-%m-%d")
    }

    # Добавляем данные текущего пользователя в user_data с ключом user_id
    user_data[message.chat.id] = current_user_data

    url = 'https://bogatyr.club/uploads/posts/2023-03/1679683330_bogatyr-club-p-laik-krasnii-foni-vkontakte-17.png'
    # Отправка изображения лайка
    await bot.send_photo(chat_id=message.chat.id, photo=url,
                         caption="Спасибо за участие в опросе!")

    await send_to_system(user_data)


async def send_to_system(data: Dict) -> None:
    # Заглушка для отправки данных в систему
    logging.info(f"Отправка данных в систему: {data}")
