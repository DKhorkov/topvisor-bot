from typing import List, Optional, Sequence, Any
from sqlalchemy import insert, select, delete, update, Result, RowMapping, Row

from src.tasks.interfaces.repositories import TasksRepository, TasksAssociationsRepository
from src.tasks.domain.models import TaskModel, TaskAssociationModel
from src.core.database.interfaces.repositories import SQLAlchemyAbstractRepository
from src.core.interfaces import AbstractModel


class SQLAlchemyTasksRepository(SQLAlchemyAbstractRepository, TasksRepository):

    async def get(self, id: int) -> Optional[TaskModel]:
        result: Result = await self._session.execute(select(TaskModel).filter_by(id=id))
        return result.scalar_one_or_none()

    async def get_by_description(self, description: str) -> Optional[TaskModel]:
        result: Result = await self._session.execute(select(TaskModel).filter_by(description=description))
        return result.scalar_one_or_none()

    async def add(self, model: AbstractModel) -> TaskModel:
        result: Result = await self._session.execute(
            insert(TaskModel).values(**await model.to_dict(exclude={'id'})).returning(TaskModel)
        )

        return result.scalar_one()

    async def update(self, id: int, model: AbstractModel) -> TaskModel:
        result: Result = await self._session.execute(
            update(TaskModel).filter_by(id=id).values(**await model.to_dict(exclude={'id'})).returning(TaskModel)
        )

        return result.scalar_one()

    async def delete(self, id: int) -> None:
        await self._session.execute(delete(TaskModel).filter_by(id=id))

    async def list(self) -> List[TaskModel]:
        """
        Returning result object instead of converting to new objects by
                    [TaskModel(**await r.to_dict()) for r in result.scalars().all()]
        to avoid sqlalchemy.orm.exc.UnmappedInstanceError lately.

        Checking by asserts, that expected return type is equal to fact return type.
        """

        result: Result = await self._session.execute(select(TaskModel))
        tasks: Sequence[Row | RowMapping | Any] = result.scalars().all()

        assert isinstance(tasks, List)
        for task in tasks:
            assert isinstance(task, TaskModel)

        return tasks


class SQLAlchemyTasksAssociationsRepository(SQLAlchemyAbstractRepository, TasksAssociationsRepository):

    async def get(self, id: int) -> Optional[TaskAssociationModel]:
        result: Result = await self._session.execute(select(TaskAssociationModel).filter_by(id=id))
        return result.scalar_one_or_none()

    async def add(self, model: AbstractModel) -> TaskAssociationModel:
        result: Result = await self._session.execute(
            insert(TaskAssociationModel).values(**await model.to_dict(exclude={'id'})).returning(TaskAssociationModel)
        )

        return result.scalar_one()

    async def update(self, id: int, model: AbstractModel) -> TaskAssociationModel:
        result: Result = await self._session.execute(
            update(
                TaskAssociationModel
            ).filter_by(
                id=id
            ).values(
                **await model.to_dict(exclude={'id'})
            ).returning(
                TaskAssociationModel
            )
        )

        return result.scalar_one()

    async def delete(self, id: int) -> None:
        await self._session.execute(delete(TaskAssociationModel).filter_by(id=id))

    async def list(self) -> List[TaskAssociationModel]:
        """
        Returning result object instead of converting to new objects by
                    [TaskAssociationModel(**await r.to_dict()) for r in result.scalars().all()]
        to avoid sqlalchemy.orm.exc.UnmappedInstanceError lately.

        Checking by asserts, that expected return type is equal to fact return type.
        """

        result: Result = await self._session.execute(select(TaskAssociationModel))
        task_associations: Sequence[Row | RowMapping | Any] = result.scalars().all()

        assert isinstance(task_associations, List)
        for task_association in task_associations:
            assert isinstance(task_association, TaskAssociationModel)

        return task_associations

    async def get_associated_tasks_by_task_id(self, task_id: int) -> List[TaskAssociationModel]:
        result: Result = await self._session.execute(select(TaskAssociationModel).filter_by(task_id=task_id))
        task_associations: Sequence[Row | RowMapping | Any] = result.scalars().all()

        assert isinstance(task_associations, List)
        for task_association in task_associations:
            assert isinstance(task_association, TaskAssociationModel)

        return task_associations

    async def get_associated_tasks_by_user_id(self, user_id: int) -> List[TaskAssociationModel]:
        result: Result = await self._session.execute(select(TaskAssociationModel).filter_by(user_id=user_id))
        task_associations: Sequence[Row | RowMapping | Any] = result.scalars().all()

        assert isinstance(task_associations, List)
        for task_association in task_associations:
            assert isinstance(task_association, TaskAssociationModel)

        return task_associations
