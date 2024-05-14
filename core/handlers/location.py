import httpx
from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ContentType
from core.settings import settings
from core.handlers.weather import get_current_date, convert_timestamp_to_time, code_to_smile, get_wind_direction

loc_router = Router()

async def fetch_weather_data(api_url: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        return f"HTTP error: {e.response.status_code}"
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"

async def get_location_weather(latitude: float, longitude: float):
    api_url = f"{settings.api_url.weather_url}lat={latitude}&lon={longitude}&appid={settings.api_url.openweather_api_token}&units=metric"
    return await fetch_weather_data(api_url)

def format_weather_report(weather_data, current_date):
    city_name = weather_data["name"]
    weather_description = weather_data["weather"][0]["main"]
    wd = code_to_smile.get(weather_description, "nomalum")
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
    sunrise_time = convert_timestamp_to_time(sunrise_timestamp)
    sunset_time = convert_timestamp_to_time(sunset_timestamp)

    return (
        f"**🌆 Shahar nomi: {city_name}:**\n"
        f"**{current_date}:**\n"
        f"* Harorat: {temperature:.1f}°C {wd}\n"
        f"*(His qilinadigan harorat: {feels_like:.1f}°C)\n"
        f"* Namligi: {humidity}%\n"
        f"* Shamol tezligi: {wind_speed:.1f} м/с\n"
        f"* Shamol yo'nalishi: 🧭 {wind_direction}\n"
        f"* Bosim: {pressure} гПа\n"
        f"* Ko'rinish: {visibility} м\n"
        f"**Qo'shimcha ma'lumotlar:**\n"
        f"* Bulutli: {clouds_percentage}%\n"
        f"* Quyosh chiqishi: {sunrise_time}\n"
        f"* Quyosh botishi: {sunset_time}\n"
    )

@loc_router.message(F.content_type == ContentType.LOCATION)
async def process_location(message: Message):
    latitude = message.location.latitude
    longitude = message.location.longitude

    weather_data = await get_location_weather(latitude, longitude)
    current_date = get_current_date()

    if isinstance(weather_data, dict):
        weather_report = format_weather_report(weather_data, current_date)
        await message.answer(weather_report)
    else:
        await message.reply(weather_data or "Ma'lumotlarni olishda xatolik yuz berdi, qayta urinib ko'ring.")
