from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.services.profile import get_full_profile
from app.services.pdf import generate_portfolio_pdf
from app.services.resume import draft_resume_data, generate_resume_pdf

router = APIRouter(prefix="/profile", tags=["PDF"])


@router.get("/{student_id}/pdf")
def download_portfolio_pdf(
    student_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    data = get_full_profile(db, student_id)
    student = data["student"]
    submissions = data["verified_submissions"]

    student_dict = {
        "full_name": student.full_name,
        "email": student.email,
        "institution": student.institution,
        "department": student.department,
    }

    submissions_list = [
        {
            "title": s.title,
            "category": s.category,
            "status": s.status,
            "created_at": str(s.created_at),
        }
        for s in submissions
    ]

    pdf_bytes = generate_portfolio_pdf(
        student=student_dict,
        profile={},
        submissions=submissions_list,
    )

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=portfolio_{student_id}.pdf"
        },
       )


@router.get("/{student_id}/resume-preview")
def download_resume_preview(
    student_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Auto-drafted resume from the student's own verified Pragati data.
    Student reviews and edits before it's ever attached to an application --
    nothing here is collected without their knowledge or sent anywhere
    without an explicit confirm step on the frontend."""

    if current_user.id != student_id and current_user.role.value == "student":
        raise HTTPException(status_code=403, detail="You can only preview your own resume")

    data = draft_resume_data(db, student_id)
    if not data:
        raise HTTPException(status_code=404, detail="Student not found")

    pdf_bytes = generate_resume_pdf(data)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "inline; filename=resume_draft.pdf"},
    )