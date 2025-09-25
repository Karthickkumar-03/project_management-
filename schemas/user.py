from pydantic import BaseModel,EmailStr
from .role import RoleBase
from typing import Optional
class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: bool = True
    role_id: int
   

class UserCreate(UserBase):
    hashed_password: str

class UserUpdate(BaseModel):
    username: Optional[str] | None = None
    email: Optional[EmailStr] | None = None
    is_active: Optional[bool] | None = None
    role_id: Optional[int] | None = None
class UserOut(BaseModel):
    user_id: int
    username: str
    email: str
    is_active: bool
    role_id: int
    role_name: Optional[str] = None  # flat field

    class Config:
        orm_mode = True
class User(UserBase):
    user_id: int
    role_name:Optional[str]
    class Config:
        from_attributes = True










































