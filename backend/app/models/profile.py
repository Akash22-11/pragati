from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from app.db_types import GUID
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import uuid


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    student_id = Column(GUID(), ForeignKey("users.id"), unique=True, nullable=False)
    bio = Column(Text, nullable=True)
    qr_token = Column(String, unique=True, nullable=True)
    qr_code_url = Column(String, nullable=True)
    pdf_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = relationship("User", backref="profile")