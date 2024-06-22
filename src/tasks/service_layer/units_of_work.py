from typing import Self

from src.tasks.interfaces.repositories import TasksRepository, TasksAssociationsRepository
from src.tasks.interfaces.units_of_work import TasksUnitOfWork
from src.tasks.adapters.repositories import SQLAlchemyTasksRepository, SQLAlchemyTasksAssociationsRepository
from src.core.database.interfaces.units_of_work import SQLAlchemyAbstractUnitOfWork


class SQLAlchemyTasksUnitOfWork(SQLAlchemyAbstractUnitOfWork, TasksUnitOfWork):

    async def __aenter__(self) -> Self:
        uow = await super().__aenter__()
        self.tasks: TasksRepository = SQLAlchemyTasksRepository(session=self._session)
        self.tasks_associations: TasksAssociationsRepository = SQLAlchemyTasksAssociationsRepository(
            session=self._session
        )
        return uow
