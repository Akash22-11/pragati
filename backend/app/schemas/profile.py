from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from app.schemas.submission import SubmissionResponse

class ProfileResponse(BaseModel):
    id: UUID
    student_id: UUID
    bio: str | None
    qr_token: str | None
    qr_code_url: str | None
    pdf_url: str | None
    created_at: datetime
    updated_at: datetime
    submissions: list[SubmissionResponse] = []

    class Config:
        from_attributes = True