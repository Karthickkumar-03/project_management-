from crud.base import CRUDBase
from models.user.user import User
from schemas.user import UserCreate, UserUpdate

user_crud = CRUDBase[User, UserCreate, UserUpdate](User)
