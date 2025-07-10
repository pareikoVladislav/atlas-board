from django.db import models


class Tag(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,

    )

    class Meta:
        db_table = 'tags'
        ordering = ['name']
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self) -> str:
        return self.name
