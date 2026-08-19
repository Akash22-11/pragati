from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.profile import Profile
from app.services.qr import generate_student_qr

router = APIRouter(tags=["QR"])


@router.post("/profile/{student_id}/qr")
def create_qr_code(
    student_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Generate (or regenerate) a student's QR code."""
    profile = generate_student_qr(db, student_id)
    return {
        "message": "QR code generated successfully",
        "qr_token": profile.qr_token,
        "qr_code_url": profile.qr_code_url,
    }


@router.get("/verify/{token}")
def verify_by_token(token: str, db: Session = Depends(get_db)):
    """Public endpoint — no auth needed. Anyone can scan and verify."""
    profile = db.query(Profile).filter(Profile.qr_token == token).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Invalid or expired QR token")

    student = profile.student
    from app.models.submission import Submission, SubmissionStatus
    verified_submissions = db.query(Submission).filter(
        Submission.student_id == profile.student_id,
        Submission.status == SubmissionStatus.approved,
    ).all()

    return {
        "student": {
            "full_name": student.full_name,
            "institution": student.institution,
            "department": student.department,
        },
        "verified_submissions": [
            {
                "title": s.title,
                "category": s.category,
                "created_at": str(s.created_at),
            }
            for s in verified_submissions
        ],
        "verified_count": len(verified_submissions),
    }