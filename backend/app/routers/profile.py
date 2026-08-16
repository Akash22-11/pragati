from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.services.profile import get_full_profile

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.get("/{student_id}")
def get_profile(
    student_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    data = get_full_profile(db, student_id)
    student = data["student"]
    profile = data["profile"]
    submissions = data["verified_submissions"]

    return {
        "student": {
            "id": str(student.id),
            "full_name": student.full_name,
            "email": student.email,
            "institution": student.institution,
            "department": student.department,
        },
        "profile": {
            "bio": profile.bio,
            "qr_token": profile.qr_token,
            "qr_code_url": profile.qr_code_url,
            "pdf_url": profile.pdf_url,
        },
        "verified_submissions": [
            {
                "id": str(s.id),
                "title": s.title,
                "category": s.category,
                "status": s.status,
                "file_url": s.file_url,
                "created_at": str(s.created_at),
            }
            for s in submissions
        ],
    }