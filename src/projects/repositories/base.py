from typing import TypeVar, Type, Optional
from django.db.models import Model, QuerySet
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import DatabaseError, OperationalError, IntegrityError, transaction

Model_ = TypeVar('Model_', bound=Model)


class BaseRepository:
    def __init__(self, model: Type[Model_]) -> None:
        self.model = model

    def get_by_id(self, id_: int) -> Optional[Model_]:
        if isinstance(id_, int) and id_ > 0:
            try:
                obj = self.model.objects.get(id=id_)
                return obj
            except self.model.DoesNotExist as e:
                raise ObjectDoesNotExist(f'{self.model.__name__} with id {id_} does not exist') from e
            except DatabaseError as e:
                raise OperationalError(f'Failed to retrieve {self.model.__name__} with id {id_}') from e
        else:
            raise ValueError('id must be positive integer')

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
            obj = self.get_by_id(id_)
            if obj is None:
                raise ObjectDoesNotExist(f'Object with id {id_} does not exist')
            obj.delete()
        except DatabaseError as e:
            raise OperationalError(f'Failed to delete {self.model.__name__} object') from e
