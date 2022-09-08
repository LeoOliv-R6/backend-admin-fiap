from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class RoleBase(BaseModel):
    name: Optional[str] = None
    level: Optional[int] = None
    description: Optional[str] = None
    is_active: Optional[bool] = True
    created: Optional[datetime] = None


class RoleCreate(RoleBase):
    name: str
    level: int


class RoleUpdate(RoleBase):
    pass


class RoleInDBBase(RoleBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class Role(RoleInDBBase):
    pass


class RoleInDB(RoleInDBBase):
    pass