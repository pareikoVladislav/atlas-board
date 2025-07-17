from src.projects.views.project import (
    get_all_projects,
    update_project,
    create_new_project,
)

from src.projects.views.task import (
    task_list,
    task_detail,
)

__all__ = (
    "get_all_projects",
    "create_new_project",
    "update_project",
    "task_list",
    "task_detail",
)

