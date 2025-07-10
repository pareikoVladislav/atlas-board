from django.utils import timezone
from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator

from src.projects.models.base_model import BaseFieldsModel
from src.choices import Status, Priority


class Task(BaseFieldsModel):

    title = models.CharField(
        max_length=255,
        validators = [MinLengthValidator(10)]
    )
    description = models.TextField(
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices(),
        default=Status.new)

    priority = models.PositiveSmallIntegerField(
        choices=Priority.choices(),
        default=Priority.LOW)

    estimated_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0.1)],
        help_text='Expected time to complete the task, in hours.'
    )
    deadline: timezone = models.DateTimeField()

    project = models.ForeignKey(
        'Project',  # строковая ссылка на проект
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    assignee = models.ForeignKey(
        'users.User',  # строковая ссылка на пользователя
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tasks"
    )

    created_by = models.ForeignKey(
        'users.User',  # строковая ссылка на пользователя
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_tasks"
    )

    tags = models.ManyToManyField(
        'Tag',
        related_name='tasks',
        blank=True
    )

    class Meta:
        db_table = "tasks"
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        unique_together = ('project', 'title')

    def __str__(self):
        return self.title
