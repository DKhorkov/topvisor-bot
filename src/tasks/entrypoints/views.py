from typing import List

from src.tasks.domain.models import TaskModel, TaskAssociationModel
from src.tasks.entrypoints.schemas import UserTasksStatisticsResponseScheme
from src.tasks.interfaces.units_of_work import TasksUnitOfWork
from src.tasks.service_layer.service import TasksService


class TasksViews:
    """
    Views related to tasks, which purpose is to return information upon read requests,
    due to the fact that write requests (represented by commands) are different from read requests.

    # TODO At current moment uses repositories pattern to retrieve data. In future can be changed on raw SQL
    # TODO for speed-up purpose
    """

    def __init__(self, uow: TasksUnitOfWork) -> None:
        self._uow: TasksUnitOfWork = uow

    async def get_all_tasks(self) -> List[TaskModel]:
        tasks: List[TaskModel] = await TasksService(uow=self._uow).get_all_tasks()

        # Return only not archived tasks:
        return [task for task in tasks if not task.is_archived]

    async def get_user_tasks_statistics(self, user_id: int) -> List[UserTasksStatisticsResponseScheme]:
        tasks_service: TasksService = TasksService(uow=self._uow)

        # Only not archived task associations should be processed:
        task_associations: List[TaskAssociationModel] = [
            task_association for task_association in
            await tasks_service.get_user_tasks_associations(user_id=user_id) if not task_association.task_archived
        ]

        return [
            UserTasksStatisticsResponseScheme(
                description=(await tasks_service.get_task_by_id(id=task_association.task_id)).description,
                is_completed=task_association.task_completed
            ) for task_association in task_associations
        ]
