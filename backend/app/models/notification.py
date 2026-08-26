from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Text
from app.db_types import GUID
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import uuid


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.id"), nullable=False)
    type = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="notifications")