from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ---------------- Bug ----------------
class BugBase(BaseModel):
    title: str
    description: Optional[str] = None
    project_id: int
    reporter_id: int
    assignee_id: Optional[int] = None
    status_id: int
    priority_id: int
    environment_id: Optional[int] = None
    created_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None

class BugCreate(BugBase):
    pass

class BugUpdate(BugBase):
    pass

class BugOut(BaseModel):
    Bug_id: int
    title:str
    Description:str
    reporter_id:int
    reporter_name:Optional[str]
    project_id:int
    project_name:Optional[str]
    assigned_id:int
    assigned_name:Optional[str]
    BugStatus_id:int 
    Bugstatus_name:Optional[str]
    priority_id:int
    priority_name:Optional[str]
    environment_id:int
    environment_name:Optional[str]
    created_at:datetime
    class Config:
        from_attributes = True


# ---------------- Bug Status ----------------
class BugStatusBase(BaseModel):
    name: str

class BugStatusCreate(BugStatusBase):
    pass

class BugStatusUpdate(BugStatusBase):
    pass

class BugStatusOut(BugStatusBase):
    id: int

    class Config:
        from_attributes = True


# ---------------- Bug Priority ----------------
class BugPriorityBase(BaseModel):
    name: str

class BugPriorityCreate(BugPriorityBase):
    pass

class BugPriorityUpdate(BugPriorityBase):
    pass

class BugPriorityOut(BugPriorityBase):
    id: int

    class Config:
        from_attributes = True


# ---------------- Bug Environment ----------------
class BugEnvironmentBase(BaseModel):
    name: str

class BugEnvironmentCreate(BugEnvironmentBase):
    pass

class BugEnvironmentUpdate(BugEnvironmentBase):
    pass

class BugEnvironmentOut(BugEnvironmentBase):
    id: int

    class Config:
        from_attributes = True
