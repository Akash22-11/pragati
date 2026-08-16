from sqlalchemy import Column, String, DateTime, Enum, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import uuid
import enum

class SubmissionStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    returned = "returned"

class SubmissionCategory(str, enum.Enum):
    certification = "certification"
    internship = "internship"
    project = "project"
    competition = "competition"
    research = "research"
    extracurricular = "extracurricular"
    other = "other"

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(Enum(SubmissionCategory), nullable=False)
    status = Column(Enum(SubmissionStatus), default=SubmissionStatus.pending)
    file_url = Column(String, nullable=True)  # Cloudinary/S3 URL
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    student = relationship("User", back_populates="submissions")
    verification = relationship("Verification", back_populates="submission", uselist=False)