from dataclasses import dataclass

from src.core.interfaces import AbstractModel


@dataclass
class FakeModel(AbstractModel):
    """
    Inherited model from base just to test AbstractModel's methods.
    """

    field1: str = 'test'
    field2: int = 123
