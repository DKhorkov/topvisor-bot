from typing import Optional, List
from abc import ABC, abstractmethod

from src.core.interfaces import AbstractRepository, AbstractModel
from src.tasks.domain.models import TaskModel, TaskAssociationModel


class TasksRepository(AbstractRepository, ABC):
    """
    An interface for work with tasks, that is used by tasks unit of work.
    The main goal is that implementations of this interface can be easily replaced in tasks unit of work
    using dependency injection without disrupting its functionality.
    """

    @abstractmethod
    async def add(self, model: AbstractModel) -> TaskModel:
        raise NotImplementedError

    @abstractmethod
    async def get(self, id: int) -> Optional[TaskModel]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_description(self, description: str) -> Optional[TaskModel]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: int, model: AbstractModel) -> TaskModel:
        raise NotImplementedError

    @abstractmethod
    async def list(self) -> List[TaskModel]:
        raise NotImplementedError


class TasksAssociationsRepository(AbstractRepository, ABC):
    """
    An interface for work with many-2-many tasks associations table, that is used by tasks unit of work.
    The main goal is that implementations of this interface can be easily replaced in tasks unit of work
    using dependency injection without disrupting its functionality.
    """

    @abstractmethod
    async def add(self, model: AbstractModel) -> TaskAssociationModel:
        raise NotImplementedError

    @abstractmethod
    async def get(self, id: int) -> Optional[TaskAssociationModel]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: int, model: AbstractModel) -> TaskAssociationModel:
        raise NotImplementedError

    @abstractmethod
    async def list(self) -> List[TaskAssociationModel]:
        raise NotImplementedError

    @abstractmethod
    async def get_associated_tasks_by_task_id(self, task_id: int) -> List[TaskAssociationModel]:
        raise NotImplementedError

    @abstractmethod
    async def get_associated_tasks_by_user_id(self, user_id: int) -> List[TaskAssociationModel]:
        raise NotImplementedError
