from src.projects.views.project import (
    get_all_projects,
    update_project,
    create_new_project,
    get_all_project_files
)
from src.projects.views.tag import (
    delete_tag,
    get_all_tags,
    create_tag,
    get_tag_by_id,
    update_tag,
)
from src.projects.views.task import (
    TaskViewSet
)

from src.projects.views.project_file import (
    file_detail,
)



__all__ = (
    "get_all_projects",
    "update_project",
    "create_new_project",
  
    "get_all_project_files",
  

    "get_all_tags",
    "get_tag_by_id",
    "create_tag",
    "delete_tag",
    "update_tag",

    "file_detail"
)
