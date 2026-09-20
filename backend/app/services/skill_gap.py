from sqlalchemy.orm import Session
from app.models.submission import Submission, SubmissionStatus
from app.models.posting import Posting, PostingStatus
from app.models.user import User
from datetime import datetime
import uuid


def get_student_skills(db: Session, student_id: uuid.UUID) -> list[str]:
    """All skills from a student's verified (approved) submissions, deduped."""
    submissions = db.query(Submission).filter(
        Submission.student_id == student_id,
        Submission.status == SubmissionStatus.approved,
    ).all()

    skills = []
    for s in submissions:
        if s.skills:
            for skill in s.skills:
                if skill not in skills:
                    skills.append(skill)
    return skills


def get_posting_gap(db: Session, student_id: uuid.UUID, posting_id: uuid.UUID) -> dict:
    """Compare a student's verified skills against one posting's required skills."""
    posting = db.query(Posting).filter(Posting.id == posting_id).first()
    if not posting:
        return None

    student_skills = get_student_skills(db, student_id)
    student_skills_lower = [s.lower() for s in student_skills]

    required = posting.skills_required or []
    matched = [s for s in required if s.lower() in student_skills_lower]
    missing = [s for s in required if s.lower() not in student_skills_lower]

    match_pct = round((len(matched) / len(required) * 100), 1) if required else 100.0

    return {
        "posting_id": str(posting_id),
        "posting_title": posting.title,
        "required_skills": required,
        "matched_skills": matched,
        "missing_skills": missing,
        "match_percentage": match_pct,
    }


def get_institutional_gap(db: Session) -> list[dict]:
    """Across all open postings, which required skills are most often
    missing from verified student profiles institution-wide."""
    open_postings = db.query(Posting).filter(Posting.status == PostingStatus.open).all()
    students = db.query(User).filter(User.role == "student").all()

    demand_count = {}
    for p in open_postings:
        for skill in (p.skills_required or []):
            demand_count[skill] = demand_count.get(skill, 0) + 1

    availability_count = {}
    for student in students:
        student_skills = get_student_skills(db, student.id)
        for skill in student_skills:
            availability_count[skill] = availability_count.get(skill, 0) + 1

    total_students = len(students) or 1
    total_postings = len(open_postings) or 1

    result = []
    for skill, demand in demand_count.items():
        availability = availability_count.get(skill, 0)
        demand_pct = round(demand / total_postings * 100, 1)
        availability_pct = round(availability / total_students * 100, 1)
        gap = round(demand_pct - availability_pct, 1)
        result.append({
            "skill": skill,
            "demand_pct": demand_pct,
            "availability_pct": availability_pct,
            "gap": gap,
        })

    result.sort(key=lambda x: x["gap"], reverse=True)
    return result


def get_demand_over_time(db: Session) -> dict:
    """Honest demand snapshot -- how many postings requiring each skill
    were created, grouped by month. No prediction, just real history."""
    postings = db.query(Posting).order_by(Posting.created_at).all()

    monthly_skill_counts = {}
    for p in postings:
        if not p.created_at or not p.skills_required:
            continue
        month_key = p.created_at.strftime("%Y-%m")
        if month_key not in monthly_skill_counts:
            monthly_skill_counts[month_key] = {}
        for skill in p.skills_required:
            monthly_skill_counts[month_key][skill] = monthly_skill_counts[month_key].get(skill, 0) + 1

    months = sorted(monthly_skill_counts.keys())
    all_skills = set()
    for month_data in monthly_skill_counts.values():
        all_skills.update(month_data.keys())

    series = {}
    for skill in all_skills:
        series[skill] = [monthly_skill_counts[m].get(skill, 0) for m in months]

    return {
        "months": months,
        "series": series,
        "note": "Real posting counts over time, not a prediction. Trends become meaningful as more postings accumulate.",
    }