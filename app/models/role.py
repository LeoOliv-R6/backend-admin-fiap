from sqlalchemy import Integer, String, Column, Boolean, DateTime
from datetime import datetime
from app.db.base_class import Base


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    level = Column(Integer, nullable=False)
    description = Column(String(256), nullable=False)
    is_active = Column(Boolean, default=True)
    created = Column(DateTime, index=True, default=datetime.utcnow())