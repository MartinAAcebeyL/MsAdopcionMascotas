from graphene import Enum


class SizeEnum(Enum):
    SMALL = "small"
    MIDDLE = "middle"
    BIG = "big"


class StatusEnum(Enum):
    PROGRESS = "progress"
    ADOPTED = "adopted"
    ABLE = "able"


class SexEnum(Enum):
    M = "M"
    F = "F"
