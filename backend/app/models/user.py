from sqlalchemy import Column, String, Boolean, DateTime, Enum
from app.db_types import GUID
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import uuid
import enum


class UserRole(str, enum.Enum):
    student = "student"
    faculty = "faculty"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.student, nullable=False)
    institution = Column(String, nullable=True)
    department = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    reset_token_hash = Column(String, nullable=True)
    reset_token_expires = Column(DateTime, nullable=True)

    submissions = relationship("Submission", back_populates="student")
    notifications = relationship("Notification", back_populates="user")