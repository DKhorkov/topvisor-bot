from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile

from src.help.constants import CommandNames
from src.help.entrypoints.templates import TemplateCreator
from src.logging_system.config import LOG_FILE
from src.users.entrypoints.dependencies import check_if_user_is_admin
from src.users.exceptions import UserHasNoPermissionsError

help_router: Router = Router()


@help_router.message(Command(CommandNames.HELP))
async def help_handler(message: Message) -> None:
    await message.delete()
    await message.answer(text=await TemplateCreator.help_message())


@help_router.message(Command(CommandNames.LOGS))
async def logs_handler(message: Message) -> None:
    """
    Message, which request logs-command should not be deleted for appropriate work of @message.reply_document function.
    """

    if not await check_if_user_is_admin(message=message):
        raise UserHasNoPermissionsError

    logs: FSInputFile = FSInputFile(LOG_FILE)
    await message.reply_document(document=logs)
