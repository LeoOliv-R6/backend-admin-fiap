from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


class AdministratorBase(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    document: Optional[str] = None
    role_id: Optional[int] = None
    is_active: Optional[bool] = True
    created: Optional[datetime] = None


class AdministratorCreate(AdministratorBase):
    name: str
    email: EmailStr
    password: str
    document: str
    role_id: int


class AdministratorUpdate(AdministratorBase):
    password: Optional[str] = None


class AdministratorInDBBase(AdministratorBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class Administrator(AdministratorInDBBase):
    pass


class AdministratorInDB(AdministratorInDBBase):
    hashed_password: Optional[str] = None