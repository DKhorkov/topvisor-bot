from typing import List
from aiogram.types import Message

from src.tasks.service_layer.service import TasksService
from src.tasks.service_layer.units_of_work import SQLAlchemyTasksUnitOfWork
from src.users.constants import UserRoles, ADMINS_TELEGRAM_IDS
from src.users.domain.models import UserModel
from src.users.entrypoints.views import UsersViews
from src.users.service_layer.service import UsersService
from src.users.service_layer.units_of_work import SQLAlchemyUsersUnitOfWork


async def register_user(message: Message) -> UserModel:
    assert message.from_user is not None  # Check for mypy. Also register should work only with private messages
    users_service: UsersService = UsersService(uow=SQLAlchemyUsersUnitOfWork())

    user: UserModel
    if not await users_service.check_user_existence(id=message.from_user.id):
        user = await users_service.register_user(
            user=UserModel(
                id=message.from_user.id,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                username=message.from_user.username,
                is_bot=message.from_user.is_bot,
                role=UserRoles.DEFAULT if message.from_user.id not in ADMINS_TELEGRAM_IDS else UserRoles.ADMIN
            )
        )

        tasks_service: TasksService = TasksService(uow=SQLAlchemyTasksUnitOfWork())
        await tasks_service.create_tasks_associations_for_user(user=user)
    else:
        user = await users_service.get_user_by_id(id=message.from_user.id)

    return user


async def get_all_users() -> List[UserModel]:
    users_views: UsersViews = UsersViews(uow=SQLAlchemyUsersUnitOfWork())
    return await users_views.get_all_users()
