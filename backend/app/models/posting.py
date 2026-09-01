from sqlalchemy import Column, String, DateTime, Enum, ForeignKey, Text, JSON, Integer
from sqlalchemy.orm import relationship
from app.db_types import GUID
from app.database import Base
from datetime import datetime
import uuid
import enum


class PostingType(str, enum.Enum):
    internship = "internship"
    job = "job"


class PostingStatus(str, enum.Enum):
    open = "open"
    closed = "closed"


class Posting(Base):
    """
    Phase 2 -- Internship & Placement Posting
    A verified recruiter (company) posts an internship/job opening.
    Students browse open postings and apply; applications are tracked
    separately in the Application model.
    """
    __tablename__ = "postings"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    recruiter_id = Column(GUID(), ForeignKey("users.id"), nullable=False, index=True)

    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    type = Column(Enum(PostingType), nullable=False, default=PostingType.internship)

    location = Column(String, nullable=True)
    stipend = Column(String, nullable=True)  # free text, e.g. "₹15,000/month" or "12 LPA"
    positions = Column(Integer, nullable=True, default=1)

    # JSON array of strings, e.g. ["Python", "React"] -- mirrors Submission.skills
    skills_required = Column(JSON, nullable=True, default=list)

    deadline = Column(DateTime, nullable=True)
    status = Column(Enum(PostingStatus), default=PostingStatus.open, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    recruiter = relationship("User", foreign_keys=[recruiter_id])
    applications = relationship(
        "Application", back_populates="posting", cascade="all, delete-orphan"
    )

    @property
    def company_name(self):
        if not self.recruiter:
            return None
        return self.recruiter.company_name or self.recruiter.full_name

    @property
    def is_open(self):
        if self.status != PostingStatus.open:
            return False
        if self.deadline and self.deadline < datetime.utcnow():
            return False
        return True

    @property
    def applications_count(self):
        return len(self.applications) if self.applications is not None else 0
