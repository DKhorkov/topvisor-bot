from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from typing import List

from src.core.utils import get_substring_after_chars
from src.tasks.domain.models import TaskModel, TaskAssociationModel
from src.tasks.entrypoints.callback_data import CompleteTaskCallbackData, ConfirmTaskCompletenessCallbackData
from src.tasks.entrypoints.dependencies import (
    get_user_tasks_statistics,
    update_tasks,
    get_user_active_tasks,
    get_task_by_association_id,
    set_task_competed_for_user,
    get_user_by_association_id,
    get_task_association_by_id
)
from src.tasks.constants import CommandNames, ConfirmTaskCompletenessData, CallbackDataActions, MessageFileTypes
from src.tasks.entrypoints.schemas import (
    UserTaskStatisticsResponseScheme,
    UserActiveTaskScheme
)
from src.tasks.entrypoints.templates import TemplateCreator
from src.tasks.entrypoints.markups import MarkupCreator
from src.tasks.entrypoints.utils import get_new_tasks_from_message, send_task_on_confirmation
from src.users.domain.models import UserModel
from src.users.entrypoints.dependencies import get_user_by_id

tasks_router: Router = Router()


@tasks_router.message(Command(CommandNames.USER_TASKS_STATISTICS))
async def user_tasks_statistics_handler(message: Message) -> None:
    await message.delete()
    tasks_statistics: List[UserTaskStatisticsResponseScheme] = await get_user_tasks_statistics(message=message)
    await message.answer(
        text=await TemplateCreator.user_tasks_statistics_message(
            tasks_statistics=tasks_statistics
        )
    )


@tasks_router.message(Command(CommandNames.COMPLETE_TASK))
async def complete_task_handler(message: Message) -> None:
    await message.delete()
    user_active_tasks: List[UserActiveTaskScheme] = await get_user_active_tasks(message=message)
    if not user_active_tasks:
        await message.answer(text=await TemplateCreator.all_tasks_already_completed_by_user())
    else:
        await message.answer(
            text=await TemplateCreator.complete_task_message(),
            reply_markup=await MarkupCreator.complete_task_markup(tasks=user_active_tasks)
        )


@tasks_router.callback_query(CompleteTaskCallbackData.filter(F.action == CallbackDataActions.COMPLETE_TASK))
async def prove_completed_task_handler(
        query: CallbackQuery,
        callback_data: CompleteTaskCallbackData,
        bot: Bot
) -> None:

    assert query.message is not None
    await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
    task: TaskModel = await get_task_by_association_id(task_association_id=callback_data.task_association_id)
    await bot.send_message(
        chat_id=query.message.chat.id,
        text=await TemplateCreator.prove_completed_task_message(
            task=task,
            task_association_id=callback_data.task_association_id
        )
    )


@tasks_router.callback_query(
    ConfirmTaskCompletenessCallbackData.filter(F.action == CallbackDataActions.CONFIRM_TASK_COMPLETENESS)
)
async def confirm_task_completeness_handler(
        query: CallbackQuery,
        callback_data: ConfirmTaskCompletenessCallbackData,
        bot: Bot
) -> None:

    task_association: TaskAssociationModel = await get_task_association_by_id(
        task_association_id=callback_data.task_association_id
    )

    if not task_association.task_completed:
        await set_task_competed_for_user(task_association_id=callback_data.task_association_id)

        task: TaskModel = await get_task_by_association_id(task_association_id=callback_data.task_association_id)
        user: UserModel = await get_user_by_association_id(task_association_id=callback_data.task_association_id)
        admin: UserModel = await get_user_by_id(id=query.from_user.id)
        await bot.send_message(
            chat_id=user.id,
            text=await TemplateCreator.task_completeness_confirmed_message(
                task=task,
                admin=admin
            )
        )

        await query.answer(text=await TemplateCreator.task_completeness_confirmed_query_answer())
    else:
        await query.answer(
            text=await TemplateCreator.task_completeness_was_already_confirmed_by_another_admin_query_answer()
        )

    assert query.message is not None
    assert isinstance(query.message, Message)
    await query.message.delete_reply_markup()


@tasks_router.callback_query(
    ConfirmTaskCompletenessCallbackData.filter(F.action == CallbackDataActions.REJECT_TASK_COMPLETENESS)
)
async def reject_task_completeness_handler(
        query: CallbackQuery,
        callback_data: ConfirmTaskCompletenessCallbackData,
        bot: Bot
) -> None:

    task_association: TaskAssociationModel = await get_task_association_by_id(
        task_association_id=callback_data.task_association_id
    )

    if not task_association.task_completed:
        task: TaskModel = await get_task_by_association_id(task_association_id=callback_data.task_association_id)
        user: UserModel = await get_user_by_association_id(task_association_id=callback_data.task_association_id)
        admin: UserModel = await get_user_by_id(id=query.from_user.id)
        await bot.send_message(
            chat_id=user.id,
            text=await TemplateCreator.task_completeness_rejected_message(
                task=task,
                admin=admin
            )
        )

        await query.answer(text=await TemplateCreator.task_completeness_rejected_query_answer())
    else:
        await query.answer(
            text=await TemplateCreator.task_completeness_was_already_confirmed_by_another_admin_query_answer()
        )

    assert query.message is not None
    assert isinstance(query.message, Message)
    await query.message.delete_reply_markup()


@tasks_router.message(
    F.content_type.in_({MessageFileTypes.PHOTO, MessageFileTypes.DOCUMENT, MessageFileTypes.VIDEO}),
    F.reply_to_message.text.startswith(ConfirmTaskCompletenessData.START_TEXT)
)
async def send_file_to_confirm_task_completeness_handler(message: Message, bot: Bot) -> None:
    await message.delete()
    assert message.reply_to_message is not None
    await message.reply_to_message.delete()

    assert message.reply_to_message is not None
    assert message.reply_to_message.text is not None
    task_association_id: int = int(
        get_substring_after_chars(
            string=message.reply_to_message.text,
            chars=ConfirmTaskCompletenessData.TASK_ASSOCIATION_ID_TEXT
        )
    )

    task: TaskModel = await get_task_by_association_id(task_association_id=task_association_id)
    await send_task_on_confirmation(message=message, task_association_id=task_association_id, task=task, bot=bot)

    await message.answer(text=await TemplateCreator.task_sent_on_confirmation_message(task=task))


@tasks_router.message(F.content_type.in_({MessageFileTypes.DOCUMENT}))
async def update_tasks_handler(message: Message, bot: Bot) -> None:
    await message.delete()
    new_tasks: List[TaskModel] = await get_new_tasks_from_message(message=message, bot=bot)
    updated_tasks: List[TaskModel] = await update_tasks(tasks=new_tasks)
    await message.answer(
        text=await TemplateCreator.tasks_updated_message(
            tasks=updated_tasks
        )
    )
