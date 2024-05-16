from environs import Env
from dataclasses import dataclass


@dataclass
class Bots:
    bot_token: str
    admin_id: int


@dataclass
class ApiUrls:
    openweather_api_token: str
    weather_url: str


@dataclass
class Settings:
    bots: Bots
    api_url: ApiUrls


def get_settings(path: str):
    env = Env()
    env.read_env(path)
    return Settings(
        bots=Bots(
            bot_token=env.str("TOKEN"),
            admin_id=env.int("ADMIN_ID")
        ),
        api_url=ApiUrls(
            openweather_api_token=env.str("OPENWEATHER_API_TOKEN"),
            weather_url=env.str("WEATHER_URL")
        )
    )


settings = get_settings("input")
