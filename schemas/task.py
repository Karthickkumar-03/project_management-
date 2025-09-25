from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .project import ProjectBase
# ---------------- Task Status ----------------
class TaskStatusBase(BaseModel):
    name: str


class TaskStatusCreate(TaskStatusBase):
    pass


class TaskStatusUpdate(TaskStatusBase):
    pass


class TaskStatusOut(TaskStatusBase):
    id: int

    class Config:
        from_attributes = True


# ---------------- Task Priority ----------------
class TaskPriorityBase(BaseModel):
    name: str


class TaskPriorityCreate(TaskPriorityBase):
    pass


class TaskPriorityUpdate(TaskPriorityBase):
    pass


class TaskPriorityOut(TaskPriorityBase):
    id: int

    class Config:
        from_attributes = True

# ---------------- Task ----------------
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    project_id: int
    assigned_to: Optional[int] = None
    status_id: int
    priority_id: int


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    project_id: Optional[int] = None
    assigned_to: Optional[int] = None
    status_id: Optional[int] = None
    priority_id: Optional[int] = None


class TaskOut(BaseModel):
    Task_id:int
    title:str
    description:str
    start_date:Optional[datetime]
    due_date:Optional[datetime]
    project_id:int
    project_name:Optional[str]
    assigned_id:int
    assigned_name:Optional[str]
    status_id:int
    status_name:Optional[str]
    priority_id:int
    priority_name:Optional[str]
    
    class Config:
        from_attributes = True
