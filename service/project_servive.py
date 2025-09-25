from sqlalchemy.orm import Session
from fastapi import status
from models.user.user import User as UserModel,Role as RoleModel
from models.project.project import Project as ProjectModel, ProjectStatus as ProjectStatusModel, ProjectPriority as ProjectPriorityModel
from schemas.project import (
    ProjectCreate, ProjectUpdate, ProjectOut,
    ProjectStatusCreate, ProjectStatus as ProjectStatusSchema,
    ProjectPriorityCreate, ProjectPriority as ProjectPrioritySchema
)
from crud.base import CRUDBase
from utils.response import AppException

# CRUD instances
project_crud = CRUDBase(ProjectModel)
project_status_crud = CRUDBase(ProjectStatusModel)
project_priority_crud = CRUDBase(ProjectPriorityModel)


class ProjectService:
    def __init__(self, db: Session):
        self.db = db

    # ---------------- Create Project ----------------
    def create_project(self, project_in: ProjectCreate):
        try:
            existing_project = self.db.query(ProjectModel).filter(ProjectModel.name == project_in.name).first()
            if existing_project:
                 raise AppException(f"Project'{existing_project.name}' already exists", "Duplicate status", status.HTTP_400_BAD_REQUEST, data=None)

            db_project = project_crud.create(self.db, project_in)

            creator = self.db.query(UserModel).filter(UserModel.user_id == db_project.created_by).first()
            creator_name =creator.username if creator else None 
            upadter = self.db.query(UserModel).filter(UserModel.user_id == db_project.updated_by).first() 
            print(upadter)
            updater_name = upadter.username if upadter else None
            project_out = ProjectOut(
                id=db_project.id,
                name=db_project.name,
                description=db_project.description,
                start_date=db_project.start_date,
                end_date=db_project.end_date,
                
                status_id=db_project.status_id,
                status_name=db_project.status.status_name if db_project.status else None,
                
                priority_id=db_project.priority_id,
                priority_name=db_project.priority.priority_name if db_project.priority else None,
                
                created_by=creator_name,
                created_at=db_project.created_at,
                
                updated_at=db_project.updated_at,
                updated_by=updater_name
            )

            return {"success": True, "message": "Project created successfully", "data": project_out, "error": None}
        except AppException:
            raise

        except Exception as e:
            raise AppException("Unexpected error occurred", str(e), 500)

    # ---------------- Get All Projects ----------------
    def get_projects(self, skip: int = 0, limit: int = 100):
        # projects = self.db.query(ProjectModel).offset(skip).limit(limit).all()
        projects=project_crud.get_multi(self.db,skip=skip,limit=limit)
        result = []

        for p in projects:
            creator = self.db.query(RoleModel).filter(RoleModel.id == p.created_by).first()
            creator_name =creator.name if creator else None 
            upadter = self.db.query(UserModel).filter(UserModel.user_id == p.created_by).first() 
            updater_name = upadter.username if upadter else None
            result.append(ProjectOut(
                id=p.id,
                name=p.name,
                description=p.description,
                start_date=p.start_date,
                end_date=p.end_date,
                status_id=p.status_id,
                status_name=p.status.status_name if p.status else None,
                priority_id=p.priority_id,
                priority_name=p.priority.priority_name if p.priority else None,
                created_by=creator_name,
                created_at=p.created_at,
                updated_at=p.updated_at,
                updated_by=updater_name
            ))

        return {"success": True, "message": "Projects retrieved successfully", "data": result, "error": None}

    # ---------------- Get Single Project ----------------
    def get_project(self, project_id: int):
        project = project_crud.get(self.db, project_id)
        if not project:
            raise AppException("Project not found", "Invalid project ID", status.HTTP_404_NOT_FOUND)

        creator = self.db.query(RoleModel).filter(RoleModel.id == project.created_by).first()
        creator_name =creator.name if creator else None 
        upadter = self.db.query(UserModel).filter(UserModel.user_id == project.created_by).first() 
        updater_name = upadter.username if upadter else None
        project_out = ProjectOut(
            id=project.id,
            name=project.name,
            description=project.description,
            start_date=project.start_date,
            end_date=project.end_date,
            status_id=project.status_id,
            status_name=project.status.status_name if project.status else None,
            priority_id=project.priority_id,
            priority_name=project.priority.priority_name if project.priority else None,
            created_by=creator_name,
            created_at=project.created_at,
            updated_at=project.updated_at,
            updated_by=updater_name
        )

        return {"success": True, "message": "Project retrieved successfully", "data": project_out, "error": None}

    # ---------------- Update Project ----------------
    def update_project(self, project_id: int, project_in: ProjectUpdate):
        project = project_crud.get(self.db, project_id)
        if not project:
            raise AppException("Project not found", "Invalid project ID", status.HTTP_404_NOT_FOUND)

        try:
            updated_project = project_crud.update(self.db, project, project_in)

            creator = self.db.query(RoleModel).filter(RoleModel.id == updated_project.created_by).first()
            creator_name =creator.name if creator else None 
            upadter = self.db.query(UserModel).filter(UserModel.user_id ==updated_project.created_by).first() 
            updater_name = upadter.username if upadter else None
            project_out = ProjectOut(
                id=updated_project.id,
                name=updated_project.name,
                description=updated_project.description,
                start_date=updated_project.start_date,
                end_date=updated_project.end_date,
                status_id=updated_project.status_id,
                status_name=updated_project.status.status_name if updated_project.status else None,
                priority_id=updated_project.priority_id,
                priority_name=updated_project.priority.priority_name if updated_project.priority else None,
                created_by=creator_name,
                created_at=updated_project.created_at,
                updated_at=updated_project.updated_at,
                updated_by=updater_name
            )

            return {"success": True, "message": "Project updated successfully", "data": project_out, "error": None}

        except Exception as e:
            raise AppException("Unexpected error occurred", str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)

    # ---------------- Delete Project ----------------
    def delete_project(self, project_id: int):
        project = project_crud.get(self.db, project_id)
        if not project:
            raise AppException("Project not found", "Invalid project ID", status.HTTP_404_NOT_FOUND)

        project_crud.remove(self.db, project_id)
        return {"success": True, "message": "Project deleted successfully", "data": None, "error": None}

    # ---------------- Project Status ----------------
    def create_status(self, status_in: ProjectStatusCreate):
        existing = self.db.query(ProjectStatusModel).filter(ProjectStatusModel.status_name == status_in.status_name).first()
        if existing:
            raise AppException(f"Status '{existing.status_name}' already exists", "Duplicate status", status.HTTP_400_BAD_REQUEST, data=[])

        db_status = project_status_crud.create(self.db, status_in)
        return {"success": True, "message": "Status created successfully", "data": ProjectStatusSchema.from_orm(db_status), "error": None}

    def get_statuses(self):
        statuses = project_status_crud.get_multi(self.db)
        return {"success": True, "message": "Statuses retrieved successfully", "data": [ProjectStatusSchema.from_orm(s) for s in statuses], "error": None}

    # ---------------- Project Priority ----------------
    def create_priority(self, priority_in: ProjectPriorityCreate):
        existing = self.db.query(ProjectPriorityModel).filter(ProjectPriorityModel.priority_name == priority_in.priority_name).first()
        if existing:
            raise AppException(f"Priority '{existing.priority_name}' already exists", "Duplicate priority", status.HTTP_400_BAD_REQUEST, data=[])

        db_priority = project_priority_crud.create(self.db, priority_in)
        return {"success": True, "message": "Priority created successfully", "data": ProjectPrioritySchema.from_orm(db_priority), "error": None}

    def get_priorities(self):
        priorities = project_priority_crud.get_multi(self.db)
        return {"success": True, "message": "Priorities retrieved successfully", "data": [ProjectPrioritySchema.from_orm(p) for p in priorities], "error": None}


