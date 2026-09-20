from sqlalchemy.orm import Session
from app.models.submission import Submission, SubmissionStatus
from app.models.posting import Posting, PostingStatus
from app.models.user import User
import uuid


def get_student_skills(db: Session, student_id: uuid.UUID) -> list[str]:
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
