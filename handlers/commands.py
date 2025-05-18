from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from weather import get_one_forecast, get_five_forecasts
from keyboards.reply_kb import reply_start



router = Router()

class Registration(StatesGroup):
    one_day_city = State()
    five_days_city = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'Добро пожаловать, <b>{message.from_user.full_name}</b>.\n Я могу рассказать тебе какая сейчас погода.',parse_mode='HTML', reply_markup=reply_start,)

@router.message(Command('about'))
async def cmd_about(message: Message):
    await message.answer('Я бот. Меня написали для того, чтобы я давал прогнозы погоды для любого города.')

@router.message(Command('help'))
async def cmd_help(message: Message):
    message_text = ('<b>Список команд:</b>\n\n'
    '<b>Основные</b>\n'
    '/menu - перейти в меню\n'
    '/help - список команд\n' 
    '/start - запуск бота\n' 
    '/about - про бота\n\n'
    '<b>Прогнозы погоды</b>\n' 
    '/one_day_forecast - прогноз погоды на сегодня\n'
    '/five_days_forecasts - прогноз погоды на пять дней')
    await message.answer(message_text, parse_mode='HTML')



@router.message(Command('one_day_forecast'))
async def get_city(message: Message, state: FSMContext):
    await state.set_state(Registration.one_day_city)
    await message.answer('Введите город')

@router.message(Registration.one_day_city)
async def waiting_city(message: Message, state: FSMContext):
    city = message.text.strip()
    await message.answer(f'Получаю прогноз погоды для города {city}...')
    try:
        forecast_message = get_one_forecast(city)
        await message.answer(forecast_message, parse_mode='HTML', reply_markup=reply_start)
    except Exception as e:
        await message.answer(f'Ошибка получения прогноза: {e}.\nПроверьте написание и попробуйте снова.')

    await state.clear()

    return



@router.message(Command('five_days_forecasts'))
async def get_city(message: Message, state: FSMContext):
    await state.set_state(Registration.five_days_city)
    await message.answer('Введите город')

@router.message(Registration.five_days_city)
async def waiting_city(message: Message, state: FSMContext):
    city = message.text.strip()
    await message.answer(f'Получаю прогноз погоды для города {city}...')
    try:
        forecast_message = get_five_forecasts(city)
        await message.answer(forecast_message, parse_mode='HTML', reply_markup=reply_start)
    except Exception as e:
        await message.answer(f'Ошибка получения прогноза: {e}.\nПроверьте написание и попробуйте снова.')
    
    await state.clear()

    return



@router.message(F.text == 'Меню')
async def cmd_menu(message: Message):
    await message.answer('Вы перешли в меню.', reply_markup=reply_start)

@router.message(Command('menu'))
async def cmd_menu(message: Message):
    await message.answer('Вы перешли в меню.', reply_markup=reply_start)



@router.message(F.text == 'Спасибо' or 'спасибо')
async def thanks(message: Message):
    await message.answer_photo(photo=FSInputFile(path='pozhalyista.png'), caption='Рад, что помог!')

"""
@router.message(F.text)
async def handle_city(message: Message):
    city = message.text.strip()
    await message.answer(f'Получаю прогноз погоды для города {city}...')
    try:
        forecasts = get_forecast(city)
        daily_forecasts = aggregate_daily_forecast(forecasts)
        forecast_message = f'Прогноз погоды для <b>{city}</b>:\n\n'
        for forecast in daily_forecasts:
            date = datetime.datetime.fromtimestamp(forecast['dt']).strftime('%d.%m.%Y')
            temp_day = forecast['main']['temp']
            pressure = forecast['main']['pressure']
            humidity = forecast['main']['humidity']
            wind = forecast['wind']['speed']
            description = forecast['weather'][0]['description']
            if description in smiles:
                new_description = smiles[description]
            else:
                new_description = 'Посмотри в окно, не пойму, что там'
            
            forecast_message += f'<b>{date}</b>:\nтемпература: {temp_day}°C,\nдавление: {pressure} мм.рт.ст.,\nвлажность: {humidity}%,\nскорость ветра: {wind} м/с.\n{new_description} {description}\n\n'
        await message.answer(forecast_message, parse_mode='HTML')
    except Exception as e:
        await message.answer(f'Ошибка при получении прогноза: {e}')
        """