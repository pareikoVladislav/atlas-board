from django.db.models import TextChoices


class ProjectStatus(TextChoices):
    ACTIVE = ('active', 'Active')
    ON_HOLD = ('on_hold', 'On Hold')
    COMPLETED = ('completed', 'Completed')
    CANCELLED = ('canceled', 'Canceled')
    PLANNING = ('planning', 'Planning')
