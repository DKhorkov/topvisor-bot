from src.tasks.constants import ErrorDetails
from src.core.exceptions import DetailedException


class TaskAlreadyExistsError(DetailedException):
    DETAIL = ErrorDetails.TASK_ALREADY_EXISTS


class TaskNotFoundError(DetailedException):
    DETAIL = ErrorDetails.TASK_NOT_FOUND


class TaskAssociationNotFoundError(DetailedException):
    DETAIL = ErrorDetails.TASK_ASSOCIATION_NOT_FOUND


class TasksFileFormatError(DetailedException):
    DETAIL = ErrorDetails.TASKS_FILE_FORMAT_ERROR
