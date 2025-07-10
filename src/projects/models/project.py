from datetime import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _

from src.choices.common import Priority
from src.choices.project import ProjectStatus
from src.projects.models.base_model import BaseFieldsModel


class Project(BaseFieldsModel):
    name: str = models.CharField(_('Name'), max_length=100, unique=True)
    description: str = models.TextField(_('Description'))
    owner = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='owned_projects',
        help_text="The user who created the project."
    )
    team_lead = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        related_name='lead_projects',
        help_text="The user responsible for overseeing the project."
    )
    members = models.ManyToManyField(
        'User',
        related_name='projects',
        help_text="Users participating in the project"
    )
    start_date: datetime = models.DateField(_('Start date'), null=True)
    status: str = models.CharField(
        _('Status'),
        max_length=30,
        choices=ProjectStatus.choices
    )
    is_active: bool = models.BooleanField(_('Is active'))
    priority: int = models.PositiveSmallIntegerField(
        _('Priority'),
        choices=Priority.choices(),
        help_text="The priority level of the project."
    )

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return f"{self.name}"
