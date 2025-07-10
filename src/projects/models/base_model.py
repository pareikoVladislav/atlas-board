from django.db import models
from django.utils import timezone

class BaseFieldsModel(models.Model):
    created_at: timezone = models.DateTimeField(auto_now_add=True)
    updated_at: timezone = models.DateTimeField(auto_now=True)
    deleted_at: timezone = models.DateTimeField(null=True, blank=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
