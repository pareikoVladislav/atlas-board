from src.projects.repositories import BaseRepository
from src.projects.models import ProjectFile


class ProjectFileRepository(BaseRepository):
    def __init__(self):
        super().__init__(ProjectFile)







