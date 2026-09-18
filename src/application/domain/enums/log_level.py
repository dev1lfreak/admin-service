from enum import Enum


class LogLevel(Enum):
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50
    EXCEPTION = 60

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"[{self.value}, '{self.name}']"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, LogLevel):
            return self.value == other.value
        if isinstance(other, int):
            return self.value == other
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __lt__(self, other: object) -> bool:
        if isinstance(other, LogLevel):
            return self.value < other.value
        if isinstance(other, int):
            return self.value < other
        return NotImplemented

    def __le__(self, other: object) -> bool:
        if isinstance(other, LogLevel):
            return self.value <= other.value
        if isinstance(other, int):
            return self.value <= other
        return NotImplemented

    def __gt__(self, other: object) -> bool:
        if isinstance(other, LogLevel):
            return self.value > other.value
        if isinstance(other, int):
            return self.value > other
        return NotImplemented

    def __ge__(self, other: object) -> bool:
        if isinstance(other, LogLevel):
            return self.value >= other.value
        if isinstance(other, int):
            return self.value >= other
        return NotImplemented
