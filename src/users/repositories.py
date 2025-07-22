from typing import TypeVar, Optional
from django.db.models import Model
from django.db import DatabaseError, OperationalError

from src.users.models import User
from src.projects.repositories.base import BaseRepository

Model_ = TypeVar('Model_', bound=Model)

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)