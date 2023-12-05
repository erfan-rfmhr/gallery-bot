from collections import namedtuple

from pydantic_settings import BaseSettings, SettingsConfigDict


class BotSettings(BaseSettings):
    model_config = SettingsConfigDict(str_strip_whitespace=True, env_file="config/.env")
    TELEGRAM_TOKEN: str
    TELEGRAM_CHANNEL_ID: str
    INSTAGRAM_USERNAME: str
    INSTAGRAM_PASSWORD: str
    FACEBOOK_URL: str
    FACEBOOK_TOKEN: str


state_names = ('START', 'SEND_NEW_LINK', 'LINKS_IN_QUEUE', 'SEND_NOW', 'SEND_NEWS', 'SET_PUBLIC_HASHTAGS', 'SCHEDULE',)

STATES = namedtuple('states', state_names)(*range(len(state_names)))

settings = BotSettings()
