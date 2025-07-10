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


## Создать модель Tag для категоризации задач
### Поля модели Tag
# - название тега `name`

### Конфигурация Tag
# - **Таблица**: `tags`
# - **Verbose names**: Tag/Tags
# - **Строковое представление**: через name
# - **Уникальность**: name должен быть уникальным


## 2. Обновить модель Task - добавить связь с тегами
### Дополнительное поле в Task
# - теги задачи `tags`

### Особенности M2M связи
# - Использовать строковую ссылку для избежания циклических импортов `'Tag'`
# - обратная связь от тега к задачам

## 3. Назначение системы тегов
### Примеры использования тегов:
# - **По технологии**: backend, frontend, database
# - **По типу**: bug, feature, improvement, tests
# - **По сложности**: easy, medium, hard
# - **По компоненту**: api, ui, auth
# M2M связь с Task
#tags = models.ManyToManyField('Tag', related_name='tasks', blank=True)
