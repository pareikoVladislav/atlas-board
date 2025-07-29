from typing import TypeVar, Type, Optional, Any
from django.db.models import Model, QuerySet
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import DatabaseError, OperationalError, IntegrityError, transaction

Model_ = TypeVar('Model_', bound=Model)


class BaseRepository:
    def __init__(self, model: Type[Model_]) -> None:
        self.model = model

    def get_by_id(self, id_: int) -> Optional[Model_]:
        try:
            obj_id = self._normalize_id(id_)
            obj = self.model.objects.get(pk=obj_id)
            return obj
        except ObjectDoesNotExist as e:
            raise ObjectDoesNotExist(str(e))
        except ValueError as e:
            raise ValidationError(str(e))
        except DatabaseError as e:
            raise OperationalError(f'Failed to retrieve {self.model.__name__} with id {id}') from e

    def get_all(self) -> QuerySet[Model_]:
        try:
            qs = self.model.objects.all()
            return qs
        except DatabaseError as e:
            raise OperationalError(f'Failed to retrieve {self.model.__name__} objects') from e

    @transaction.atomic
    def create(self, **kwargs) -> Model_:
        try:
            obj = self.model.objects.create(**kwargs)
            return obj
        except ValidationError as v:
            raise ValidationError(f'Validation failed for {self.model.__name__} object') from v
        except IntegrityError as i:
            raise IntegrityError(f'Integrity constraint validation for {self.model.__name__} object') from i
        except DatabaseError as e:
            raise OperationalError(f'Failed to create {self.model.__name__} object') from e

    @transaction.atomic
    def update(self, id_: int, **kwargs) -> Model_:
        try:
            id_ = self._normalize_id(id_)
            obj = self.get_by_id(id_)
            if obj is None:
                raise ObjectDoesNotExist(f'Object with id {id_} does not exist')
            for attr, value in kwargs.items():
                setattr(obj, attr, value)
                obj.save()
            return obj
        except ValidationError as v:
            raise ValidationError(f'Validation failed for {self.model.__name__} object') from v
        except IntegrityError as i:
            raise IntegrityError(f'Integrity constraint validation for {self.model.__name__} object') from i
        except DatabaseError as e:
            raise OperationalError(f'Failed to update {self.model.__name__} object') from e

    @transaction.atomic
    def delete(self, id_: int) -> None:
        try:
            id_ = self._normalize_id(id_)
            obj = self.get_by_id(id_)
            if obj is None:
                raise ObjectDoesNotExist(f'Object with id {id_} does not exist')
            obj.delete()

        except DatabaseError as e:
            raise OperationalError(f'Failed to delete {self.model.__name__} object') from e

    def _normalize_id(self, id_: Any) -> int:
        if isinstance(id_, int):
            return id_
        else:
            if not id_.isdigit():
                raise ValueError('id must be an integer')
            int_id = int(id_)
            if int_id < 1:
                raise ValueError('id must be positive')
            return int_id