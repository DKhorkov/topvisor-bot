import asyncio
import logging
import sys
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.app import dispatcher
from src.config import bot_config
from src.lifespan import on_startup, on_shutdown


async def launch_bot() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot: Bot = Bot(token=bot_config.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        on_startup()
        asyncio.run(launch_bot())
    except Exception as e:
        logging.exception(e)
    finally:
        on_shutdown()
