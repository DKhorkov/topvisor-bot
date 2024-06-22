from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class ErrorDetails:
    """
    Users error messages for custom exceptions.
    """

    INVALID_USER: str = 'Current user is invalid'
    USER_ALREADY_EXISTS: str = 'User with provided credentials already exists'
    USER_NOT_FOUND: str = 'User with provided credentials not found'
    USER_ATTRIBUTE_REQUIRED: str = 'user id, email or username is required'


@dataclass(frozen=True)
class UserRoles:
    ADMIN: str = 'admin'
    DEFAULT: str = 'default'


ADMINS_TELEGRAM_IDS: List[int] = [415749541, 367790380]
