from environs import Env
from dataclasses import dataclass


@dataclass
class Bots:
    bot_token: str
    admin_id: str
    openweather_api_token: str


@dataclass
class Settings:
    bots: Bots


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bots=Bots(
            bot_token=env.str("TOKEN"),
            admin_id=env.str("ADMIN_ID"),
            openweather_api_token=env.str("OPENWEATHER_API_TOKEN")
        )
    )


settings = get_settings("input  ")
