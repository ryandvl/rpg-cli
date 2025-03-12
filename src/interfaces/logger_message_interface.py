from abc import ABC

from .logger_message_part_interface import LoggerMessagePartInterface


class LoggerMessageInterface(ABC):
    message_parts: list[LoggerMessagePartInterface]
