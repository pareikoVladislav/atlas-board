from enum import Enum


class ProjectStatus(tuple, Enum):
    ACTIVE = ('active', 'Active')
    ON_HOLD = ('on_hold', 'On Hold')
    COMPLETED = ('completed', 'Completed')
    CANCELLED = ('canceled', 'Canceled')
    PLANNING = ('planning', 'Planning')

    @classmethod
    def choices(cls):
        return [(attr.value[0], attr.value[1]) for attr in cls]
