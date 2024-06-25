from dataclasses import dataclass


@dataclass(frozen=True)
class ErrorDetails:
    """
    Tasks error messages for custom exceptions.
    """

    TASK_ALREADY_EXISTS: str = 'Task with provided data already exists'
    TASK_NOT_FOUND: str = 'Task with provided data not found'
    TASK_ASSOCIATION_NOT_FOUND: str = 'Task association with provided data not found'
    TASK_ATTRIBUTE_REQUIRED: str = 'task id or description is required'
    TASKS_FILE_FORMAT_ERROR: str = 'Tasks file format should be a YAML'


@dataclass(frozen=True)
class CommandNames:
    USER_TASKS_STATISTICS: str = 'my_stats'
