class Log:
    """
    Basic logger class for handling different severity levels for printing.
    """

    class Severity:
        NOLOG = 0
        DEBUG = 1
        INFO = 2
        WARNING = 3
        ERROR = 4

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
