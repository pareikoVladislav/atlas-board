from src.projects.models import TimeEntry
from src.projects.repositories import BaseRepository


class TimeEntryRepository(BaseRepository):
    def __init__(self):
        super().__init__(TimeEntry)
