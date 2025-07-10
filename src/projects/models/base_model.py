from datetime import datetime

from django.db import models


class BaseFieldsModel(models.Model):
    created_at: datetime = models.DateField(auto_now_add=True)
    updated_at: datetime = models.DateField(auto_now=True)
    deleted_at: datetime = models.DateField(auto_now=True)
    deleted: bool = models.BooleanField(default=False, db_default=False)
