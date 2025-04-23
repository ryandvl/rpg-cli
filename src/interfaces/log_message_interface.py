from src.globals import ABC


class LogMessagePartInterface(ABC):
    message: str
    color: int


class LogMessageInterface(ABC):
    message_parts: list[LogMessagePartInterface]
