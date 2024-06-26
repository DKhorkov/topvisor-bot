import asyncio
import logging
from aiogram import Bot

from src.app import dispatcher
from src.bot import TopvisorBot
from src.lifespan import on_startup, on_shutdown
from src.logging_system.config import LOGGING_CONFIG


async def launch_bot(bot: Bot) -> None:
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    try:
        logging.basicConfig(**LOGGING_CONFIG)
        on_startup()
        asyncio.run(launch_bot(bot=TopvisorBot))
    except Exception as e:
        logging.exception(e)
    finally:
        on_shutdown()
