import logging
from typing import Dict, Any

from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery


from core.keyboards.inline import select_category
from core.utils.statesform import StepsForm
from core.utils.validate_phone import validate_phone_number

form_router = Router()

user_data: Dict[int, Dict[str, Any]] = {}


@form_router.message(F.text, StepsForm.get_last_name)
async def get_first_name(message: Message, state: FSMContext) -> None:
    if not message.text.isalpha():
        await message.answer('Введите фамилию корректно')
        return
    await state.update_data(last_name=message.text.capitalize(), user_id=message.from_user.id)
    await message.answer('Отлично, теперь введи имя')
    await state.set_state(StepsForm.get_first_name)


@form_router.message(F.text, StepsForm.get_first_name)
async def get_middle_name(message: Message, state: FSMContext) -> None:
    if not message.text.isalpha():
        await message.answer('Введите имя корректно')
        return
    await state.update_data(first_name=message.text.capitalize())
    await message.answer('Хорошо, напиши своё отчество')
    await state.set_state(StepsForm.get_middle_name)


@form_router.message(F.text, StepsForm.get_middle_name)
async def get_phone_number(message: Message, state: FSMContext) -> None:
    if not message.text.isalpha():
        await message.answer('Введите отчество корректно')
        return
    await message.answer('Теперь напиши свой номер телефона в формате: 79991234567')
    await state.update_data(middle_name=message.text.capitalize())
    await state.set_state(StepsForm.get_phone_number)


@form_router.message(F.text, StepsForm.get_phone_number)
async def get_interest(message: Message, state: FSMContext) -> None:
    valid_phone = validate_phone_number(message.text)
    if not valid_phone:
        await message.reply('Пожалуйста введите правильный номер телефона')
        return
    await state.update_data(phone_number=valid_phone)
    await message.answer(f'Выбери интересующую тебя категорию', reply_markup=select_category)
    await state.set_state(StepsForm.get_interest)


@form_router.callback_query(F.data, StepsForm.get_interest)
async def process_interest(call: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    if call.data.split('_')[1] != 'other':
        data = await state.update_data(interest=call.data)
        await call.answer()
        await state.clear()
        await finish_survey(message=call.message, data=data, bot=bot)
    await call.answer()
    await call.message.answer('Введите интересующую вас категорию')
    await state.set_state(StepsForm.get_interest)


@form_router.message(F.text, StepsForm.get_interest)
async def set_other_interest(message: Message, state: FSMContext, bot: Bot) -> None:
    data = await state.update_data(interest=message.text)
    await state.clear()
    await finish_survey(message=message, data=data, bot=bot)


async def finish_survey(message: Message, data: Dict[str, Any], bot: Bot) -> None:
    user_id = data.get('user_id')
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
    user_data[user_id] = current_user_data

    url = 'https://bogatyr.club/uploads/posts/2023-03/1679683330_bogatyr-club-p-laik-krasnii-foni-vkontakte-17.png'
    # Отправка изображения лайка
    await bot.send_photo(chat_id=message.chat.id, photo=url,
                         caption="Спасибо за участие в опросе!")

    await send_to_system(user_data[user_id])


async def send_to_system(data: Dict) -> None:
    # Заглушка для отправки данных в систему
    logging.info(f"Отправка данных в систему: {data}")
