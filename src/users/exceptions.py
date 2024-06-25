from src.users.constants import ErrorDetails
from src.core.exceptions import DetailedException


class InvalidUserError(DetailedException):
    DETAIL = ErrorDetails.INVALID_USER


class UserAlreadyExistsError(DetailedException):
    DETAIL = ErrorDetails.USER_ALREADY_EXISTS


class UserNotFoundError(DetailedException):
    DETAIL = ErrorDetails.USER_NOT_FOUND


class UserHasNoPermissionsError(DetailedException):
    DETAIL = ErrorDetails.USER_HAS_NO_PERMISSIONS
