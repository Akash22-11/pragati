from sqlalchemy import (
    Column, DateTime, Enum, ForeignKey, Text, UniqueConstraint
)
from sqlalchemy.orm import relationship
from app.db_types import GUID
from app.database import Base
from datetime import datetime
import uuid
import enum


class ApplicationStatus(str, enum.Enum):
    applied = "applied"
    shortlisted = "shortlisted"
    selected = "selected"
    rejected = "rejected"


class Application(Base):
    
    __tablename__ = "applications"

    
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)

    posting_id = Column(GUID(), ForeignKey("postings.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id = Column(GUID(), ForeignKey("users.id"), nullable=False, index=True)

    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.applied, nullable=False)
    cover_note = Column(Text, nullable=True)

    applied_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("posting_id", "student_id", name="uq_posting_student"),
    )

    posting = relationship("Posting", back_populates="applications")
    student = relationship("User", foreign_keys=[student_id])

    @property
    def student_name(self):
        return self.student.full_name if self.student else None

    @property
    def student_email(self):
        return self.student.email if self.student else None

    @property
    def posting_title(self):
        return self.posting.title if self.posting else None

    @property
    def company_name(self):
        return self.posting.company_name if self.posting else None
