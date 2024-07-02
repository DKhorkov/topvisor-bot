import yaml
from io import BytesIO
from typing import List, Optional, BinaryIO
from aiogram import Bot
from aiogram.types import Message

from src.tasks.constants import UPDATE_TASKS_DOCUMENT_APPROPRIATE_EXTENSIONS
from src.tasks.domain.models import TaskModel
from src.tasks.entrypoints.markups import MarkupCreator
from src.tasks.entrypoints.templates import TemplateCreator
from src.tasks.exceptions import TasksFileFormatError
from src.users.constants import AdminsIds
from src.users.domain.models import UserModel
from src.users.entrypoints.dependencies import check_if_user_is_admin, get_user_by_id
from src.users.exceptions import UserHasNoPermissionsError


async def get_new_tasks_from_message(message: Message, bot: Bot) -> List[TaskModel]:
    if not await check_if_user_is_admin(message=message):
        raise UserHasNoPermissionsError

    assert message.document is not None
    assert message.document.file_name is not None
    if not message.document.file_name.endswith(UPDATE_TASKS_DOCUMENT_APPROPRIATE_EXTENSIONS):
        raise TasksFileFormatError

    raw_file: Optional[BinaryIO] = await bot.download(file=message.document.file_id)
    assert isinstance(raw_file, BytesIO)

    tasks_descriptions: List[str] = yaml.safe_load(raw_file)
    assert isinstance(tasks_descriptions, list)
    for description in tasks_descriptions:
        assert isinstance(description, str)

    return [TaskModel(description=description) for description in tasks_descriptions]


async def send_task_on_confirmation(message: Message, bot: Bot, task_association_id: int, task: TaskModel) -> None:
    assert message.from_user is not None
    user: UserModel = await get_user_by_id(id=message.from_user.id)

    assert message.photo is not None
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
