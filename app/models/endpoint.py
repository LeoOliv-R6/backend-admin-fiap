from sqlalchemy import Integer, String, Column, Boolean, DateTime
from datetime import datetime
from app.db.base_class import Base


class Endpoint(Base):
    __tablename__ = "endpoint"

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    url = Column(String(256), nullable=False)
    description = Column(String(256), nullable=False)
    is_active = Column(Boolean, default=True)
    created = Column(DateTime, index=True, default=datetime.utcnow())