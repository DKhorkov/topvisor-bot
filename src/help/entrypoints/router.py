from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.help.constants import CommandNames
from src.help.entrypoints.templates import TemplateCreator

help_router: Router = Router()


@help_router.message(Command(CommandNames.HELP))
async def command_help_handler(message: Message) -> None:
    await message.delete()
    await message.answer(text=await TemplateCreator.help_message())
