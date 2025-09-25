
from sqlalchemy.orm import Session
from fastapi import status
from models.user.user import User as UserModel, Role as RoleModel
from schemas.user import UserCreate, UserUpdate, UserOut
from utils.response import AppException
from crud.base import CRUDBase
from utils.pagination import BaseRepository

user_crud = CRUDBase(UserModel)

class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = BaseRepository(UserModel)
    # Helper: Map user to UserOut with role_name
    def map_user(self, user: UserModel) -> UserOut:
        role_name = None
        if user.role_id:
            role = self.db.query(RoleModel).filter(RoleModel.id == user.role_id).first()
            if role:
                role_name = role.name
        return UserOut(
            user_id=user.user_id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            role_id=user.role_id,
            role_name=role_name
        )
    # Create user
    def create_user(self, user_in: UserCreate):
        existing = self.db.query(UserModel).filter(UserModel.email == user_in.email).first()
        if existing:
            raise AppException(
                message="Email already exists",
                error="Duplicate email",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        try:
            db_user = user_crud.create(self.db, user_in)
            return {
                "success": True,
                "message": "User created successfully",
                "data": self.map_user(db_user).dict(),
                "error": None
            }
        except Exception as e:
            raise AppException(
                message="Unexpected error occurred",
                error=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    # List users
    def get_users(self):
        try:
            users = user_crud.get_multi(self.db)
            return {
                "success": True,
                "message": "Users retrieved successfully",
                "data": [self.map_user(u).dict() for u in users],
                "error": None
            }
        except Exception as e:
            raise AppException(
                message="Unexpected error occurred",
                error=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    # Get user by ID
    def get_user_by_id(self, user_id: int):
        user = user_crud.get(self.db, user_id)
        if not user:
            raise AppException(
                message="User not found",
                error="Invalid user ID",
                status_code=status.HTTP_404_NOT_FOUND
            )
        return {
            "success": True,
            "message": "User retrieved successfully",
            "data": self.map_user(user).dict(),
            "error": None
        }

    # Update user
    def update_user(self, user_id: int, user_in: UserUpdate):
        user = user_crud.get(self.db, user_id)
        if not user:
            raise AppException(
                message="User not found",
                error="Invalid user ID",
                status_code=status.HTTP_404_NOT_FOUND
            )

        if user_in.email and self.db.query(UserModel).filter(
            UserModel.email == user_in.email, UserModel.user_id != user_id
        ).first():
            raise AppException(
                message="Email already exists",
                error="Duplicate email",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        try:
            updated_user = user_crud.update(self.db, user, user_in)
            return {
                "success": True,
                "message": "User updated successfully",
                "data": self.map_user(updated_user).dict(),
                "error": None
            }
        except Exception as e:
            raise AppException(
                message="Unexpected error occurred",
                error=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    # Delete user
    def delete_user(self, user_id: int):
        user = user_crud.get(self.db, user_id)
        if not user:
            raise AppException(
                message="User not found",
                error="Invalid user ID",
                status_code=status.HTTP_404_NOT_FOUND
            )
        try:
            user_crud.remove(self.db, user.user_id)
            return {
                "success": True,
                "message": "User deleted successfully",
                "data": None,
                "error": None
            }
        except Exception as e:
            raise AppException(
                message="Unexpected error occurred",
                error=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
 