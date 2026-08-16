from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from app.models.submission import SubmissionStatus, SubmissionCategory
from app.models.verification import VerificationAction

class SubmissionCreate(BaseModel):
    title: str
    description: str | None = None
    category: SubmissionCategory

class SubmissionResponse(BaseModel):
    id: UUID
    student_id: UUID
    title: str
    description: str | None
    category: SubmissionCategory
    status: SubmissionStatus
    file_url: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class VerifyRequest(BaseModel):
    action: VerificationAction
    note: str | None = None