from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from configurations.database import get_db
from schemas.user import UserCreate, UserUpdate, User
from schemas.response import ResponseModel
from service.user_service import UserService
from utils.response import AppException
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# Dependency to get service
def get_service(db: Session = Depends(get_db)):
    try:
        return UserService(db)
    except AppException as e:
        # Already formatted response from AppException
        return e.detail

# Create User
@router.post("/", response_model=ResponseModel[User])
def create_user(user_in: UserCreate, service: UserService = Depends(get_service)):
    try:
        return service.create_user(user_in)
    except AppException as e:
        # Already formatted response from AppException
        return e.detail

# List Users
@router.get("/", response_model=ResponseModel[list[User]])
def list_users(service: UserService = Depends(get_service)):
    try:
        return service.get_users()
    except AppException as e:
        # Already formatted response from AppException
        return e.detail

# Get single User
@router.get("/{user_id}", response_model=ResponseModel[User])
def get_user(user_id: int, service: UserService = Depends(get_service)):
    try:
        return service.get_user_by_id(user_id)
    except AppException as e:
        # Already formatted response from AppException
        return e.detail

# Update User
@router.put("/{user_id}", response_model=ResponseModel[User])
def update_user(user_id: int, user_in: UserUpdate, service: UserService = Depends(get_service)):
    try:
        return service.update_user(user_id, user_in)
    except AppException as e:
        # Already formatted response from AppException
        return e.detail

# Delete User
@router.delete("/{user_id}", response_model=ResponseModel[None])
def delete_user(user_id: int, service: UserService = Depends(get_service)):
    try:
        return service.delete_user(user_id)
    except AppException as e:
        # Already formatted response from AppException
        return e.detail
