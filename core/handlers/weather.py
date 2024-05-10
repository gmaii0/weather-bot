import httpx
from aiogram.types import CallbackQuery, Message
from aiogram import Router, Bot, F
import datetime
from core.keyboards.inline import inline_regions_list_keyboard, inline_answer_menu
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
    "Shimol", "Shimoliy-sharqiy", "Sharqiy", "Shimoliy-sharqiy",
    "Sharq", "Sharqiy-janubiy", "Janubiy-sharqiy", "Janubiy-janubiy-sharqiy",
    "Janubiy", "Janubiy-g'arbiy", "G'arbiy-janubiy", "G'arb",
    "G'arbiy-shimoliy", "Shimoliy-g'arbiy", "Shimoliy-shimoliy-g'arbiy", "Shimol"
]
    index = int((degrees + 11.25) / 22.5)
    return directions[index % 16]


code_to_smile = {
    "Clear": "Ochiq havo \U00002600",
    "Clouds": "Bulutli \U00002601",
    "Rain": "Yomg'ir \U00002614",
    "Drizzle": "Yomg'ir \u00002614",
    "Thunderstorm": "Momaqaldiroq \U000026A1",
    "Snow": "Qor \u0001F328",
    "Mist": "Tuman \U0001F32B"}


# Функция для преобразования timestamp в читаемый формат времени
def convert_timestamp_to_time(timestamp, timezone_offset):
    timezone = pytz.timezone("Asia/Tashkent")  # Укажите часовой пояс
    dt = datetime.datetime.fromtimestamp(timestamp, tz=timezone)
    return dt.strftime("%H:%M")


async def get_weather(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    city = callback_query.data
    api_url = f"{settings.api_url.weather_url}q={city}&appid={settings.api_url.openweather_api_token}&units=metric"
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



@weather_router.message(F.text =="Hududni tanlash")
async def get_menu(message: Message):
    await message.answer(text='Hududni tanlang',reply_markup=inline_regions_list_keyboard)

@weather_router.callback_query(F.data.in_(
    [
        'andijan', 'bukhara', 'jizzakh', 'qarshi',
        'navoi', 'namangan', 'samarkand', 'termez',
        'Sirdaryo', 'Toshkent', "Farg'ona", 'urgench', 'nukus'
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
            f"* Quyosh chiqishi: {convert_timestamp_to_time(sunrise_timestamp, 18000)}\n"
            f"* Quyosh botishi: {convert_timestamp_to_time(sunset_timestamp, 18000)}\n"
            ,
            reply_markup=inline_answer_menu
        )
    else:
        pass
