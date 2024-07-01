from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


no_insta = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Net_instagram')]
], resize_keyboard=True, one_time_keyboard=True)

num_class = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='01'), KeyboardButton(text='02'), KeyboardButton(text='03'), KeyboardButton(text='04')],
    [KeyboardButton(text='05'), KeyboardButton(text='06'), KeyboardButton(text='07'), KeyboardButton(text='08')],
    [KeyboardButton(text='09'), KeyboardButton(text='10'), KeyboardButton(text='11')]
], resize_keyboard=True, one_time_keyboard=True)
