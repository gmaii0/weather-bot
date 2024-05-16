import logging
import datetime
import pytz
import httpx
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from core.keyboards.inline import inline_regions_list_keyboard, inline_answer_menu, \
    inline_back_button
from core.settings import settings
import betterlogging as bl

bl.basic_colorized_config(level=logging.INFO)

bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
weather_router = Router()

class WeatherState(StatesGroup):
    location = State()

code_to_smile = {
    "Clear": "Ochiq havo \U00002600",
    "Clouds": "Bulutli \U00002601",
    "Rain": "Yomg'ir \U00002614",
    "Drizzle": "Yomg'ir \u00002614",
    "Thunderstorm": "Momaqaldiroq \U000026A1",
    "Snow": "Qor \u0001F328",
    "Mist": "Tuman \U0001F32B"
}

directions = [
    "Shimol", "Shimoliy-sharqiy", "Sharqiy", "Shimoliy-sharqiy",
    "Sharq", "Sharqiy-janubiy", "Janubiy-sharqiy", "Janubiy-janubiy-sharqiy",
    "Janubiy", "Janubiy-g'arbiy", "G'arbiy-janubiy", "G'arb",
    "G'arbiy-shimoliy", "Shimoliy-g'arbiy", "Shimoliy-shimoliy-g'arbiy", "Shimol"
]

def get_current_date():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M")

def get_wind_direction(degrees):
    index = int((degrees + 11.25) / 22.5)
    return directions[index % 16]

def convert_timestamp_to_time(timestamp, timezone_offset=18000):
    timezone = pytz.timezone("Asia/Tashkent")
    dt = datetime.datetime.fromtimestamp(timestamp, tz=timezone)
    return dt.strftime("%H:%M")

async def get_weather(lat, lon):
    api_url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={settings.api_url.openweather_api_token}&units=metric"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        bl.error(f"HTTP error: {e.response.status_code}")
        return None
    except Exception as e:
        bl.error(f"An error occurred: {str(e)}")
        return None

async def get_air_quality(lat, lon):
    api_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={settings.api_url.openweather_api_token}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        bl.error(f"HTTP error: {e.response.status_code}")
        return None
    except Exception as e:
        bl.error(f"An error occurred: {str(e)}")
        return None

def format_air_quality_report(air_quality_data):
    coord = air_quality_data["coord"]
    pollution_data = air_quality_data["list"][0]
    aqi = pollution_data["main"]["aqi"]

    aqi_level_info = {
        1: ("Yaxshi", "🟢"),
        2: ("Qoniqarli", "🟡"),
        3: ("O'rtacha", "🟠"),
        4: ("Yomon", "🔴"),
        5: ("Juda yomon", "🟣")
    }.get(aqi, ("Noma'lum", "⚫️"))

    components = pollution_data["components"]

    timestamp = datetime.datetime.fromtimestamp(
        pollution_data["dt"], tz=pytz.timezone("Asia/Tashkent")
    )
    formatted_time = timestamp.strftime("%Y-%m-%d %H:%M")

    report = (
        f"🍃 <b>Havo sifati indeksi</b>:\n\n"
        f"📆 <b>Sana va vaqt</b>: <code>{formatted_time} (UZT)</code>\n"
        f"🌍 <b>Joylashuv</b>: <code>{coord['lat']}°N, {coord['lon']}°E</code>\n\n"
        f"{aqi_level_info[1]} <b>AQI</b>: <code>{aqi} ({aqi_level_info[0]})</code>\n\n"  # Use emoji and text from aqi_level
        f"📊 <b>Havoning asosiy ifloslantiruvchi moddalari:</b>\n\n"
    )

    for pollutant, value in components.items():
        pollutant_name = {
            "co": "CO (Uglerod oksidi)",
            "no": "NO (Azot oksidi)",
            "no2": "NO₂ (Azot dioksidi)",
            "o3": "O₃ (Ozon)",
            "so2": "SO₂ (Oltingugurt dioksidi)",
            "pm2_5": "PM2.5 (qattiq zarrachalar)",
            "pm10": "PM10 (qattiq zarrachalar)",
            "nh3": "NH₃ (Ammiak)"
        }.get(pollutant, pollutant.upper())
        report += f"* <b>{pollutant_name}</b>: <code>{value}  μg/m3</code>\n"

    return report

