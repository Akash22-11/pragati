from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import get_db
from app.dependencies.auth import get_current_user, require_role
from app.models.user import User, UserRole
from app.models.submission import SubmissionStatus
from app.schemas.submission import SubmissionResponse, VerifyRequest
from app.services.submission import get_submissions_by_status, verify_submission

router = APIRouter(prefix="/submissions", tags=["Submissions"])

@router.get("/", response_model=list[SubmissionResponse])
def list_submissions(
    status: SubmissionStatus = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_submissions_by_status(db, status)

@router.patch("/{submission_id}/verify", response_model=dict)
def verify(
    submission_id: UUID,
    payload: VerifyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(UserRole.faculty, UserRole.admin)
    ),
):
    verification = verify_submission(
        db=db,
        submission_id=submission_id,
        verifier=current_user,
        action=payload.action,
        note=payload.note,
    )
    return {
        "message": f"Submission {payload.action} successfully",
        "verification_id": str(verification.id),
        "hash": verification.hash,
    }