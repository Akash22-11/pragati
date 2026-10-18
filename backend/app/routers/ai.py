import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.submission import Submission
from app.models.user import User, UserRole
from app.schemas.ai import AnalyzeRequest, AnalyzeResponse
from app.config import settings
from app.services.ai_analyzer import AIAnalysisError, analyze_achievement

logger = logging.getLogger("pragati.ai")
router = APIRouter(prefix="/ai", tags=["Pragati AI"])


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(
    payload: AnalyzeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Analyze one achievement with the open-weight model.

    Students may analyze their own submissions or free text; faculty/admin may analyze
    any submission. Recruiters are not allowed.
    """
    if current_user.role == UserRole.recruiter:
        raise HTTPException(status_code=403, detail="You do not have permission to perform this action")

    submission = None
    if payload.achievement_id:
        submission = db.query(Submission).filter(Submission.id == payload.achievement_id).first()
        if not submission:
            raise HTTPException(status_code=404, detail="Achievement not found")
        if current_user.role == UserRole.student and submission.student_id != current_user.id:
            # Same response as "missing" so IDs of other students' work are not discoverable.
            raise HTTPException(status_code=404, detail="Achievement not found")
        args = dict(
            title=submission.title,
            description=submission.description,
            category=submission.category.value if submission.category else None,
            existing_skills=submission.skills or [],
        )
    else:
        args = dict(title=None, description=payload.achievement)

    try:
        analysis = analyze_achievement(**args)
    except AIAnalysisError:
        logger.exception("Pragati AI analysis failed")
        raise HTTPException(status_code=502, detail="AI analysis failed. Please try again.")

    return AnalyzeResponse(
        **analysis.model_dump(),
        model=settings.AI_MODEL,
        achievement_id=submission.id if submission else None,
        verification_status=submission.status.value if submission and submission.status else None,
    )
