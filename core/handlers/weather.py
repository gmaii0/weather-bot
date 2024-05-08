import httpx
from aiogram.types import CallbackQuery
from aiogram import Router, Bot, F
import datetime
from core.keyboards.inline import inline_regions_list_keyboard
from core.settings import settings
import pytz

bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
weather_router = Router()


def get_current_date():
    now = datetime.datetime.now()
    formatted_date = now.strftime("%Y-%m-%d %H:%M")
    return formatted_date


def get_wind_direction(degrees):
    """Возвращает направление ветра по сторонам света на основе угла в градусах."""

    directions = [
        "С (Север)", "ССВ", "СВ", "ВСВ",
        "В (Восток)", "ВЮВ", "ЮВ", "ЮЮВ",
        "Ю (Юг)", "ЮЗ", "ЗЮЗ", "З (Запад)",
        "ЗСЗ", "СЗ", "ССЗ", "С (Север)"
    ]
    index = int((degrees + 11.25) / 22.5)
    return directions[index % 16]


code_to_smile = {
    "Clear": "Ясно \U00002600",
    "Clouds": "Облачно \U00002601",
    "Rain": "Дождь \U00002614",
    "Drizzle": "Дождь \u00002614",
    "Thunderstorm": "Гроза \U000026A1",
    "Snow": "Снег \u0001F328",
    "Mist": "Туман \U0001F32B"}


# Функция для преобразования timestamp в читаемый формат времени
def convert_timestamp_to_time(timestamp, timezone_offset):
    timezone = pytz.timezone("Asia/Tashkent")  # Укажите часовой пояс
    dt = datetime.datetime.fromtimestamp(timestamp, tz=timezone)
    return dt.strftime("%H:%M")


async def get_weather(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    city = callback_query.data
    api_url = f"{settings.api_url.weather_url}{city}&appid={settings.api_url.openweather_api_token}&units=metric"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                await callback_query.message.answer(f"{response.status_code}")
    except Exception as e:
        await  callback_query.message.reply(f"Произошла ошибка: {str(e)}")


@weather_router.callback_query(F.data.in_(
    [
        'andijan', 'bukhara', 'jizzakh', 'qarshi',
        'navoi', 'namangan', 'samarkand', 'termez',
        'gulistan', 'tashkent', 'ferghana', 'urgench', 'nukus'
    ]))
async def process_weather(callback_query: CallbackQuery):
    weather_data = await get_weather(callback_query)
    current_date = get_current_date()
    if weather_data:
        city_name = weather_data["name"]
        weather_description = weather_data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "nomalum"
        temperature = weather_data["main"]["temp"]
        feels_like = weather_data["main"]["feels_like"]
        humidity = weather_data["main"]["humidity"]
        wind_speed = weather_data["wind"]["speed"]
        wind_direction = get_wind_direction(weather_data["wind"]["deg"])  # Функция для определения направления ветра
        pressure = weather_data["main"]["pressure"]
        visibility = weather_data["visibility"]
        clouds_percentage = weather_data["clouds"]["all"]
        sunrise_timestamp = weather_data["sys"]["sunrise"]
        sunset_timestamp = weather_data["sys"]["sunset"]
        await callback_query.message.edit_text(
            f"**🌆 Погода в {city_name}:**\n"
            f"**{current_date}:**\n"
            f"* Температура: {temperature:.1f}°C {wd}\n"
            f"*(ощущается как {feels_like:.1f}°C)\n"
            f"* Влажность: {humidity}%\n"
            f"* Ветер: {wind_speed:.1f} м/с, {wind_direction}\n"
            f"* Давление: {pressure} гПа\n"
            f"* Видимость: {visibility} м\n"
            f"**Дополнительно:**\n"
            f"* Облачность: {clouds_percentage}%\n"
            f"* Восход солнца: {convert_timestamp_to_time(sunrise_timestamp, 18000)}\n"
            f"* Заход солнца: {convert_timestamp_to_time(sunset_timestamp, 18000)}\n"
            ,
            reply_markup=inline_regions_list_keyboard
        )
    else:
        pass
