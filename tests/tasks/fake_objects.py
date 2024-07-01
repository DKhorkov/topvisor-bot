from typing import Dict, Optional, List

from src.tasks.interfaces.units_of_work import TasksUnitOfWork
from src.tasks.interfaces.repositories import TasksRepository, TasksAssociationsRepository
from src.tasks.domain.models import TaskModel, TaskAssociationModel
from src.core.interfaces import AbstractModel


class FakeTasksRepository(TasksRepository):

    def __init__(self, tasks: Optional[Dict[int, TaskModel]] = None) -> None:
        self.tasks: Dict[int, TaskModel] = tasks if tasks else {}

    async def get_by_description(self, description: str) -> Optional[TaskModel]:
        for task in self.tasks.values():
            if task.description == description:
                return task

        return None

    async def get(self, id: int) -> Optional[TaskModel]:
        return self.tasks.get(id)

    async def add(self, model: AbstractModel) -> TaskModel:
        task: TaskModel = TaskModel(**await model.to_dict())
        self.tasks[task.id] = task
        return task

    async def update(self, id: int, model: AbstractModel) -> TaskModel:
        task: TaskModel = TaskModel(**await model.to_dict())
        if id in self.tasks:
            self.tasks[id] = task

        return task

    async def delete(self, id: int) -> None:
        if id in self.tasks:
            del self.tasks[id]

    async def list(self) -> List[TaskModel]:
        return list(self.tasks.values())


class FakeTasksAssociationsRepository(TasksAssociationsRepository):

    def __init__(self, tasks_associations: Optional[Dict[int, TaskAssociationModel]] = None) -> None:
        self.tasks_associations: Dict[int, TaskAssociationModel] = tasks_associations if tasks_associations else {}

    async def get(self, id: int) -> Optional[TaskAssociationModel]:
        return self.tasks_associations.get(id)

    async def get_task_associations_by_task_id(self, task_id: int) -> List[TaskAssociationModel]:
        return [
            task_association for task_association in self.tasks_associations.values() if
            task_association.task_id == task_id
        ]

    async def get_tasks_associations_by_user_id(self, user_id: int) -> List[TaskAssociationModel]:
        return [
            task_association for task_association in self.tasks_associations.values() if
            task_association.user_id == user_id
        ]

    async def add(self, model: AbstractModel) -> TaskAssociationModel:
        task_association: TaskAssociationModel = TaskAssociationModel(**await model.to_dict())
        self.tasks_associations[task_association.id] = task_association
        return task_association

    async def update(self, id: int, model: AbstractModel) -> TaskAssociationModel:
        task_association: TaskAssociationModel = TaskAssociationModel(**await model.to_dict())
        if id in self.tasks_associations:
            self.tasks_associations[id] = task_association

        return task_association

    async def delete(self, id: int) -> None:
        if id in self.tasks_associations:
            del self.tasks_associations[id]

    async def list(self) -> List[TaskAssociationModel]:
        return list(self.tasks_associations.values())


class FakeTasksUnitOfWork(TasksUnitOfWork):

    def __init__(
            self,
            tasks_repository: TasksRepository,
            tasks_associations_repository: TasksAssociationsRepository
    ) -> None:

        super().__init__()
        self.tasks: TasksRepository = tasks_repository
        self.tasks_associations: TasksAssociationsRepository = tasks_associations_repository
        self.committed: bool = False

    async def commit(self) -> None:
        self.committed = True

    async def rollback(self) -> None:
        pass
