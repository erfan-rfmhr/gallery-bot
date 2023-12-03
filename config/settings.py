from pydantic_settings import BaseSettings, SettingsConfigDict


class BotSettings(BaseSettings):
    model_config = SettingsConfigDict(str_strip_whitespace=True, env_file="config/.env")
    TOKEN: str


settings = BotSettings()
