import httpx
from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext

from core.keyboards.inline import inline_answer_menu
from core.keyboards.menu import start_menu
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
        f"🌆 <b>Shahar nomi:</b> {city_name}:\n\n"
        f"🗓 <b>Sana:</b><code>{current_date}</code>\n\n"
        f"🌡️<b>Harorat:</b> <code>{temperature:.1f}°C</code> {wd}\n\n"
        # f"   (His qilinadigan harorat: <code>{feels_like:.1f}°C)</code>\n\n"
        f"💧 <b>Namligi:</b> <code>{humidity}%\n</code>"
        f"💨 <b>Shamol tezligi:</b> <code>{wind_speed:.1f} м/с</code>\n"
        f"🧭 <b>Shamol yo'nalishi:</b> <code>{wind_direction}</code>\n\n"
        ##f"🔵 Bosim: <code>{pressure} гПа</code>\n"
        # f"🌫 Ko'rinish: <code>{visibility} м</code>\n"
        f"☁️ <b>Bulutli:</b> <code>{clouds_percentage}%</code>\n"
        f"🌅 <b>Quyosh chiqishi:</b> <code>{sunrise_time}</code>\n"
        f"🌇 <b>Quyosh botishi:</b> <code>{sunset_time}</code>\n"
    )


@loc_router.message(F.content_type == ContentType.LOCATION)
async def process_location(message: Message, state: FSMContext):
    latitude = message.location.latitude
    longitude = message.location.longitude

    await state.update_data(latitude=latitude, longitude=longitude)

    weather_data = await get_location_weather(latitude, longitude)
    current_date = get_current_date()

    if isinstance(weather_data, dict):
        weather_report = format_weather_report(weather_data, current_date)
        await message.answer(weather_report, reply_markup=inline_answer_menu)
    else:
        await message.reply(weather_data or "Ma'lumotlarni olishda xatolik yuz berdi, qayta urinib ko'ring.")
