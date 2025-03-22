from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean

from config.database import Base


class ApiKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    valid_until = Column(DateTime(6), nullable=True)
    created_at = Column(DateTime(6), default=datetime.now)
    updated_at = Column(DateTime(6), default=datetime.now)

    def __repr__(self):
        return f"{self.id}"
