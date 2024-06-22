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