@weather_router.message(F.text == "Hududni tanlash 🇺🇿")
async def get_menu(message: Message):
    await message.answer(text='Hududni tanlang', reply_markup=inline_regions_list_keyboard)

@weather_router.callback_query(F.data == "prev")
async def get_back(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text(text='Hududni tanlang', reply_markup=inline_regions_list_keyboard)

@weather_router.callback_query(F.data.startswith('loc_'))
async def process_weather(callback_query: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    _, lat, lon = callback_query.data.split('_')

    await state.update_data(latitude=lat, longitude=lon)

    weather_data = await get_weather(lat, lon)
    if weather_data:
        current_date = get_current_date()
        city_name = weather_data["city"]["name"]
        weather_description = weather_data["list"][0]["weather"][0]["main"]
        wd = code_to_smile.get(weather_description, "nomalum")
        temperature = weather_data["list"][0]["main"]["temp"]
        feels_like = weather_data["list"][0]["main"]["feels_like"]
        humidity = weather_data["list"][0]["main"]["humidity"]
        wind_speed = weather_data["list"][0]["wind"]["speed"]
        wind_direction = get_wind_direction(weather_data["list"][0]["wind"]["deg"])
        pressure = weather_data["list"][0]["main"]["pressure"]
        visibility = weather_data["list"][0]["visibility"]
        clouds_percentage = weather_data["list"][0]["clouds"]["all"]
        sunrise_timestamp = weather_data["city"]["sunrise"]
        sunset_timestamp = weather_data["city"]["sunset"]
        sunrise_time = convert_timestamp_to_time(sunrise_timestamp)
        sunset_time = convert_timestamp_to_time(sunset_timestamp)

        weather_report = (
            f"🌆 <b>Shahar nomi:</b> {city_name}:\n\n"
            f"🗓 <b>Sana:</b><code>{current_date}</code>\n\n"
            f"🌡️<b>Harorat:</b> <code>{temperature:.1f}°C</code> {wd}\n\n"
            #f"   (His qilinadigan harorat: <code>{feels_like:.1f}°C)</code>\n\n"
            f"💧 <b>Namligi:</b> <code>{humidity}%\n</code>"
            f"💨 <b>Shamol tezligi:</b> <code>{wind_speed:.1f} м/с</code>\n"
            f"🧭 <b>Shamol yo'nalishi:</b> <code>{wind_direction}</code>\n\n"
            ##f"🔵 Bosim: <code>{pressure} гПа</code>\n"
            #f"🌫 Ko'rinish: <code>{visibility} м</code>\n"
            f"☁️ <b>Bulutli:</b> <code>{clouds_percentage}%</code>\n"
            f"🌅 <b>Quyosh chiqishi:</b> <code>{sunrise_time}</code>\n"
            f"🌇 <b>Quyosh botishi:</b> <code>{sunset_time}</code>\n"
        )

        await callback_query.message.edit_text(weather_report, reply_markup=inline_answer_menu)
    else:
        await callback_query.message.reply("Ma'lumotlarni olishda xatolik yuz berdi, qayta urinib ko'ring.")



@weather_router.callback_query(F.data == "index")
async def process_air_quality(callback_query: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)

    data = await state.get_data()
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    if latitude and longitude:
        air_quality_data = await get_air_quality(latitude, longitude)
        if air_quality_data:
            air_quality_report = format_air_quality_report(air_quality_data)
            await callback_query.message.edit_text(air_quality_report, reply_markup=inline_back_button)
        else:
            await callback_query.message.reply("Ma'lumotlarni olishda xatolik yuz berdi, qayta urinib ko'ring.")
    else:
        await callback_query.message.reply("Локация не найдена. Пожалуйста, выберите регион снова.")
