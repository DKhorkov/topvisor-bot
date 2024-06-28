from typing import Sequence
from aiogram import html

from src.tasks.constants import ConfirmTaskCompletenessData
from src.tasks.domain.models import TaskModel
from src.tasks.entrypoints.schemas import UserTaskStatisticsResponseScheme
from src.users.domain.models import UserModel


class TemplateCreator:

    @staticmethod
    async def user_tasks_statistics_message(
            tasks_statistics: Sequence[UserTaskStatisticsResponseScheme]
    ) -> str:
        return 'Here is your tasks statistics:\n' + '\n'.join(
            [
                f'{stat.description} - ✅' if stat.is_completed else f'{stat.description} - ❌'
                for stat in tasks_statistics
            ]
        )

    @staticmethod
    async def tasks_updated_message(tasks: Sequence[TaskModel]) -> str:
        return 'Tasks were successfully updated!\nNow next tasks are available:\n' + '\n'.join(
            f'{number}) {task.description}' for number, task in enumerate(tasks, start=1)
        )

    @staticmethod
    async def complete_task_message() -> str:
        return 'Please, select task, which you completeness you want to confirm:'

    @staticmethod
    async def prove_completed_task_message(task: TaskModel, task_association_id: int) -> str:
        return (
            f'{ConfirmTaskCompletenessData.START_TEXT}\n\n'
            f'To complete task "{html.bold(task.description)}", please send a photo replying to this message!\n\n'
            f'{ConfirmTaskCompletenessData.TASK_ASSOCIATION_ID_TEXT} {html.bold(str(task_association_id))}'
        )

    @staticmethod
    async def task_sent_on_confirmation_message(task: TaskModel) -> str:
        return f'Task "{html.bold(task.description)}" with provided photo has been successfully sent on confirmation!'

    @staticmethod
    async def to_admin_task_confirmation_message(task: TaskModel, user: UserModel) -> str:
        return (
            f'{user.full_name} ({user.url}) want\'s to complete task "{html.bold(task.description)}".\n'
            f'Here is provided photo.\n'
            f'Confirm task completeness?'
        )

    @staticmethod
    async def task_completeness_confirmed_message() -> str:
        return 'Task completeness was successfully confirmed!'
