from django.db import models

from src.projects.models import Task
from src.users.models import User


class TimeEntry(models.Model):
    task: Task = models.ForeignKey(
        'Task',
        on_delete=models.CASCADE,
        related_name='time_entries',
        verbose_name='Task'
    )
    user: User = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='time_entries',
        verbose_name='User'
    )
    hours = models.PositiveIntegerField(verbose_name='Hours')
    logged_at = models.DateTimeField(auto_now_add=True)
    verbose_name = 'Logged At'

    class Meta:
        db_table = 'time_entries'
        verbose_name = 'Time Entry'
        verbose_name_plural = 'Time Entries'

    def __str__(self):
        return f"{self.user.username} logged {self.hours} hours on task '{self.task.title}'"
