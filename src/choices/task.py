from enum import Enum


class Status(str, Enum):
    new = 'New'
    in_progress = 'In Progress'
    done = 'Done'
    pending = 'Pending'
    blocked = 'Blocked'
    close = 'Close'

    @classmethod
    def choices(cls):
        return [(attr.name, attr.value) for attr in cls]

class Priority(tuple, Enum):
    LOW         = (5, 'Low')
    MEDIUM      = (4, 'Medium')
    HIGH        = (3, 'High')
    VERY_HIGH   = (2, 'Very High')
    URGENT      = (1, 'Urgent')

    @classmethod
    def choices(cls):
        return [(attr.value[0], attr.value[1]) for attr in cls]

    def __str__(self):
        return self.value[0]