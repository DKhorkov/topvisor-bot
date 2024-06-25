from typing import Sequence

from src.tasks.domain.models import TaskModel
from src.tasks.entrypoints.schemas import UserTasksStatisticsResponseScheme


class TemplateCreator:

    @staticmethod
    async def user_tasks_statistics_message(
            tasks_statistics: Sequence[UserTasksStatisticsResponseScheme]
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
