import requests
import os
from dotenv import load_dotenv
import datetime


load_dotenv()

WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')



def get_forecast(city: str) -> list:
    forecast_url = (
        f'http://api.openweathermap.org/data/2.5/forecast?'
        f'q={city}&units=metric&appid={WEATHER_API_KEY}'
    )
    response = requests.get(forecast_url)
    data = response.json()
    print('Forecast API response:', data)
    if 'list' in data:
        return data['list']
    else:
        raise Exception('Незнаю такого города')
        #raise Exception(f'Ошибка получения прогноза погоды. Ответ API: {data}')
   
def aggregate_daily_forecast(forecasts: list) -> list:
    daily = {}
    for forecast in forecasts:
        dt_txt = forecast.get('dt_txt')
        if not dt_txt:
            continue
        date_str, time_str = dt_txt.split(" ")
        if date_str not in daily:
            daily[date_str] = forecast
        if time_str == '12:00:00':
            daily[date_str] = forecast
    daily_forecasts = [daily[date] for date in sorted(daily.keys())]
    return daily_forecasts



def get_one_forecast(city):
    forecast_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric'
    response = requests.get(forecast_url)
    data = response.json()
    if response.status_code == 200:
        date = datetime.datetime.now().strftime('%d.%m.%Y')
        temp_day = data['main']['temp']
        pressure = data['main']['pressure']
        new_pressure = round(pressure*100/133.32, 2)
        humidity = data['main']['humidity']
        wind = data['wind']['speed']
        description = data['weather'][0]['description']
        if description in smiles:
            new_description = smiles[description]
        else:
            new_description = 'Посмотри в окно, не пойму, что там'
        forecast_message = (
            f'Прогноз погоды для <b>{city}</b>:\n\n'
            f'<b>Сегодня, {date}</b>:\n🌡 температура: {temp_day}°C,\n〰️ давление: {new_pressure} мм.рт.ст.,\n💧 влажность: {humidity}%,\n💨 скорость ветра: {wind} м/с.\n{new_description}\n'# {description}\n\n'
        )    
        return forecast_message
    elif response.status_code == 404:
        raise Exception('Не знаю такого города')



def get_five_forecasts(city):
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
        
        forecast_message += f'<b>{date}</b>:\n🌡 температура: {temp_day}°C,\n〰️ давление: {pressure} мм.рт.ст.,\n💧 влажность: {humidity}%,\n💨 скорость ветра: {wind} м/с.\n{new_description}\n\n' #{description}\n\n'
    return forecast_message




#словарь иконок под описание погоды
smiles = {
        'thunderstorm with light rain': 'Гроза с небольшим дождём \U000026A1',
	    'thunderstorm with rain': 'Гроза с дождём \U000026A1',
	    'thunderstorm with heavy rain': 'Гроза с сильным дождём\U000026A1',	 
	    'light thunderstorm': 'Небольшая гроза\U000026A1',	 
	    'thunderstorm': 'Гроза \U000026A1',
	    'heavy thunderstorm': 'Сильная гроза \U000026A1',	 
	    'ragged thunderstorm': 'Переменная роза \U000026A1',	
	    'thunderstorm with light drizzle': 'Гроза с моросящим дождём \U000026A1',	 
	    'thunderstorm with drizzle': 'Гроза с легким моросящим дождём\U000026A1',	 
	    'thunderstorm with heavy drizzle': 'Гроза сильным моросящим дождём \U000026A1',

        'light intensity drizzle': 'Лёгкий моросящий дождь \U00002614',
	    'drizzle': 'Дождь \U00002614',	 
	    'heavy intensity drizzle': 'Дождь \U00002614',	 
	    'light intensity drizzle rain': 'Небольшой дождь \U00002614',	
	    'heavy intensity drizzle rain': 'Дождь \U00002614',	 
	    'shower rain and drizzle': 'Дождь \U00002614',	 
	    'heavy shower rain and drizzle': 'Сильный дождь \U00002614', 
	    'shower drizzle': 'Сильный дождь \U00002614',

        'light rain': 'Дождь \U00002614',
	    'moderate rain': 'Дождь \U00002614',	 
	    'heavy intensity rain': 'Дождь \U00002614',	 
	    'very heavy rain': 'Дождь \U00002614',	
	    'extreme rain': 'Дождь \U00002614', 
	    'freezing rain': 'Дождь \U00002614',	
	    'light intensity shower rain': 'Дождь \U00002614',	 
	    'shower rain': 'Дождь \U00002614',	
	    'heavy intensity shower rain': 'Дождь \U00002614',	 
	    'ragged shower rain': 'Дождь \U00002614',	


	    'light snow': 'Небольшой снег \U0001F328',	
	    'snow': 'Снег \U0001F328',	
	    'heavy snow': 'Сильный снег \U0001F328',	 
	    'sleet': 'Слякоть \U0001F328',	
	    'light shower sleet': 'Слякоть \U0001F328',	 
	    'shower sleet': 'Слякоть \U0001F328',	
	    'light rain and snow': 'Дождь со снегом \U0001F328',	 
	    'rain and snow': 'Дождь со снегом \U0001F328',	
	    'light shower snow': 'Снег \U0001F328',	
	    'shower snow': 'Снег \U0001F328',	
	    'heavy shower snow': 'Снег \U0001F328',	 

        'mist': 'Туман \U0001F32B',	 
        'smoke': 'Туман \U0001F32B',	 
        'haze': 'Небольшой туман \U0001F32B',	 
        'sand/dust whirls': 'Песчаные вихри \U0001F32B',	
	    'fog': 'Туман \U0001F32B',	 
	    'sand': 'Песко \U0001F32B',	 
	    'dust': 'Пыль \U0001F32B',	 
	    'volcanic ash': 'Вулканический пепел \U0001F32B',	
        'squalls': 'Шквалистый ветер \U0001F32B',	
	    'tornado': 'Торнадо \U0001F32B',	 

	    'few clouds': 'Облачно \U00002601',	
        'scattered clouds': 'Облачно \U00002601',	
        'broken clouds': 'Переменная облачность \U00002601',	 
        'overcast clouds': 'Большая облачность \U00002601',	

        'clear sky': 'Ясно \U00002600'
    }



