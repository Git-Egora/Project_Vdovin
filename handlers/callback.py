from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from weather import get_one_forecast, get_five_forecasts

import handlers.commands as cmd

import keyboards.inline_kb as ikb
import keyboards.reply_kb as rkb


call_router = Router()

class Registration(StatesGroup):
    one_day_city = State()
    five_day_city = State()
    everyday_forecasts = State()
    everyweek_forecasts = State()



#Обработка реплаев
@call_router.message(F.text == 'Прогноз погоды')
async def one_day_forecast(message: Message):
    await message.answer('Выберите, какой прогноз хотите получить:', reply_markup=ikb.inline_kb_forecast)

@call_router.message(F.text == 'Настройки')
async def settings(message: Message):
    await message.answer('<b>Настройки:</b>', parse_mode='HTML', reply_markup=ikb.inline_kb_settings)

@call_router.message(F.text == 'О боте')
async def about(message: Message):
    await message.answer('Я бот, которого создали для проекта на тему:\n "Создание прогнозов погоды. Использование мессенджера Telegram для получения информации о погодных условиях".\n\n' \
    'Чтобы посмотреть все команды, воспользуйся /help.', reply_markup=rkb.reply_start)




#Обработка инлаев
@call_router.callback_query(F.data == 'everyday_forecasts')
async def everyday_forecasts(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Registration.everyday_forecasts)
    await callback.message.answer('Напишите время, в которое хотите получать ежедневные прогнозы погоды.\nФормат сообщения: <b>часы:минуты</b>', parse_mode='HTML')

@call_router.message(Registration.everyday_forecasts)
async def waiting_time(message: Message, state: FSMContext):
    time = message.text.strip()
    await message.answer(f'Готово!\nЯ буду отправлять прогноз погоды в <b>{time}</b>', parse_mode='HTML', reply_markup=ikb.inline_kb_change_time)
    await state.clear()
    await rkb.menu




@call_router.callback_query(F.data == 'everyweek_forecasts')
async def everyday_forecasts(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Registration.everyweek_forecasts)
    await callback.message.answer('Напишите день и время, в которое хотите получать ежедневные прогнозы погоды.\nФормат сообщения: <b>день недели часы:минуты</b>', parse_mode='HTML')

@call_router.message(Registration.everyweek_forecasts)
async def waiting_day(message: Message, state: FSMContext):
    date = message.text.strip()
    await message.answer(f'Готово!\nЯ буду отправлять прогноз погоды каждый <b>{date}</b>', parse_mode='HTML', reply_markup=ikb.inline_kb_change_day)
    await state.clear()




@call_router.callback_query(F.data == 'change_time')
async def everyday_forecasts(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Registration.everyday_forecasts)
    await callback.message.answer('Напишите НОВОЕ время, в которое хотите получать ежедневные прогнозы погоды.\nФормат сообщения: <b>часы:минуты</b>', parse_mode='HTML', reply_markup=ikb.inline_kb_cancel)
"""
@call_router.message(Registration.everyday_forecasts)
async def waiting_time(message: Message, state: FSMContext):
    time = message.text.strip()
    await message.answer(f'Готово!\nЯ буду отправлять прогноз погоды в <b>{time}</b>', parse_mode='HTML', reply_markup=ikb.inline_kb_change_time)
    await state.clear()
"""


@call_router.callback_query(F.data == 'change_day')
async def everyday_forecasts(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Registration.everyweek_forecasts)
    await callback.message.answer('Напишите НОВЫЕ день и время, в которое хотите получать ежедневные прогнозы погоды.\nФормат сообщения: <b>день недели часы:минуты</b>', parse_mode='HTML', reply_markup=ikb.inline_kb_cancel)
"""
@call_router.message(Registration.everyweek_forecasts)
async def waiting_day(message: Message, state: FSMContext):
    date = message.text.strip()
    await message.answer(f'Готово!\nЯ буду отправлять прогноз погоды каждый <b>{date}</b>', parse_mode='HTML', reply_markup=ikb.inline_kb_change_day)
    await state.clear()
"""



#прогнозы погоды
@call_router.callback_query(F.data == 'five_days_forecasts')
async def get_city(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Registration.five_day_city)
    await callback.message.answer('Введите город')

@call_router.message(Registration.five_day_city)
async def waiting_city(message: Message, state: FSMContext):
    city = message.text.strip()
    #await state.update_data(city=city)
    await message.answer(f'Получаю прогноз погоды для города {city}...')
    try:
        forecast_message = get_five_forecasts(city)
        await message.answer(forecast_message, parse_mode='HTML', reply_markup=rkb.reply_start)
    except Exception as e:
        await message.answer(f'Ошибка при получении прогноза: {e}.\nПроверьте написание и попробуйте снова.')

    await state.clear()
    
    return waiting_city()

    

@call_router.callback_query(F.data == 'one_day_forecast')
async def get_city(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Registration.one_day_city)
    await callback.message.answer('Введите город')

@call_router.message(Registration.one_day_city)
async def waiting_city1(message: Message, state: FSMContext):
    city = message.text.strip()
    await message.answer(f'Получаю прогноз погоды для города {city}...')
    try:
        forecast_message = get_one_forecast(city)
        await message.answer(forecast_message, parse_mode='HTML', reply_markup=rkb.reply_start)
    except Exception as e:
        await message.answer(f'Ошибка при получении прогноза: {e}.\nПроверьте написание и попробуйте снова.')

    await state.clear()

    return waiting_city1()
    


@call_router.callback_query(F.data == 'goBack')
async def go_back(callback: CallbackQuery):
    await callback.answer('Назад')
    await callback.message.delete()
    await cmd.cmd_menu(callback.message)

@call_router.callback_query(F.data == 'goBack_Changes')
async def cancel(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer('Настройки сохранены.', reply_markup=ikb.inline_kb_settings)

@call_router.callback_query(F.data == 'cancel')
async def cancel(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()




