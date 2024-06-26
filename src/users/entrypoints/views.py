from typing import List

from src.users.domain.models import UserModel
from src.users.interfaces.units_of_work import UsersUnitOfWork
from src.users.service_layer.service import UsersService


class UsersViews:
    """
    Views related to users, which purpose is to return information upon read requests,
    due to the fact that write requests (represented by commands) are different from read requests.

    # TODO At current moment uses repositories pattern to retrieve data. In future can be changed on raw SQL
    # TODO for speed-up purpose
    """

    def __init__(self, uow: UsersUnitOfWork) -> None:
        self._uow: UsersUnitOfWork = uow

    async def get_user_account(self, user_id: int) -> UserModel:
        return await UsersService(self._uow).get_user_by_id(id=user_id)

    async def get_all_users(self) -> List[UserModel]:
        return await UsersService(self._uow).get_all_users()
