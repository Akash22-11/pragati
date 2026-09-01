"""
Phase 2 -- Internship & Placement Posting Schemas
"""

import uuid
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


# -----------------------------------------------------------------
# Postings
# -----------------------------------------------------------------

class PostingCreate(BaseModel):
    title: str
    description: Optional[str] = None
    type: str = "internship"  # "internship" | "job"
    location: Optional[str] = None
    stipend: Optional[str] = None
    positions: Optional[int] = 1
    skills_required: Optional[list[str]] = []
    deadline: Optional[datetime] = None


class PostingUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    location: Optional[str] = None
    stipend: Optional[str] = None
    positions: Optional[int] = None
    skills_required: Optional[list[str]] = None
    deadline: Optional[datetime] = None
    status: Optional[str] = None  # "open" | "closed"


class PostingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    recruiter_id: uuid.UUID
    company_name: Optional[str] = None
    title: str
    description: Optional[str] = None
    type: str
    location: Optional[str] = None
    stipend: Optional[str] = None
    positions: Optional[int] = None
    skills_required: list[str] = []
    deadline: Optional[datetime] = None
    status: str
    is_open: bool
    applications_count: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# -----------------------------------------------------------------
# Applications
# -----------------------------------------------------------------

class ApplicationCreate(BaseModel):
    cover_note: Optional[str] = None


class ApplicationStatusUpdate(BaseModel):
    status: str  # "shortlisted" | "selected" | "rejected" | "applied"


class ApplicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    posting_id: uuid.UUID
    student_id: uuid.UUID
    status: str
    cover_note: Optional[str] = None
    applied_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ApplicationWithStudent(ApplicationResponse):
    """Recruiter-facing view: who applied to one of my postings."""
    student_name: Optional[str] = None
    student_email: Optional[str] = None


class ApplicationWithPosting(ApplicationResponse):
    """Student-facing view: status of my own applications."""
    posting_title: Optional[str] = None
    company_name: Optional[str] = None
