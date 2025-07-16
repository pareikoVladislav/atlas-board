from src.projects.repositories import BaseRepository
from src.projects.models import Project

class ProjectRepository(BaseRepository):
    def __init__(self):
        super().__init__(Project)
