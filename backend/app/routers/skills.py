"""
Phase 1 — Skills Router
Handles:
  - Skill suggestions per submission category
  - All unique skills from approved submissions (for recruiter filters)
"""

from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.submission import Submission, SubmissionStatus, CATEGORY_SKILL_SUGGESTIONS

router = APIRouter()


@router.get("/suggestions")
def get_skill_suggestions(
    category: Optional[str] = Query(None, description="Submission category"),
    current_user: User = Depends(get_current_user),
):
    """
    Returns skill tag suggestions.
    If category is provided, returns category-specific suggestions.
    Used by frontend when student is tagging a submission.
    """
    if category and category in CATEGORY_SKILL_SUGGESTIONS:
        return {
            "category": category,
            "suggestions": CATEGORY_SKILL_SUGGESTIONS[category]
        }

    # Return all suggestions grouped by category
    return {"suggestions": CATEGORY_SKILL_SUGGESTIONS}


@router.get("/all")
def get_all_skills(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Returns all unique skill tags from approved submissions.
    Used by recruiter filter dropdown.
    """
    approved_subs = db.query(Submission).filter(
        Submission.status == SubmissionStatus.approved,
        Submission.skills.isnot(None)
    ).all()

    all_skills = set()
    for sub in approved_subs:
        if sub.skills:
            for skill in sub.skills:
                all_skills.add(skill.strip())

    return {
        "skills": sorted(list(all_skills)),
        "total": len(all_skills)
    }
