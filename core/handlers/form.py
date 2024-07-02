import logging
from typing import Dict, Any

from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery


from core.keyboards.inline import select_category
from core.keyboards.reply import no_insta, num_class
from core.utils.statesform import StepsForm
from core.utils.validate_birthday import validate_date
from core.utils.validate_email import validate_email
from core.utils.validate_instagram import validate_instagram_username
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
    await message.answer('Хорошо, напиши своё отчество. Если нет отчества - напиши "нет"')
    await state.set_state(StepsForm.get_middle_name)


@form_router.message(F.text.lower() == 'нет', StepsForm.get_middle_name)
async def get_birthday(message: Message, state: FSMContext) -> None:
    await state.update_data(middle_name='')
    await message.answer('Твоя дата рождения в формате: 29.02.1999')
    await state.set_state(StepsForm.get_birthday)


@form_router.message(F.text, StepsForm.get_middle_name)
async def get_birthday(message: Message, state: FSMContext) -> None:
    if not message.text.isalpha():
        await message.answer('Введите отчество корректно')
        return
    await state.update_data(middle_name=message.text.capitalize())
    await message.answer('Твоя дата рождения в формате: 29.02.1999')
    await state.set_state(StepsForm.get_birthday)


@form_router.message(F.text, StepsForm.get_birthday)
async def get_birthday(message: Message, state: FSMContext) -> None:
    valid_date = validate_date(message.text)
    if not valid_date:
        await message.reply('Введи дату рождения по образцу 20.12.2001')
        return
    await state.update_data(birthday=valid_date)
    await message.answer('Теперь напиши свой номер телефона в формате: 79991234567')
    await state.set_state(StepsForm.get_phone_number)


@form_router.message(F.text, StepsForm.get_phone_number)
async def get_phone_number(message: Message, state: FSMContext) -> None:
    valid_phone = validate_phone_number(message.text)
    if not valid_phone:
        await message.reply('Пожалуйста введите правильный номер телефона')
        return
    await state.update_data(phone_number=valid_phone)
    await message.answer('Введи свой email')
    await state.set_state(StepsForm.get_email)


@form_router.message(F.text, StepsForm.get_email)
async def get_email(message: Message, state: FSMContext) -> None:
    valid_email = validate_email(message.text)
    if not valid_email:
        await message.reply('Пожалуйста введите правильный email адрес')
        return
    await state.update_data(email=valid_email)
    await message.answer('Напиши свой инстаграм', reply_markup=no_insta)
    await state.set_state(StepsForm.get_instagram)


@form_router.message(F.text == 'Net_instagram', StepsForm.get_instagram)
async def no_instagram(message: Message, state: FSMContext) -> None:
    await state.update_data(instagram='')
    await message.answer('Какой класс/курс у тебя?', reply_markup=num_class)
    await state.set_state(StepsForm.get_class_num)


@form_router.message(F.text, StepsForm.get_instagram)
async def no_instagram(message: Message, state: FSMContext) -> None:
    valid_inst_username = validate_instagram_username(message.text)
    if not valid_inst_username:
        await message.reply('Введите правильный instagram, либо нажмите кнопку "Net_instagram"', reply_markup=no_insta)
        return
    await state.update_data(instagram=valid_inst_username)
    await message.answer('Какой класс/курс у тебя?', reply_markup=num_class)
    await state.set_state(StepsForm.get_class_num)


@form_router.message(F.text, StepsForm.get_class_num)
async def get_class_num(message: Message, state: FSMContext) -> None:
    await state.update_data(num_class=message.text)
    await message.answer('Напиши имя своего родителя')
    await state.set_state(StepsForm.get_parent_name)


@form_router.message(F.text, StepsForm.get_parent_name)
async def get_parent_name(message: Message, state: FSMContext) -> None:
    if not message.text.isalpha():
        await message.answer('Введите имя корректно')
        return
    await state.update_data(parent_name=message.text.capitalize())
    await message.answer(f'Напиши контактный номер телефона {message.text}')
    await state.set_state(StepsForm.get_parent_phone)


@form_router.message(F.text, StepsForm.get_parent_phone)
async def get_parent_phone(message: Message, state: FSMContext) -> None:
    valid_phone = validate_phone_number(message.text)
    if not valid_phone:
        await message.reply('Пожалуйста введите правильный номер телефона')
        return
    await state.update_data(parent_phone_number=valid_phone)
    await message.answer(f'Выбери интересующие тебя категории', reply_markup=select_category)
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
        'birthday': data.get('birthday'),
        'phone_number': data.get('phone_number'),
        'email': data.get('email'),
        'instagram': data.get('instagram'),
        'num_class': data.get('num_class'),
        'parent_name': data.get('parent_name'),
        'parent_phone_number': data.get('parent_phone_number'),
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
