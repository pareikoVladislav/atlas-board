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
    update_tag
)

from src.projects.views.project_file import (
    file_detail,
    FileProjectAPIView,
)

__all__ = (
    "get_all_projects",
    "update_project",
    "create_new_project",
  
    "get_all_project_files",
  
    "task_list",
    "task_detail",
  
    "analytics_per_project",
    "analytics_per_developer",

    "get_all_tags",
    "get_tag_by_id",
    "create_tag",
    "update_tag",
    "delete_tag",
  
    "file_detail",
    "FileProjectAPIView",
)
