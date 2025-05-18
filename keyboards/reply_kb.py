from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

reply_start = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Прогноз погоды')],
    [KeyboardButton(text='Настройки')],
    [KeyboardButton(text='О боте')]
], resize_keyboard=True, one_time_keyboard=True)

menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Меню')]
], resize_keyboard=True)

