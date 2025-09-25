from sqlalchemy.orm import Session
from fastapi import status
from models.task.task import Task as TaskModel, TaskStatus as TaskStatusModel, TaskPriority as TaskPriorityModel
from schemas.task import (
    TaskCreate, TaskUpdate, TaskOut,
    TaskStatusCreate, TaskStatusUpdate, TaskStatusOut,
    TaskPriorityCreate, TaskPriorityUpdate, TaskPriorityOut
)
from crud.base import CRUDBase
from utils.response import AppException
from models.user.user import User as UserModel,Role as RoleModel
from models.project.project import Project as ProjectModel
# Initialize CRUD for each model
task_crud = CRUDBase(TaskModel)
task_status_crud = CRUDBase(TaskStatusModel)
task_priority_crud = CRUDBase(TaskPriorityModel)

class TaskService:
    def __init__(self, db: Session):
        self.db = db
    # ---------------- Task ----------------
    def create_task(self, task_in: TaskCreate):
        try:
            db_task = task_crud.create(self.db, task_in)
            project=self.db.query(ProjectModel).filter(ProjectModel.id == db_task.project_id).first()
            project_name=project.name if project else None
            # assignvved = self.db.query(RoleModel).filter(RoleModel.id == db_project.created_by).first()
            # creator_name =creator.name if creator else None 
            assingned= self.db.query(UserModel).filter(UserModel.user_id ==db_task.assigned_to).first() 
            assigned_name = assingned.username if assingned else None
            task_out=TaskOut(
                Task_id=db_task.id,
                title=db_task.title,
                description=db_task.description,
                start_date=db_task.start_date,
                due_date=db_task.due_date,
                project_id=db_task.project_id,
                project_name=project_name,
                assigned_id=db_task.assigned_to,
                assigned_name=assigned_name,
                status_id=db_task.status_id,
                status_name=db_task.status.name if db_task.status else None,
                priority_id=db_task.priority_id,
                priority_name=db_task.priority.name if db_task.priority else None,
            )
            return {
                "success": True,
                "message": "Task created successfully",
                "data": task_out,
                "error": None
            }
        except Exception as e:
            raise AppException(
                message="Unexpected error occurred",
                error=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get_tasks(self, skip: int = 0, limit: int = 100):
        try:
            # tasks=self.db.query(TaskModel).offset(skip).limit(limit).all()
            tasks=task_crud.get_multi(self.db,skip=skip,limit=limit)
            result=[]
            for t in tasks:
                project=self.db.query(ProjectModel).filter(ProjectModel.id == t.project_id).first()
                project_name=project.name if project else None
                assingned= self.db.query(UserModel).filter(UserModel.user_id ==t.assigned_to).first() 
                assigned_name = assingned.username if assingned else None
                result.append(TaskOut(
                        Task_id=t.id,
                        title=t.title,
                        description=t.description,
                        start_date=t.start_date,
                        due_date=t.due_date,
                        project_id=t.project_id,
                        project_name=project_name,
                        assigned_id=t.assigned_to,
                        assigned_name=assigned_name,
                        status_id=t.status_id,
                        status_name=t.status.name if t.status else None,
                        priority_id=t.priority_id,
                        priority_name=t.priority.name if t.priority else None,
                    ))
        
            return {
                    "success": True,
                    "message": "Tasks retrieved successfully",
                    "data": result,
                    "error": None
                }
        except Exception as e:
            raise AppException(
                message="Unexpected error occurred",
                error=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get_task(self, task_id: int):
        task = task_crud.get(self.db, id=task_id)
        if not task:
            raise AppException(
                message="Task not found",
                error="Invalid task id",
                status_code=status.HTTP_404_NOT_FOUND
            )
        project=self.db.query(ProjectModel).filter(ProjectModel.id == task.project_id).first()
        project_name=project.name if project else None
            # assignvved = self.db.query(RoleModel).filter(RoleModel.id == db_project.created_by).first()
            # creator_name =creator.name if creator else None 
        assingned= self.db.query(UserModel).filter(UserModel.user_id ==task.assigned_to).first() 
        assigned_name = assingned.username if assingned else None
        task_out=TaskOut(
                Task_id=task.id,
                title=task.title,
                description=task.description,
                start_date=task.start_date,
                due_date=task.due_date,
                project_id=task.project_id,
                project_name=project_name,
                assigned_id=task.assigned_to,
                assigned_name=assigned_name,
                status_id=task.status_id,
                status_name=task.status.name if task.status else None,
                priority_id=task.priority_id,
                priority_name=task.priority.name if task.priority else None,
            )
            
            
        return {
            "success": True,
            "message": "Task retrieved successfully",
            "data": task_out,
            "error": None
        }

    def update_task(self, task_id: int, task_in: TaskUpdate):
        task = task_crud.get(self.db, id=task_id)
        if not task:
            raise AppException(
                message="Task not found",
                error="Invalid task id",
                status_code=status.HTTP_404_NOT_FOUND
            )
        try:
            updated_task = task_crud.update(self.db, db_obj=task, obj_in=task_in)
            project=self.db.query(ProjectModel).filter(ProjectModel.id == updated_task.project_id).first()
            project_name=project.name if project else None
            # assignvved = self.db.query(RoleModel).filter(RoleModel.id == db_project.created_by).first()
            # creator_name =creator.name if creator else None 
            assingned= self.db.query(UserModel).filter(UserModel.user_id ==updated_task.assigned_to).first() 
            assigned_name = assingned.username if assingned else None
            task_out=TaskOut(
                Task_id=updated_task.id,
                title=updated_task.title,
                description=updated_task.description,
                start_date=updated_task.start_date,
                due_date=updated_task.due_date,
                project_id=updated_task.project_id,
                project_name=project_name,
                assigned_id=updated_task.assigned_to,
                assigned_name=assigned_name,
                status_id=updated_task.status_id,
                status_name=updated_task.status.name if updated_task.status else None,
                priority_id=updated_task.priority_id,
                priority_name=updated_task.priority.name if updated_task.priority else None,
            )
            return {
                "success": True,
                "message": "Task updated successfully",
                "data": task_out,
                "error": None
            }
        except Exception as e:
            raise AppException(
                message="Unexpected error occurred",
                error=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete_task(self, task_id: int):
        task = task_crud.get(self.db, id=task_id)
        if not task:
            raise AppException(
                message="Task not found",
                error="Invalid task id",
                status_code=status.HTTP_404_NOT_FOUND
            )
        task_crud.remove(self.db, id=task_id)
        return {
            "success": True,
            "message": "Task deleted successfully",
            "data": {"id": task_id},
            "error": None
        }

    # ---------------- Task Status ----------------
    def create_status(self, status_in: TaskStatusCreate):
        existing = self.db.query(TaskStatusModel).filter(TaskStatusModel.name == status_in.name).first()
        if existing:
            raise AppException(
                message=f"Task status '{existing.name}' already exists",
                error="Duplicate status",
                status_code=status.HTTP_400_BAD_REQUEST,
                data=[]
            )
        db_status = task_status_crud.create(self.db, status_in)
        return {
            "success": True,
            "message": "Task status created successfully",
            "data": TaskStatusOut.from_orm(db_status),
            "error": None
        }

    def get_statuses(self):
        statuses = task_status_crud.get_multi(self.db)
        return {
            "success": True,
            "message": "Task statuses retrieved successfully",
            "data": [TaskStatusOut.from_orm(s) for s in statuses],
            "error": None
        }

    # ---------------- Task Priority ----------------
    def create_priority(self, priority_in: TaskPriorityCreate):
        existing = self.db.query(TaskPriorityModel).filter(TaskPriorityModel.name == priority_in.name).first()
        if existing:
            raise AppException(
                message=f"Task priority '{existing.name}' already exists",
                error="Duplicate priority",
                status_code=status.HTTP_400_BAD_REQUEST,
                data=[]
            )
        db_priority = task_priority_crud.create(self.db, priority_in)
        return {
            "success": True,
            "message": "Task priority created successfully",
            "data": TaskPriorityOut.from_orm(db_priority),
            "error": None
        }

    def get_priorities(self):
        priorities = task_priority_crud.get_multi(self.db)
        return {
            "success": True,
            "message": "Task priorities retrieved successfully",
            "data": [TaskPriorityOut.from_orm(p) for p in priorities],
            "error": None
        }
