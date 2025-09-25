from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ---------------- Project Status ----------------
class ProjectStatusBase(BaseModel):
    status_name: str

class ProjectStatusCreate(ProjectStatusBase):
    pass

class ProjectStatusUpdate(BaseModel):
    status_name: str | None = None


class ProjectStatus(ProjectStatusBase):
    id: int

    class Config:
        from_attributes = True

# ---------------- Project Priority ----------------
class ProjectPriorityBase(BaseModel):
   priority_name: str

class ProjectPriorityCreate(ProjectPriorityBase):
    pass

class ProjectPriorityUpdate(BaseModel):
    priority_name: str | None = None
class ProjectPriority(ProjectPriorityBase):
    id: int
    class Config:
        from_attributes = True
# ---------------- Project ----------------
class ProjectBase(BaseModel):
    name: str
    description: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    status_id: int
    priority_id: int

class ProjectCreate(ProjectBase):
    created_by: int
    updated_by:int

class ProjectUpdate(BaseModel):
    name:Optional[str] | None = None
    description: Optional[str] | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    status_id: Optional[int] | None = None
    priority_id: Optional[int] | None = None
    updated_by: Optional[int] = None

class Project(ProjectBase):
    id: int
    status: ProjectStatus | None = None
    priority: ProjectPriority | None = None

    class Config:
        from_attributes = True


class ProjectOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status_id: int
    status_name: Optional[str] = None
    priority_id: int
    priority_name: Optional[str] = None
    created_by: Optional[str] = None  # username of creator
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None

    class Config:
        from_attributes = True