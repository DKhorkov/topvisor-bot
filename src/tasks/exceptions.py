from src.tasks.constants import ErrorDetails
from src.core.exceptions import DetailedHTTPException


class TaskAlreadyExistsError(DetailedHTTPException):
    DETAIL = ErrorDetails.TASK_ALREADY_EXISTS


class TaskNotFoundError(DetailedHTTPException):
    DETAIL = ErrorDetails.TASK_NOT_FOUND


class TaskAssociationNotFoundError(DetailedHTTPException):
    DETAIL = ErrorDetails.TASK_ASSOCIATION_NOT_FOUND
