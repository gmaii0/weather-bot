import httpx
from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ContentType
from core.settings import settings

loc_router = Router()

# Функция для получения данных о погоде по широте и долготе
async def get_location(latitude: float, longitude: float):
    api_url = f"{settings.api_url.weather_url}lat={latitude}&lon={longitude}&appid={settings.api_url.openweather_api_token}&units=metric"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Ошибка получения данных: {response.status_code}")
                return None
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        return None

# Обработчик сообщения с локацией
@loc_router.message(F.content_type == ContentType.LOCATION)
async def process_location(message: Message):
    latitude = message.location.latitude
    longitude = message.location.longitude
    weather_data = await get_location(latitude, longitude)

    if weather_data:
        # Извлечение данных о погоде из ответа API
        city_name = weather_data.get("name", "Неизвестно")
        weather_description = weather_data["weather"][0]["main"]
        temperature = weather_data["main"]["temp"]
        feels_like = weather_data["main"]["feels_like"]
        humidity = weather_data["main"]["humidity"]
        wind_speed = weather_data["wind"]["speed"]
        pressure = weather_data["main"]["pressure"]
        visibility = weather_data.get("visibility", "Неизвестно")
        clouds_percentage = weather_data["clouds"]["all"]

        # Отправка сообщения с данными о погоде
        await message.answer(
            f"**🌆 Погода в {city_name}:**\n"
            f"* Температура: {temperature:.1f}°C\n"
            f"*(ощущается как {feels_like:.1f}°C)\n"
            f"* Влажность: {humidity}%\n"
            f"* Давление: {pressure} гПа\n"
            f"* Видимость: {visibility} м\n"
            f"**Дополнительно:**\n"
            f"* Облачность: {clouds_percentage}%\n"
        )
    else:
        await message.reply("Не удалось получить данные о погоде. Попробуйте еще раз позже.")
