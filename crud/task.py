from crud.base import CRUDBase
from models.task.task import Task, TaskStatus, TaskPriority
from schemas.task import TaskCreate, TaskUpdate, TaskStatusCreate, TaskStatusUpdate, TaskPriorityCreate, TaskPriorityUpdate

# Task CRUD
task_crud = CRUDBase[Task, TaskCreate, TaskUpdate](Task)

# Task Status CRUD
task_status_crud = CRUDBase[TaskStatus, TaskStatusCreate, TaskStatusUpdate](TaskStatus, name_field="name")

# Task Priority CRUD
task_priority_crud = CRUDBase[TaskPriority, TaskPriorityCreate, TaskPriorityUpdate](TaskPriority, name_field="name")
