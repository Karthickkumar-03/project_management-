from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from configurations.database import get_db
from schemas.bug import (
    BugCreate, BugUpdate,
    BugStatusCreate, BugPriorityCreate, BugEnvironmentCreate
)
from service.bug_service import BugService
from utils.response import AppException

router = APIRouter(
    prefix="/bugs",
    tags=["Bugs"]
)

# Dependency to get service
def get_service(db: Session = Depends(get_db)):
    return BugService(db)

# ---------------- Bug Status ----------------
@router.post("/status/", response_model=dict)
def create_bug_status(status_in: BugStatusCreate, service: BugService = Depends(get_service)):
    try:
        return service.create_bug_status(status_in)
    except AppException as e:
        # Already formatted response from AppException
        return e.detail

@router.get("/status/", response_model=dict)
def get_bug_statuses(service: BugService = Depends(get_service)):
    return service.get_bug_statuses()

# ---------------- Bug Priority ----------------
@router.post("/priority/", response_model=dict)
def create_bug_priority(priority_in: BugPriorityCreate, service: BugService = Depends(get_service)):
    try:
        return service.create_bug_priority(priority_in)
    except AppException as e:
        # Already formatted response from AppException
        return e.detail

@router.get("/priority/", response_model=dict)
def get_bug_priorities(service: BugService = Depends(get_service)):
    return service.get_bug_priorities()

# ---------------- Bug Environment ----------------
@router.post("/environment/", response_model=dict)
def create_bug_environment(env_in: BugEnvironmentCreate, service: BugService = Depends(get_service)):
    try:
        return service.create_bug_environment(env_in)
    except AppException as e:
        # Already formatted response from AppException
        return e.detail

@router.get("/environment/", response_model=dict)
def get_bug_environments(service: BugService = Depends(get_service)):
    return service.get_bug_environments()

# ---------------- Bug ----------------
@router.post("/", response_model=dict)
def create_bug(bug_in: BugCreate, service: BugService = Depends(get_service)):
    return service.create_bug(bug_in)

@router.get("/", response_model=dict)
def get_bugs(service: BugService = Depends(get_service)):
    return service.get_bugs()

@router.get("/{bug_id}", response_model=dict)
def get_bug(bug_id: int, service: BugService = Depends(get_service)):
    try:
        return service.get_bug(bug_id)
    except AppException as e:
        # Already formatted response from AppException
        return e.detail

@router.put("/{bug_id}", response_model=dict)
def update_bug(bug_id: int, bug_in: BugUpdate, service: BugService = Depends(get_service)):
    try:
        return service.update_bug(bug_id, bug_in)
    except AppException as e:
        # Already formatted response from AppException
        return e.detail

@router.delete("/{bug_id}", response_model=dict)
def delete_bug(bug_id: int, service: BugService = Depends(get_service)):
    try:
        return service.delete_bug(bug_id)
    except AppException as e:
        # Already formatted response from AppException
        return e.detail
