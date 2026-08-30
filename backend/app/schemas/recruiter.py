"""
Phase 1 — Recruiter Schemas
Pydantic v2 style (model_config = ConfigDict(from_attributes=True))
"""

import uuid
from typing import Optional
from pydantic import BaseModel, ConfigDict, HttpUrl


# ─────────────────────────────────────────────────────────────
# RECRUITER PROFILE
# ─────────────────────────────────────────────────────────────

class RecruiterProfileUpdate(BaseModel):
    """Fields a recruiter can update on their profile."""
    company_name: Optional[str] = None
    company_sector: Optional[str] = None
    company_website: Optional[str] = None
    company_description: Optional[str] = None


class RecruiterProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    full_name: str
    email: str
    role: str
    company_name: Optional[str] = None
    company_sector: Optional[str] = None
    company_website: Optional[str] = None
    company_description: Optional[str] = None
    is_verified_company: bool
    is_active: bool


# ─────────────────────────────────────────────────────────────
# SUBMISSION SUMMARY (used inside StudentDetailResponse)
# ─────────────────────────────────────────────────────────────

class SubmissionSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    category: str
    skills: Optional[list[str]] = []
    file_url: Optional[str] = None
    created_at: Optional[str] = None


# ─────────────────────────────────────────────────────────────
# STUDENT LIST ITEM (lightweight — for browse feed)
# ─────────────────────────────────────────────────────────────

class StudentListItem(BaseModel):
    """Lightweight student card shown in browse feed."""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    full_name: str
    email: str
    department: Optional[str] = None
    year: Optional[int] = None
    cgpa: Optional[float] = None
    institution: Optional[str] = None
    verified_achievements: int = 0
    skills: list[str] = []


# ─────────────────────────────────────────────────────────────
# STUDENT DETAIL RESPONSE (full profile for recruiter)
# ─────────────────────────────────────────────────────────────

class StudentDetailResponse(BaseModel):
    """Full student profile shown to recruiter."""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    full_name: str
    email: str
    department: Optional[str] = None
    year: Optional[int] = None
    cgpa: Optional[float] = None
    institution: Optional[str] = None
    skills: list[str] = []
    verified_submissions: list[SubmissionSummary] = []
    is_shortlisted: bool = False


# ─────────────────────────────────────────────────────────────
# SHORTLIST
# ─────────────────────────────────────────────────────────────

class ShortlistCreate(BaseModel):
    student_id: uuid.UUID
    note: Optional[str] = None


class ShortlistResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    recruiter_id: uuid.UUID
    student_id: uuid.UUID
    note: Optional[str] = None
    shortlisted_at: Optional[str] = None
