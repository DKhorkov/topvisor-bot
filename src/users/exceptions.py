

from src.users.constants import ErrorDetails
from src.core.exceptions import DetailedHTTPException


class InvalidUserError(DetailedHTTPException):
    DETAIL = ErrorDetails.INVALID_USER


class UserAlreadyExistsError(DetailedHTTPException):
    DETAIL = ErrorDetails.USER_ALREADY_EXISTS


class UserNotFoundError(DetailedHTTPException):
    DETAIL = ErrorDetails.USER_NOT_FOUND
