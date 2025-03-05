from abc import ABC

from src.interfaces.logger_message_part import LoggerMessagePartInterface

class LoggerMessageInterface(ABC):
    message_parts: list[LoggerMessagePartInterface]
