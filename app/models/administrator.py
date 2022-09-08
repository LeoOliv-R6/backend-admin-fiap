from sqlalchemy import Integer, String, Column, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base
from .role import Role


class Administrator(Base):
    __tablename__ = "administrator"

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    email = Column(String(256), index=True, unique=True)
    hashed_password = Column(String(256), nullable=False)
    document = Column(String(14), nullable=False)
    role_id = Column(Integer, ForeignKey(Role.id), nullable=False)
    role = relationship(Role)
    is_active = Column(Boolean, default=True)
    created = Column(DateTime, index=True, default=datetime.utcnow())