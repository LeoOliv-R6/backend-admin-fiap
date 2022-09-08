from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class EndpointBase(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = True
    created: Optional[datetime] = None


class EndpointCreate(EndpointBase):
    name: str
    url: str


class EndpointUpdate(EndpointBase):
    pass


class EndpointInDBBase(EndpointBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class Endpoint(EndpointInDBBase):
    pass


class EndpointInDB(EndpointInDBBase):
    pass