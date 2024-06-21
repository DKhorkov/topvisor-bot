from pydantic_settings import BaseSettings


class BotConfig(BaseSettings):
    TOKEN: str


bot_config: BotConfig = BotConfig()
