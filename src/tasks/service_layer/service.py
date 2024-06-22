from typing import Optional, List

from src.tasks.constants import ErrorDetails
from src.tasks.domain.models import TaskModel, TaskAssociationModel
from src.tasks.exceptions import TaskNotFoundError
from src.tasks.interfaces.units_of_work import TasksUnitOfWork
from src.users.domain.models import UserModel


class TasksService:
    """
    Service layer core according to DDD, which using a unit of work, will perform operations on the domain model.
    """

    def __init__(self, uow: TasksUnitOfWork) -> None:
        self._uow: TasksUnitOfWork = uow

    async def create_task(self, task: TaskModel, users: List[UserModel]) -> TaskModel:
        async with self._uow as uow:
            task = await uow.tasks.add(model=task)
            for user in users:
                await uow.tasks_associations.add(
                    model=TaskAssociationModel(
                        user_id=user.id,
                        task_id=task.id
                    )
                )

            await uow.commit()
            return task

    async def check_task_existence(
            self,
            id: Optional[int] = None,
            description: Optional[str] = None
    ) -> bool:

        if not (id or description):
            raise ValueError(ErrorDetails.TASK_ATTRIBUTE_REQUIRED)

        async with self._uow as uow:
            task: Optional[TaskModel]  # declaring here for mypy passing
            if id:
                task = await uow.tasks.get(id=id)
                if task:
                    return True

            if description:
                task = await uow.tasks.get_by_description(description)
                if task:
                    return True

        return False

    async def get_task_by_id(self, id: int) -> TaskModel:
        async with self._uow as uow:
            task: Optional[TaskModel] = await uow.tasks.get(id=id)
            if not task:
                raise TaskNotFoundError

            return task

    async def get_all_tasks(self) -> List[TaskModel]:
        async with self._uow as uow:
            tasks: List[TaskModel] = await uow.tasks.list()
            return tasks

    async def create_tasks_associations_for_user(self, user: UserModel) -> List[TaskAssociationModel]:
        async with self._uow as uow:
            task_associations: List[TaskAssociationModel] = [
                await uow.tasks_associations.add(
                    model=TaskAssociationModel(
                        user_id=user.id,
                        task_id=task.id
                    )
                ) for task in await uow.tasks.list()
            ]

            return task_associations

    async def get_user_tasks_associations(self, user_id: int) -> List[TaskAssociationModel]:
        async with self._uow as uow:
            task_associations: List[
                TaskAssociationModel
            ] = await uow.tasks_associations.get_associated_tasks_by_user_id(user_id=user_id)

            return task_associations
