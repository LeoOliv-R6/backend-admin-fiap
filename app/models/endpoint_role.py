from sqlalchemy import Integer, Column, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base
from .role import Role
from .endpoint import Endpoint


class EndpointRole(Base):
    __tablename__ = "endpoint_role"

    endpoint_id = Column(Integer, ForeignKey(Endpoint.id), primary_key=True)
    endpoint = relationship(Endpoint)
    role_id = Column(Integer, ForeignKey(Role.id), primary_key=True)
    role = relationship(Role)
    is_active = Column(Boolean, default=True)
    created = Column(DateTime, index=True, default=datetime.utcnow())