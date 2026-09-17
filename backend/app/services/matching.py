from sqlalchemy.orm import Session
from app.models.posting import Posting, PostingStatus
from app.services.skill_gap import get_student_skills
import uuid


def score_posting_match(student_skills: list[str], posting: Posting) -> dict:
    """Transparent weighted match score -- pure skill overlap, no black box."""
    required = posting.skills_required or []
    if not required:
        return {
            "posting_id": str(posting.id),
            "posting_title": posting.title,
            "company_name": posting.company_name,
            "match_score": 100.0,
            "matched_skills": [],
            "missing_skills": [],
        }

    student_skills_lower = [s.lower() for s in student_skills]
    matched = [s for s in required if s.lower() in student_skills_lower]
    missing = [s for s in required if s.lower() not in student_skills_lower]

    match_score = round(len(matched) / len(required) * 100, 1)

    return {
        "posting_id": str(posting.id),
        "posting_title": posting.title,
        "company_name": posting.company_name,
        "match_score": match_score,
        "matched_skills": matched,
        "missing_skills": missing,
    }


def get_matched_postings(db: Session, student_id: uuid.UUID, min_score: float = 0) -> list[dict]:
    """All open postings for a student, ranked by skill match score."""
    student_skills = get_student_skills(db, student_id)
    open_postings = db.query(Posting).filter(Posting.status == PostingStatus.open).all()

    results = [score_posting_match(student_skills, p) for p in open_postings]
    results = [r for r in results if r["match_score"] >= min_score]
    results.sort(key=lambda x: x["match_score"], reverse=True)
    return results