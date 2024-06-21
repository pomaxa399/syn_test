from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

select_category = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Психология', callback_data='interest_psychology')
    ],
    [
        InlineKeyboardButton(text='Юриспруденция', callback_data='interest_law')
    ],
    [
        InlineKeyboardButton(text='Другое', callback_data='interest_other')
    ]
])
