from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


class EndpointRoleBase(BaseModel):
    endpoint_id: Optional[int] = None
    role_id: Optional[int] = None
    is_active: Optional[bool] = True
    created: Optional[datetime] = None


class EndpointRoleCreate(EndpointRoleBase):
    endpoint_id: int
    role_id: int


class EndpointRoleUpdate(EndpointRoleBase):
    pass


class EndpointRoleMulti(BaseModel):
    endpoint_id: List[int]
    role_id: int


class EndpointRoleInDBBase(EndpointRoleBase):
    class Config:
        orm_mode = True


class EndpointRole(EndpointRoleInDBBase):
    pass


class EndpointRoleInDB(EndpointRoleInDBBase):
    pass