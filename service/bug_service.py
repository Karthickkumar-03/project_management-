from sqlalchemy.orm import Session
from fastapi import status
from models.user.user import User as UserModel,Role as RoleModel
from models.bug.bug import Bug as BugModel, BugStatus as BugStatusModel, BugPriority as BugPriorityModel, BugEnvironment as BugEnvironmentModel
from schemas.bug import (
    BugCreate, BugUpdate, BugOut,
    BugStatusCreate, BugStatusOut,
    BugPriorityCreate, BugPriorityOut,
    BugEnvironmentCreate, BugEnvironmentOut
)
from crud.base import CRUDBase
from models.project.project import Project as ProjectModel, ProjectStatus as ProjectStatusModel, ProjectPriority as ProjectPriorityModel

from utils.response import AppException

# Initialize generic CRUD
bug_crud = CRUDBase(BugModel)
bug_status_crud = CRUDBase(BugStatusModel)
bug_priority_crud = CRUDBase(BugPriorityModel)
bug_environment_crud = CRUDBase(BugEnvironmentModel)

class BugService:
    def __init__(self, db: Session):
        self.db = db

    # ---------------- Bug ----------------
    def create_bug(self, bug_in: BugCreate):
        
        try:
            db_bug = bug_crud.create(self.db, bug_in)
            project = self.db.query(ProjectModel).filter(ProjectModel.id == db_bug.project_id).first()
            project_name = project.name if project else None

            
            assigned = self.db.query(UserModel).filter(UserModel.user_id == db_bug.assignee_id).first()
            assigned_name = assigned.username if assigned else None

            
            reporter = self.db.query(RoleModel).filter(RoleModel.id == db_bug.reporter_id).first()
            reporter_name = reporter.name if reporter else None

            
            bug_out = BugOut(
                        Bug_id=db_bug.id,
                        title=db_bug.title,
                        Description=db_bug.description,
                        
                        reporter_id=db_bug.reporter_id,
                        reporter_name=reporter_name,
                        
                        project_id=db_bug.project_id,
                        project_name=project_name,
                        
                        assigned_id=db_bug.assignee_id,
                        assigned_name=assigned_name,
                        
                        BugStatus_id=db_bug.status_id,
                        Bugstatus_name=db_bug.status.name if db_bug.status else None,
                        
                        priority_id=db_bug.priority_id,
                        priority_name=db_bug.priority.name if db_bug.priority else None,
                        
                        environment_id=db_bug.environment_id,
                        environment_name=db_bug.environment.name if db_bug.environment else None,
                        
                        created_at=db_bug.created_at
                )       

            
            return {
                "success": True,
                "message": "Bug created successfully",
                "data": bug_out,
                "error": None
            }
        except Exception as e:
            raise AppException(
                message="Unexpected error occurred",
                error=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get_bugs(self, skip: int = 0, limit: int = 100):
        try:
            # bugs = self.db.query(BugModel).offset(skip).limit(limit).all()
            bugs=bug_crud.get_multi(self.db,skip=skip,limit=limit)
            result = []
            for t in bugs:
                project = self.db.query(ProjectModel).filter(ProjectModel.id == t.project_id).first()
                project_name = project.name if project else None

                
                assigned = self.db.query(UserModel).filter(UserModel.user_id == t.assignee_id).first()
                assigned_name = assigned.username if assigned else None

                
                reporter = self.db.query(RoleModel).filter(RoleModel.id == t.reporter_id).first()
                reporter_name = reporter.name if reporter else None
                result.append(BugOut(
                            Bug_id=t.id,
                            title=t.title,
                            Description=t.description,
                            
                            reporter_id=t.reporter_id,
                            reporter_name=reporter_name,
                            
                            project_id=t.project_id,
                            project_name=project_name,
                            
                            assigned_id=t.assignee_id,
                            assigned_name=assigned_name,
                            
                            BugStatus_id=t.status_id,
                            Bugstatus_name=t.status.name if t.status else None,
                            
                            priority_id=t.priority_id,
                            priority_name=t.priority.name if t.priority else None,
                            
                            environment_id=t.environment_id,
                            environment_name=t.environment.name if t.environment else None,
                            
                            created_at=t.created_at
                    )    )   

                
      
            return {
                "success": True,
                "message": "Bugs retrieved successfully",
                "data": result,
                "error": None
            }
        except Exception as e:
            raise AppException(
                message="Unexpected error occurred",
                error=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get_bug(self, bug_id: int):
        bug = bug_crud.get(self.db, bug_id)
        if not bug:
            raise AppException(
                message="Bug not found",
                error="Invalid bug ID",
                status_code=status.HTTP_404_NOT_FOUND
            )
        project = self.db.query(ProjectModel).filter(ProjectModel.id == bug.project_id).first()
        project_name = project.name if project else None

            
        assigned = self.db.query(UserModel).filter(UserModel.user_id == bug.assignee_id).first()
        assigned_name = assigned.username if assigned else None

            
        reporter = self.db.query(RoleModel).filter(RoleModel.id == bug.reporter_id).first()
        reporter_name = reporter.name if reporter else None

            
        bug_out = BugOut(
                        Bug_id=bug.id,
                        title=bug.title,
                        Description=bug.description,
                        
                        reporter_id=bug.reporter_id,
                        reporter_name=reporter_name,
                        
                        project_id=bug.project_id,
                        project_name=project_name,
                        
                        assigned_id=bug.assignee_id,
                        assigned_name=assigned_name,
                        
                        BugStatus_id=bug.status_id,
                        Bugstatus_name=bug.status.name if bug.status else None,
                        
                        priority_id=bug.priority_id,
                        priority_name=bug.priority.name if bug.priority else None,
                        
                        environment_id=bug.environment_id,
                        environment_name=bug.environment.name if bug.environment else None,
                        
                        created_at=bug.created_at
                )       

            
        return {
            "success": True,
            "message": "Bug retrieved successfully",
            "data": bug_out,
            "error": None
        }

    def update_bug(self, bug_id: int, bug_in: BugUpdate):
        bug = bug_crud.get(self.db, bug_id)
        if not bug:
            raise AppException(
                message="Bug not found",
                error="Invalid bug ID",
                status_code=status.HTTP_404_NOT_FOUND
            )
        try:
            updated_bug = bug_crud.update(self.db, bug, bug_in)
            project = self.db.query(ProjectModel).filter(ProjectModel.id == updated_bug.project_id).first()
            project_name = project.name if project else None

            
            assigned = self.db.query(UserModel).filter(UserModel.user_id == updated_bug.assignee_id).first()
            assigned_name = assigned.username if assigned else None

                
            reporter = self.db.query(RoleModel).filter(RoleModel.id == updated_bug.reporter_id).first()
            reporter_name = reporter.name if reporter else None

                
            bug_out = BugOut(
                            Bug_id=updated_bug.id,
                            title=updated_bug.title,
                            Description=updated_bug.description,
                            
                            reporter_id=updated_bug.reporter_id,
                            reporter_name=reporter_name,
                            
                            project_id=updated_bug.project_id,
                            project_name=project_name,
                            
                            assigned_id=updated_bug.assignee_id,
                            assigned_name=assigned_name,
                            
                            BugStatus_id=updated_bug.status_id,
                            Bugstatus_name=updated_bug.status.name if updated_bug.status else None,
                            
                            priority_id=updated_bug.priority_id,
                            priority_name=updated_bug.priority.name if updated_bug.priority else None,
                            
                            environment_id=updated_bug.environment_id,
                            environment_name=updated_bug.environment.name if updated_bug.environment else None,
                            
                            created_at=updated_bug.created_at
                    )   
                
            return {
                    "success": True,
                    "message": "Bug updated successfully",
                    "data": bug_out,
                    "error": None
                    }
                
        except Exception as e:
            raise AppException(
                message="Unexpected error occurred",
                error=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete_bug(self, bug_id: int):
        bug = bug_crud.get(self.db, bug_id)
        if not bug:
            raise AppException(
                message="Bug not found",
                error="Invalid bug ID",
                status_code=status.HTTP_404_NOT_FOUND
            )
        try:
            bug_crud.remove(self.db, bug_id)
            return {
                "success": True,
                "message": "Bug deleted successfully",
                "data": None,
                "error": None
            }
        except Exception as e:
            raise AppException(
                message="Unexpected error occurred",
                error=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # ---------------- Bug Status ----------------
    def create_bug_status(self, status_in: BugStatusCreate):
        existing = self.db.query(BugStatusModel).filter(BugStatusModel.name == status_in.name).first()
        if existing:
            raise AppException(f"Status '{existing.name}' already exists", 
                               "Duplicate status",
                               status.HTTP_400_BAD_REQUEST, 
                               data=[])

        db_status = bug_status_crud.create(self.db, status_in)
        return {
                "success": True,
                "message": "Bug status created successfully",
                "data": BugStatusOut.from_orm(db_status),
                "error": None
            }
      

    def get_bug_statuses(self):
        try:
            statuses = bug_status_crud.get_multi(self.db)
            return {
                "success": True,
                "message": "Bug statuses retrieved successfully",
                "data": [BugStatusOut.from_orm(s).dict() for s in statuses],
                "error": None
            }
        except Exception as e:
            raise AppException(message="Unexpected error occurred", error=str(e))

    # ---------------- Bug Priority ----------------
    def create_bug_priority(self, priority_in: BugPriorityCreate):
        existing = self.db.query(BugStatusModel).filter(BugStatusModel.name == priority_in.name).first()
        if existing:
            raise AppException(f"Status '{existing.name}' already exists", 
                               "Duplicate status", 
                               status.HTTP_400_BAD_REQUEST, 
                               data=[])
        
        db_priority = bug_priority_crud.create(self.db, priority_in)
        return {
                "success": True,
                "message": "Bug priority created successfully",
                "data": BugPriorityOut.from_orm(db_priority).dict(),
                "error": None
            }
       
    def get_bug_priorities(self):
        try:
            priorities = bug_priority_crud.get_multi(self.db)
            return {
                "success": True,
                "message": "Bug priorities retrieved successfully",
                "data": [BugPriorityOut.from_orm(p).dict() for p in priorities],
                "error": None
            }
        except Exception as e:
            raise AppException(message="Unexpected error occurred", error=str(e))

    # ---------------- Bug Environment ----------------
    def create_bug_environment(self, env_in: BugEnvironmentCreate):
        existing = self.db.query(BugStatusModel).filter(BugStatusModel.name == env_in.name).first()
        if existing:
            raise AppException(f"Status '{existing.name}' already exists", 
                               "Duplicate status",
                               status.HTTP_400_BAD_REQUEST, 
                               data=[])

        db_env = bug_environment_crud.create(self.db, env_in)
        return {
                "success": True,
                "message": "Bug environment created successfully",
                "data": BugEnvironmentOut.from_orm(db_env).dict(),
                "error": None
            }

    def get_bug_environments(self):
        try:
            envs = bug_environment_crud.get_multi(self.db)
            return {
                "success": True,
                "message": "Bug environments retrieved successfully",
                "data": [BugEnvironmentOut.from_orm(e).dict() for e in envs],
                "error": None
            }
        except Exception as e:
            raise AppException(message="Unexpected error occurred", error=str(e))
