from enum import IntEnum, auto


class Log:
    """

    """

    class Severity(IntEnum):
        DEBUG = auto()
        INFO = auto()
        WARNING = auto()
        ERROR = auto()

    severity = Severity.DEBUG

    @classmethod
    def debug(cls, msg: str) -> None:
        if cls.severity >= cls.Severity.DEBUG:
            print(msg)

    @classmethod
    def info(cls, msg: str) -> None:
        if cls.severity >= cls.Severity.INFO:
            print(msg)

    @classmethod
    def warning(cls, msg: str) -> None:
        if cls.severity >= cls.Severity.WARNING:
            print(msg)

    @classmethod
    def error(cls, msg: str) -> None:
        if cls.severity >= cls.Severity.ERROR:
            print(msg)
