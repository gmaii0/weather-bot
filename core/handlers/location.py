import httpx
from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ContentType
from core.settings import settings
from core.handlers.weather import get_current_date, convert_timestamp_to_time, code_to_smile, \
    get_wind_direction

loc_router = Router()


async def get_location(latitude: float, longitude: float):
    api_url = f"{settings.api_url.weather_url}lat={latitude}&lon={longitude}&appid={settings.api_url.openweather_api_token}&units=metric"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                return (f"{response.status_code}")
    except Exception as e:
        return (f"Произошла ошибка: {str(e)}")


@loc_router.message(F.content_type == ContentType.LOCATION)
async def process_location(message: Message):
    latitude = message.location.latitude
    longitude = message.location.longitude

    weather_data = await get_location(latitude, longitude)
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
        wind_direction = get_wind_direction(weather_data["wind"]["deg"])
        pressure = weather_data["main"]["pressure"]
        visibility = weather_data["visibility"]
        clouds_percentage = weather_data["clouds"]["all"]
        sunrise_timestamp = weather_data["sys"]["sunrise"]
        sunset_timestamp = weather_data["sys"]["sunset"]
        await message.answer(
            f"**🌆 Shahar nomi: {city_name}:**\n"
            f"**{current_date}:**\n"
            f"* Harorat: {temperature:.1f}°C {wd}\n"
            f"*(His qilinadigan harorat: {feels_like:.1f}°C)\n"
            f"* Namligi: {humidity}%\n"
            f"* Shamol tezligi: {wind_speed:.1f} м/с, 🧭 {wind_direction}\n"
            f"* Bosim: {pressure} гПа\n"
            f"* Ko'rinish: {visibility} м\n"
            f"**Qo'shimcha ma'lumotlar:**\n"
            f"* Bulutli: {clouds_percentage}%\n"
            f"* Quyosh chiqishi: {convert_timestamp_to_time(sunrise_timestamp, 18000)}\n"
            f"* Quyosh botishi: {convert_timestamp_to_time(sunset_timestamp, 18000)}\n"

        )
    else:
        await message.reply("Не удалось получить данные о погоде. Попробуйте еще раз позже.")
