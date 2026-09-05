import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Text, Boolean, DateTime, ForeignKey, Enum as SQLEnum
)
from sqlalchemy.orm import relationship
import enum

from app.database import Base
from app.db_types import GUID 


class ApprovalStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class ApplicationStatus(str, enum.Enum):
    applied = "applied"
    shortlisted = "shortlisted"
    selected = "selected"
    rejected = "rejected"


class Company(Base):
    __tablename__ = "companies"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    contact_email = Column(String(255), nullable=False)
    website = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)

    approval_status = Column(
        SQLEnum(ApprovalStatus), default=ApprovalStatus.pending, nullable=False
    )

    created_by_user_id = Column(GUID(), ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    postings = relationship("InternshipPosting", back_populates="company")


class InternshipPosting(Base):
    __tablename__ = "internship_postings"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    company_id = Column(GUID(), ForeignKey("companies.id"), nullable=False)

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String(255), nullable=True)
    is_remote = Column(Boolean, default=False)

    stipend = Column(String(100), nullable=True)  
    duration = Column(String(100), nullable=True)  # e.g. "3 months"

    deadline = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)  # deadline chole gele False kore dite paro

    posted_by_user_id = Column(GUID(), ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    company = relationship("Company", back_populates="postings")
    applications = relationship("Application", back_populates="posting")


class Application(Base):
    __tablename__ = "applications"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    posting_id = Column(GUID(), ForeignKey("internship_postings.id"), nullable=False)
    student_id = Column(GUID(), ForeignKey("users.id"), nullable=False)

    status = Column(
        SQLEnum(ApplicationStatus), default=ApplicationStatus.applied, nullable=False
    )

    cover_note = Column(Text, nullable=True)
    resume_url = Column(String(500), nullable=True)  # jodi file upload thake

    applied_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    posting = relationship("InternshipPosting", back_populates="applications")
    student = relationship("User")
