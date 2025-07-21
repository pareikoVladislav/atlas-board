from django.db import models
from django.utils.translation import gettext_lazy as _

from src.projects.models.base_model import BaseFieldsModel


class ProjectFile(BaseFieldsModel):
    name = models.CharField(_('File Name'), max_length=120)
    file_path = models.CharField(_('File Path'), max_length=255)
    uploaded_by = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='uploaded_files',
        help_text='User who uploaded the file'
    )
    is_public = models.BooleanField(_('Is Public'), default=False)

    class Meta:
        db_table = "project_files"
        verbose_name = "Project File"
        verbose_name_plural = "Project Files"

    def __str__(self):
        return f"{self.name}"