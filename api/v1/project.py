from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from configurations.database import get_db
from schemas.project import *
from service.project_servive import ProjectService
from schemas.response import ResponseModel
from utils.response import AppException

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)

# Dependency to get service
def get_service(db: Session = Depends(get_db)) -> ProjectService:
    return ProjectService(db)
#---------------- project Status ----------------
@router.post("/status/", response_model=dict)
def create_status(status_in: ProjectStatusCreate, service: ProjectService = Depends(get_service)):
    try:
        return service.create_status(status_in)
    except AppException as e:
        # Already formatted response from AppException
        return e.detail

@router.get("/status/", response_model=dict)
def get_statuses(service: ProjectService = Depends(get_service)):
    try:
        return service.get_statuses()
    except AppException as e:
        # Already formatted response from AppException
        return e.detail
    
#---------------- project prority ----------------
@router.post("/priority/", response_model=dict)
def create_priority(priority_in: ProjectPriorityCreate, service: ProjectService = Depends(get_service)):
    try:
        return service.create_priority(priority_in)
    except AppException as e:
        # Already formatted response from AppException
        return e.detail

@router.get("/priority/", response_model=dict)
def get_priorities(service: ProjectService = Depends(get_service)):
    try:
        return service.get_priorities()
    except AppException as e:
        # Already formatted response from AppException
        return e.detail

# ----------------- Project Endpoints -----------------

# Create Project
@router.post("/", response_model=ResponseModel[ProjectOut])
def create_project(project_in: ProjectCreate, service: ProjectService = Depends(get_service)):
    try:
        return service.create_project(project_in)
    except AppException as e:
        # Already formatted response from AppException
        return e.detail

# Get all Projects
@router.get("/", response_model=ResponseModel[list[ProjectOut]])
def get_projects(service: ProjectService = Depends(get_service)):
    try:
        return service.get_projects()
    except AppException as e:
        # Already formatted response from AppException
        return e.detail

# Get single Project
@router.get("/{project_id}", response_model=ResponseModel[ProjectOut])
def get_project(project_id: int, service: ProjectService = Depends(get_service)):
    try:
        return service.get_project(project_id)
    except AppException as e:
        # Already formatted response from AppException
        return e.detail
    

# Update Project
@router.put("/{project_id}", response_model=ResponseModel[ProjectOut])
def update_project(project_id: int, project_in: ProjectUpdate, service: ProjectService = Depends(get_service)):
    try:
        return service.update_project(project_id, project_in)
    except AppException as e:
        # Already formatted response from AppException
        return e.detail

# Delete Project
@router.delete("/{project_id}", response_model=ResponseModel[None])
def delete_project(project_id: int, service: ProjectService = Depends(get_service)):
    try:
        return service.delete_project(project_id)
    except AppException as e:
        # Already formatted response from AppException
        return e.detail
