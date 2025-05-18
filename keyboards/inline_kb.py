from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_kb_forecast = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Прогноз на сегодня', callback_data='one_day_forecast')],
    [InlineKeyboardButton(text='Прогноз на 5 дней', callback_data='five_days_forecasts')],
    [InlineKeyboardButton(text='Назад', callback_data='goBack')]
])

inline_kb_settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Ежедневные прогнозы', callback_data='everyday_forecasts')],
    [InlineKeyboardButton(text='Еженедельные прогнозы', callback_data='everyweek_forecasts')],
    [InlineKeyboardButton(text='Назад', callback_data='goBack')]
])

inline_kb_change_time = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Изменить время', callback_data='change_time')],
    [InlineKeyboardButton(text='Назад', callback_data='goBack_Changes')]
])

inline_kb_change_day = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Изменить день', callback_data='change_day')],
    [InlineKeyboardButton(text='Изменить время', callback_data='change_time')],
    [InlineKeyboardButton(text='Назад', callback_data='goBack_Changes')]
])

inline_kb_cancel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отмена', callback_data='cancel')]
])

