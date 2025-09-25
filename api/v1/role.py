from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from configurations.database import get_db
from schemas.role import RoleCreate, Role
from service.role_service import RoleService
from utils.response import AppException

router = APIRouter(
    prefix="/roles",
    tags=["Roles"]
)

# Dependency to get RoleService
def get_service(db: Session = Depends(get_db)):
    return RoleService(db)

# Create Role
@router.post("/")
def create_role(role_in: RoleCreate, service: RoleService = Depends(get_service)):
    try:
        return service.create_role(role_in)
    except AppException as e:
        # Already formatted response from AppException
        return e.detail

# List Roles
@router.get("/")
def list_roles(service: RoleService = Depends(get_service)):
    try:
        return service.get_roles()
    except AppException as e:
        return e.detail




















# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from configurations.database import get_db
# import crud.role as role_crud
# import schemas.role as role_schema

# router = APIRouter(
#     prefix="/roles",
#     tags=["Roles"]
# )

# @router.post("/", response_model=role_schema.Role)
# def create_role(role: role_schema.RoleCreate, db: Session = Depends(get_db)):
#     return role_crud.create_role(db=db, role=role)

# @router.get("/", response_model=list[role_schema.Role])
# def list_roles(db: Session = Depends(get_db)):
#     return role_crud.get_roles(db=db)
