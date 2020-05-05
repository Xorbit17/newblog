from enum import Enum, auto


class Role(Enum):
    VISITOR = auto()
    AUTHOR = auto()
    ADMIN = auto()
