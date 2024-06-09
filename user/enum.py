from enum import Enum


class EnumStatus(Enum):
    pending = "pending"
    accepted = "accepted"
    rejected= "rejected"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)