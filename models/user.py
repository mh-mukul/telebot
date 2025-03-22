from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean

from config.database import Base


class TelegramUser(Base):
    __tablename__ = 'telegram_users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    username = Column(String(100), nullable=True)
    mobile = Column(String(15), nullable=False, unique=True)
    chat_id = Column(String(100), nullable=False, unique=True)
    is_active = Column(Boolean(), nullable=False, default=True)
    is_deleted = Column(Boolean(), nullable=False, default=False)
    is_superuser = Column(Boolean(), nullable=False, default=False)
    created_at = Column(DateTime(6), default=datetime.now)
    updated_at = Column(DateTime(6), default=datetime.now)

    def soft_delete(self):
        self.is_active = False
        self.is_deleted = True
        self.updated_at = datetime.now()

    def __repr__(self):
        return f"{self.mobile}"