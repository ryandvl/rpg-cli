from abc import ABC


class LoggerMessagePartInterface(ABC):
    message: str
    color: int
