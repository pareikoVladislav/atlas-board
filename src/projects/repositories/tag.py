from src.projects.models import Tag
from src.projects.repositories.base import BaseRepository


class TagRepository(BaseRepository):
    def __init__(self):
        super().__init__(Tag)