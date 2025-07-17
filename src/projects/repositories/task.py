from src.projects.models import Task
from src.projects.repositories.base import BaseRepository


class TaskRepository(BaseRepository):
    def __init__(self):
        super().__init__(Task)
