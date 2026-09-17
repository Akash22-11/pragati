from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import get_db
from app.dependencies.auth import get_current_user, require_role
from app.models.user import User, UserRole
from app.services.skill_gap import get_posting_gap, get_institutional_gap
from app.services.matching import get_matched_postings

router = APIRouter(prefix="/skill-gap", tags=["Skill Gap"])


@router.get("/posting/{posting_id}")
def posting_skill_gap(
    posting_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """A student's own skill match against one posting's requirements."""
    result = get_posting_gap(db, current_user.id, posting_id)
    if not result:
        raise HTTPException(status_code=404, detail="Posting not found")
    return result


@router.get("/institutional")
def institutional_skill_gap(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.faculty, UserRole.admin)),
):
    """Institution-wide demand vs availability, sorted by biggest gap first."""
    return get_institutional_gap(db)

@router.get("/matches")
def my_matched_postings(
    min_score: float = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.student)),
):
    """Open postings ranked by skill match score, highest first."""
    return get_matched_postings(db, current_user.id, min_score)        