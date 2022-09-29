from enum import Enum


class StrEnum(str, Enum):
    def __str__(self) -> str:
        return self.value


class ListEnum(Enum):
    @classmethod
    def list(cls) -> list[str]:
        return list(map(str, cls))
