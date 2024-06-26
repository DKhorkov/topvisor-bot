from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.methods import GetUpdates, GetMe

from src.config import bot_config
from src.middlewares import RequestLoggingMiddleware

# Initialize Bot instance with default bot properties which will be passed to all API calls
TopvisorBot: Bot = Bot(token=bot_config.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
TopvisorBot.session.middleware(RequestLoggingMiddleware(ignore_methods=[GetUpdates, GetMe]))
