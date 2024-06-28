import yaml
from io import BytesIO
from typing import List, BinaryIO, Optional, Dict
from aiogram import Bot
from aiogram.types import Message

from src.core.utils import get_substring_after_chars
from src.tasks.constants import ConfirmTaskCompletenessData
from src.tasks.domain.models import TaskModel, TaskAssociationModel
from src.tasks.entrypoints.markups import MarkupCreator
from src.tasks.entrypoints.templates import TemplateCreator
from src.tasks.entrypoints.views import TasksViews
from src.tasks.service_layer.service import TasksService
from src.tasks.service_layer.units_of_work import SQLAlchemyTasksUnitOfWork
from src.tasks.entrypoints.schemas import UserTaskStatisticsResponseScheme, UserActiveTaskScheme
from src.tasks.exceptions import TasksFileFormatError
from src.users.constants import AdminsIds
from src.users.domain.models import UserModel
from src.users.entrypoints.dependencies import check_if_user_is_admin, get_all_users, get_user_by_id
from src.users.exceptions import UserHasNoPermissionsError


async def get_user_tasks_statistics(message: Message) -> List[UserTaskStatisticsResponseScheme]:
    assert message.from_user is not None  # Check for mypy. Also register should work only with private messages

    tasks_views: TasksViews = TasksViews(uow=SQLAlchemyTasksUnitOfWork())
    return await tasks_views.get_user_tasks_statistics(user_id=message.from_user.id)


async def get_actual_tasks() -> List[TaskModel]:
    tasks_service: TasksService = TasksService(uow=SQLAlchemyTasksUnitOfWork())
    return [task for task in await tasks_service.get_all_tasks() if not task.is_archived]


async def update_tasks(message: Message, bot: Bot) -> List[TaskModel]:
    if not await check_if_user_is_admin(message=message):
        raise UserHasNoPermissionsError

    assert message.document is not None
    assert message.document.file_name is not None
    if not message.document.file_name.endswith(('.yaml', '.yml')):
        raise TasksFileFormatError

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


async def get_user_active_tasks(message: Message) -> List[UserActiveTaskScheme]:
    assert message.from_user is not None

    tasks_service: TasksService = TasksService(uow=SQLAlchemyTasksUnitOfWork())
    user_task_associations: List[TaskAssociationModel] = [
        task_association for task_association in await tasks_service.get_user_tasks_associations(
            user_id=message.from_user.id
        ) if not task_association.task_archived
    ]

    tasks_storage: Dict[int, TaskModel] = {task.id: task for task in await tasks_service.get_all_tasks()}
    return [
        UserActiveTaskScheme(
            description=tasks_storage[task_association.task_id].description,
            task_association_id=task_association.id
        ) for task_association in user_task_associations
    ]


async def get_task_by_association_id(task_association_id: int) -> TaskModel:
    tasks_service: TasksService = TasksService(uow=SQLAlchemyTasksUnitOfWork())
    return await tasks_service.get_task_by_association_id(task_association_id=task_association_id)


async def get_user_by_association_id(task_association_id: int) -> UserModel:
    tasks_service: TasksService = TasksService(uow=SQLAlchemyTasksUnitOfWork())
    task_association: TaskAssociationModel = await tasks_service.get_task_association_by_id(
        task_association_id=task_association_id
    )

    return await get_user_by_id(id=task_association.user_id)


async def send_task_on_confirmation(message: Message, bot: Bot) -> TaskModel:
    assert message.reply_to_message is not None
    assert message.reply_to_message.text is not None
    task_association_id: int = int(
        await get_substring_after_chars(
            string=message.reply_to_message.text,
            chars=ConfirmTaskCompletenessData.TASK_ASSOCIATION_ID_TEXT
        )
    )

    assert message.photo is not None
    task: TaskModel = await get_task_by_association_id(task_association_id=task_association_id)

    assert message.from_user is not None
    user: UserModel = await get_user_by_id(id=message.from_user.id)

    for admin_id in AdminsIds().tuple():
        await bot.send_photo(
            chat_id=admin_id,
            photo=message.photo[-1].file_id,  # the most quality photo
            reply_markup=await MarkupCreator.confirm_task_completeness_markup(task_association_id=task_association_id),
            caption=await TemplateCreator.to_admin_task_confirmation_message(
                task=task,
                user=user
            )
        )

    return task


async def set_task_competed_for_user(task_association_id: int) -> None:
    tasks_service: TasksService = TasksService(uow=SQLAlchemyTasksUnitOfWork())
    await tasks_service.set_task_association_completed_status(task_association_id=task_association_id)
