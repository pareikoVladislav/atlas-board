from src.projects.models.project import Project
from src.projects.repositories.base import BaseRepository


class ProjectRepository(BaseRepository):
    def __init__(self):
        super().__init__(Project)
