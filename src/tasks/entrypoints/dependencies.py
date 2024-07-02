from typing import List, Dict
from aiogram.types import Message

from src.tasks.domain.models import TaskModel, TaskAssociationModel
from src.tasks.entrypoints.views import TasksViews
from src.tasks.service_layer.service import TasksService
from src.tasks.service_layer.units_of_work import SQLAlchemyTasksUnitOfWork
from src.tasks.entrypoints.schemas import UserTaskStatisticsResponseScheme, UserActiveTaskScheme
from src.users.domain.models import UserModel
from src.users.entrypoints.dependencies import get_all_users, get_user_by_id


async def get_user_tasks_statistics(message: Message) -> List[UserTaskStatisticsResponseScheme]:
    assert message.from_user is not None  # Check for mypy. Also register should work only with private messages

    tasks_views: TasksViews = TasksViews(uow=SQLAlchemyTasksUnitOfWork())
    return await tasks_views.get_user_tasks_statistics(user_id=message.from_user.id)


async def get_actual_tasks() -> List[TaskModel]:
    tasks_service: TasksService = TasksService(uow=SQLAlchemyTasksUnitOfWork())
    return [task for task in await tasks_service.get_all_tasks() if not task.is_archived]


async def update_tasks(tasks: List[TaskModel]) -> List[TaskModel]:
    tasks_service: TasksService = TasksService(uow=SQLAlchemyTasksUnitOfWork())
    await tasks_service.archive_old_tasks(new_tasks=tasks)

    users: List[UserModel] = await get_all_users()
    for task in tasks:
        if not await tasks_service.check_task_existence(description=task.description):
            await tasks_service.create_task(
                task=task,
                users=users
            )
        else:
            task = await tasks_service.get_task_by_description(description=task.description)
            if task.is_archived:
                await tasks_service.reopen_task(id=task.id)

    return await get_actual_tasks()


async def get_user_active_tasks(message: Message) -> List[UserActiveTaskScheme]:
    assert message.from_user is not None

    tasks_service: TasksService = TasksService(uow=SQLAlchemyTasksUnitOfWork())
    user_active_task_associations: List[TaskAssociationModel] = [
        task_association for task_association in await tasks_service.get_user_tasks_associations(
            user_id=message.from_user.id
        ) if not (task_association.task_archived or task_association.task_completed)
    ]

    tasks_storage: Dict[int, TaskModel] = {task.id: task for task in await tasks_service.get_all_tasks()}
    return [
        UserActiveTaskScheme(
            description=tasks_storage[task_association.task_id].description,
            task_association_id=task_association.id
        ) for task_association in user_active_task_associations
    ]


async def get_task_by_association_id(task_association_id: int) -> TaskModel:
    tasks_service: TasksService = TasksService(uow=SQLAlchemyTasksUnitOfWork())
    return await tasks_service.get_task_by_association_id(task_association_id=task_association_id)


async def get_user_by_association_id(task_association_id: int) -> UserModel:
    tasks_service: TasksService = TasksService(uow=SQLAlchemyTasksUnitOfWork())
    task_association: TaskAssociationModel = await tasks_service.get_task_association_by_id(
        task_association_id=task_association_id
    )

    return await get_user_by_id(id=task_association.user_id)


async def set_task_competed_for_user(task_association_id: int) -> None:
    tasks_service: TasksService = TasksService(uow=SQLAlchemyTasksUnitOfWork())
    await tasks_service.set_task_association_completed_status(task_association_id=task_association_id)
