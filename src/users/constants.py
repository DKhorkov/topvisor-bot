from dataclasses import dataclass, astuple
from typing import Tuple, Any


@dataclass(frozen=True)
class ErrorDetails:
    """
    Users error messages for custom exceptions.
    """

    INVALID_USER: str = 'Current user is invalid'
    USER_ALREADY_EXISTS: str = 'User with provided credentials already exists'
    USER_NOT_FOUND: str = 'User with provided credentials not found'
    USER_ATTRIBUTE_REQUIRED: str = 'user id, first_name or username is required'
    USER_HAS_NO_PERMISSIONS: str = 'User has no permissions for current operation'


@dataclass(frozen=True)
class UserRoles:
    ADMIN: str = 'admin'
    DEFAULT: str = 'default'


@dataclass(frozen=True)
class AdminsIds:
    D3M0S666: int = 415749541
    elizlisian: int = 367790380

    def tuple(self) -> Tuple[Any, ...]:
        return astuple(self)
