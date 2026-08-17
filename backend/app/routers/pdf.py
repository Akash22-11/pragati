from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.services.profile import get_full_profile
from app.services.pdf import generate_portfolio_pdf

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