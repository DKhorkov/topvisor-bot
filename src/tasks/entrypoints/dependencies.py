import yaml
from io import BytesIO
from typing import List, BinaryIO, Optional
from aiogram import Bot
from aiogram.types import Message

from src.config import bot_config
from src.tasks.domain.models import TaskModel
from src.tasks.entrypoints.views import TasksViews
from src.tasks.service_layer.service import TasksService
from src.tasks.service_layer.units_of_work import SQLAlchemyTasksUnitOfWork
from src.tasks.entrypoints.schemas import UserTasksStatisticsResponseScheme
from src.tasks.exceptions import TasksFileFormatError
from src.users.domain.models import UserModel
from src.users.entrypoints.dependencies import check_if_user_is_admin, get_all_users
from src.users.exceptions import UserHasNoPermissionsError


async def get_user_tasks_statistics(message: Message) -> List[UserTasksStatisticsResponseScheme]:
    assert message.from_user is not None  # Check for mypy. Also register should work only with private messages

    tasks_views: TasksViews = TasksViews(uow=SQLAlchemyTasksUnitOfWork())
    return await tasks_views.get_user_tasks_statistics(user_id=message.from_user.id)


async def get_actual_tasks() -> List[TaskModel]:
    tasks_service: TasksService = TasksService(uow=SQLAlchemyTasksUnitOfWork())
    return [task for task in await tasks_service.get_all_tasks() if not task.is_archived]


async def update_tasks(message: Message) -> List[TaskModel]:
    if not await check_if_user_is_admin(message=message):
        raise UserHasNoPermissionsError

    assert message.document is not None
    assert message.document.file_name is not None
    if not message.document.file_name.endswith(('.yaml', '.yml')):
        raise TasksFileFormatError

    bot = Bot(token=bot_config.TOKEN)
    raw_file: Optional[BinaryIO] = await bot.download(file=message.document.file_id)
    assert isinstance(raw_file, BytesIO)

    tasks_descriptions: List[str] = yaml.safe_load(raw_file)
    assert isinstance(tasks_descriptions, list)
    for description in tasks_descriptions:
        assert isinstance(description, str)

    tasks: List[TaskModel] = [TaskModel(description=description) for description in tasks_descriptions]
    tasks_service: TasksService = TasksService(uow=SQLAlchemyTasksUnitOfWork())
    await tasks_service.archive_old_tasks(new_tasks=tasks)

    users: List[UserModel] = await get_all_users()
    for task in tasks:
        if not await tasks_service.check_task_existence(description=task.description):
            await tasks_service.create_task(
                task=task,
                users=users
            )
        else:
            task = await tasks_service.get_task_by_description(description=task.description)
            if task.is_archived:
                await tasks_service.reopen_task(id=task.id)

    return await get_actual_tasks()
