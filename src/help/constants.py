from dataclasses import dataclass


@dataclass(frozen=True)
class CommandNames:
    HELP: str = 'help'
