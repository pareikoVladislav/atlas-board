from enum import IntEnum


class Priority(IntEnum):
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5

    @classmethod
    def choices(cls):
        return [(attr.name, attr.value) for attr in cls]