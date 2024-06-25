from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from typing import List

from src.tasks.domain.models import TaskModel
from src.tasks.entrypoints.dependencies import get_user_tasks_statistics, update_tasks
from src.tasks.constants import CommandNames
from src.tasks.entrypoints.schemas import UserTasksStatisticsResponseScheme
from src.tasks.entrypoints.templates import TemplateCreator

tasks_router: Router = Router()


@tasks_router.message(Command(CommandNames.USER_TASKS_STATISTICS))
async def user_tasks_statistics_handler(message: Message) -> None:
    await message.delete()
    tasks_statistics: List[UserTasksStatisticsResponseScheme] = await get_user_tasks_statistics(message=message)
    await message.answer(
        text=await TemplateCreator.user_tasks_statistics_message(
            tasks_statistics=tasks_statistics
        )
    )


@tasks_router.message(F.content_type.in_({'document'}))
async def update_tasks_handler(message: Message) -> None:
    await message.delete()
    tasks: List[TaskModel] = await update_tasks(message=message)
    await message.answer(
        text=await TemplateCreator.tasks_updated_message(
            tasks=tasks
        )
    )
