from typing import Optional, List, Set

from src.tasks.constants import ErrorDetails
from src.tasks.domain.models import TaskModel, TaskAssociationModel
from src.tasks.exceptions import TaskNotFoundError, TaskAssociationNotFoundError
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
                        task_id=task.id,
                        task_archived=task.is_archived
                    )
                ) for task in await uow.tasks.list()
            ]

            await uow.commit()
            return task_associations

    async def get_user_tasks_associations(self, user_id: int) -> List[TaskAssociationModel]:
        async with self._uow as uow:
            task_associations: List[
                TaskAssociationModel
            ] = await uow.tasks_associations.get_associated_tasks_by_user_id(user_id=user_id)

            return task_associations

    async def archive_old_tasks(self, new_tasks: List[TaskModel]) -> None:
        new_tasks_descriptions: Set[str] = {task.description for task in new_tasks}
        async with self._uow as uow:
            for task in await uow.tasks.list():
                if not (task.is_archived or task.description in new_tasks_descriptions):
                    task.is_archived = True

                    task_associations: List[
                        TaskAssociationModel
                    ] = await uow.tasks_associations.get_associated_tasks_by_task_id(task_id=task.id)

                    for task_association in task_associations:
                        task_association.task_archived = True

                    await uow.commit()

    async def get_task_by_description(self, description: str) -> TaskModel:
        async with self._uow as uow:
            task: Optional[TaskModel] = await uow.tasks.get_by_description(description=description)
            if not task:
                raise TaskNotFoundError

            return task

    async def reopen_task(self, id: int) -> TaskModel:
        async with self._uow as uow:
            task: Optional[TaskModel] = await uow.tasks.get(id=id)
            if not task:
                raise TaskNotFoundError

            task.is_archived = False

            task_associations: List[
                TaskAssociationModel
            ] = await uow.tasks_associations.get_associated_tasks_by_task_id(task_id=task.id)

            for task_association in task_associations:
                task_association.task_archived = False

            await uow.commit()
            return task

    async def get_task_by_association_id(self, task_association_id: int) -> TaskModel:
        async with self._uow as uow:
            task_association: Optional[TaskAssociationModel] = await uow.tasks_associations.get(id=task_association_id)
            if not task_association:
                raise TaskAssociationNotFoundError

            task: Optional[TaskModel] = await uow.tasks.get(id=task_association.task_id)
            if not task:
                raise TaskNotFoundError

            return task

    async def get_task_association_by_id(self, task_association_id: int) -> TaskAssociationModel:
        async with self._uow as uow:
            task_association: Optional[TaskAssociationModel] = await uow.tasks_associations.get(id=task_association_id)
            if not task_association:
                raise TaskAssociationNotFoundError

            return task_association

    async def set_task_association_completed_status(self, task_association_id: int) -> TaskAssociationModel:
        async with self._uow as uow:
            task_association: Optional[TaskAssociationModel] = await uow.tasks_associations.get(id=task_association_id)
            if not task_association:
                raise TaskAssociationNotFoundError

            if not task_association.task_archived and not task_association.task_completed:
                task_association.task_completed = True
                await uow.commit()

            return task_association
