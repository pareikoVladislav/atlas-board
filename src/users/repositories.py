from typing import TypeVar, Optional
from django.db.models import Model
from django.db import DatabaseError, OperationalError

from src.users.models import User
from src.projects.repositories.base import BaseRepository

Model_ = TypeVar('Model_', bound=Model)

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, email: str) -> Optional[Model_]:
        try:
            obj = self.model.objects.get(email=email)
            return obj
        except self.model.DoesNotExist:
            return None
        except DatabaseError as e:
            raise OperationalError(f'Failed to retrieve {self.model.__name__} with email {email}') from e
