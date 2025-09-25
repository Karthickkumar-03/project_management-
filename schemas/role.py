from pydantic import BaseModel

class RoleBase(BaseModel):
    name: str
    class Config:
        from_attributes = True

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    id: int

    class Config:
       from_attributes = True
