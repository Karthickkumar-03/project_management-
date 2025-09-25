from crud.base import CRUDBase
from models.project.project import Project, ProjectStatus, ProjectPriority
from schemas.project import ProjectCreate, ProjectUpdate, ProjectStatusCreate, ProjectStatusUpdate, ProjectPriorityCreate, ProjectPriorityUpdate

project_crud = CRUDBase[Project, ProjectCreate, ProjectUpdate](Project)
project_status_crud = CRUDBase[ProjectStatus, ProjectStatusCreate, ProjectStatusUpdate](ProjectStatus)
project_priority_crud = CRUDBase[ProjectPriority, ProjectPriorityCreate, ProjectPriorityUpdate](ProjectPriority)
