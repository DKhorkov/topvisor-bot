from abc import ABC

from src.tasks.interfaces.repositories import TasksRepository, TasksAssociationsRepository
from src.core.interfaces import AbstractUnitOfWork


class TasksUnitOfWork(AbstractUnitOfWork, ABC):
    """
    An interface for work with tasks, that is used by service layer of tasks module.
    The main goal is that implementations of this interface can be easily replaced in the service layer
    using dependency injection without disrupting its functionality.
    """

    tasks: TasksRepository
    tasks_associations: TasksAssociationsRepository
