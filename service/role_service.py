from sqlalchemy.orm import Session
from fastapi import status
from models.user.user import Role as RoleModel
from schemas.role import RoleCreate, Role as RoleSchema
from utils.response import AppException
from crud.base import CRUDBase

# Initialize generic CRUD
role_crud = CRUDBase(RoleModel)

class RoleService:
    def __init__(self, db: Session):
        self.db = db

    # Create Role
    def create_role(self, role_in: RoleCreate):
        existing = self.db.query(RoleModel).filter(RoleModel.name == role_in.name).first()
        if existing:
            raise AppException(
                message=f"Role '{existing.name}' already exists",
                error="Duplicate role",
                status_code=status.HTTP_400_BAD_REQUEST,
                data=[]
            )
        try:
            db_role = role_crud.create(self.db, role_in)
            return {
                "success": True,
                "message": "Role created successfully",
                "data": RoleSchema.from_orm(db_role).dict(),
                "error": None
            }
        except Exception as e:
            raise AppException(
                message="Unexpected error occurred",
                error=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # List Roles
    def get_roles(self):
        try:
            roles = role_crud.get_multi(self.db)
            return {
                "success": True,
                "message": "Roles retrieved successfully",
                "data": [RoleSchema.from_orm(r).dict() for r in roles],
                "error": None
            }
        except Exception as e:
            raise AppException(
                message="Unexpected error occurred",
                error=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
