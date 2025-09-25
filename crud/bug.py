from crud.base import CRUDBase
from models.bug.bug import Bug, BugStatus, BugPriority, BugEnvironment
from schemas.bug import BugCreate, BugUpdate, BugStatusCreate, BugPriorityCreate, BugEnvironmentCreate

# Bug CRUD
bug_crud = CRUDBase(Bug)

# Bug Status CRUD
bug_status_crud = CRUDBase(BugStatus, name_field="name")

# Bug Priority CRUD
bug_priority_crud = CRUDBase(BugPriority, name_field="name")

# Bug Environment CRUD
bug_environment_crud = CRUDBase(BugEnvironment, name_field="name")
