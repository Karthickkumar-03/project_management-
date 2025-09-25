from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from configurations.database import get_db
from service.task_service import TaskService
from utils.response import AppException
from schemas.task import TaskCreate, TaskUpdate, TaskStatusCreate, TaskPriorityCreate

router = APIRouter(prefix="/tasks", tags=["Tasks"])
# ---------------- Task Status ----------------
@router.post("/status")
def create_status(status_in: TaskStatusCreate, db: Session = Depends(get_db)):
    try:
        return TaskService(db).create_status(status_in)
    except AppException as e:
        # Already formatted response from AppException
        return e.detail


@router.get("/status")
def read_statuses(db: Session = Depends(get_db)):
    try:
        return TaskService(db).get_statuses()
    except AppException as e:
        # Already formatted response from AppException
        return e.detail

    

# ---------------- Task Priority ----------------
@router.post("/priority")
def create_priority(priority_in: TaskPriorityCreate, db: Session = Depends(get_db)):
    try:
        return TaskService(db).create_priority(priority_in)
    except AppException as e:
        # Already formatted response from AppException
        return e.detail


@router.get("/priority")
def read_priorities(db: Session = Depends(get_db)):
    return TaskService(db).get_priorities()

# ---------------- Task ----------------
@router.post("/")
def create_task(task_in: TaskCreate, db: Session = Depends(get_db)):
    return TaskService(db).create_task(task_in)

@router.get("/")
def read_tasks(db: Session = Depends(get_db)):
    return TaskService(db).get_tasks()

@router.get("/{task_id}")
def read_task(task_id: int, db: Session = Depends(get_db)):
    try:
        return TaskService(db).get_task(task_id)
    except AppException as e:
        # Already formatted response from AppException
        return e.detail

@router.put("/{task_id}")
def update_task(task_id: int, task_in: TaskUpdate, db: Session = Depends(get_db)):
    return TaskService(db).update_task(task_id, task_in)

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    try:
        return TaskService(db).delete_task(task_id)
    except AppException as e:
        # Already formatted response from AppException
        return e.detail

