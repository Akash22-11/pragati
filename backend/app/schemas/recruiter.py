"""
Phase 1 -- Recruiter Schemas
Pydantic v2 style. Matches the ACTUAL users table schema
(no `year` or `roll_number` columns exist).
"""

import uuid
from typing import Optional
from pydantic import BaseModel, ConfigDict


class RecruiterProfileUpdate(BaseModel):
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


class SubmissionSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    category: str
    skills: Optional[list[str]] = []
    file_url: Optional[str] = None
    created_at: Optional[str] = None


class StudentListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    full_name: str
    email: str
    department: Optional[str] = None
    cgpa: Optional[float] = None
    institution: Optional[str] = None
    verified_achievements: int = 0
    skills: list[str] = []


class StudentDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    full_name: str
    email: str
    department: Optional[str] = None
    cgpa: Optional[float] = None
    institution: Optional[str] = None
    skills: list[str] = []
    verified_submissions: list[SubmissionSummary] = []
    is_shortlisted: bool = False


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
