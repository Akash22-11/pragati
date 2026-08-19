from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.submission import Submission, SubmissionStatus, SubmissionCategory
from app.models.user import User, UserRole


def get_stats(db: Session) -> dict:
    """Overall platform statistics."""
    total_students = db.query(User).filter(User.role == UserRole.student).count()
    total_submissions = db.query(Submission).count()
    total_verified = db.query(Submission).filter(
        Submission.status == SubmissionStatus.approved
    ).count()
    total_pending = db.query(Submission).filter(
        Submission.status == SubmissionStatus.pending
    ).count()
    total_rejected = db.query(Submission).filter(
        Submission.status == SubmissionStatus.rejected
    ).count()

    return {
        "total_students": total_students,
        "total_submissions": total_submissions,
        "total_verified": total_verified,
        "total_pending": total_pending,
        "total_rejected": total_rejected,
        "verification_rate": round(
            (total_verified / total_submissions * 100) if total_submissions > 0 else 0, 1
        ),
    }

def get_stats_by_category(db: Session) -> list:
    """Submission count and verification rate per category."""
    categories = db.query(Submission.category).distinct().all()
    results = []
    for (category,) in categories:
        total = db.query(Submission).filter(Submission.category == category).count()
        verified = db.query(Submission).filter(
            Submission.category == category,
            Submission.status == SubmissionStatus.approved,
        ).count()
        pending = db.query(Submission).filter(
            Submission.category == category,
            Submission.status == SubmissionStatus.pending,
        ).count()
        results.append({
            "category": category,
            "total": total,
            "verified": verified,
            "pending": pending,
            "verification_rate": round((verified / total * 100) if total > 0 else 0, 1),
        })

    return sorted(results, key=lambda x: x["total"], reverse=True)

    return sorted(results, key=lambda x: x["total"], reverse=True)


def get_stats_by_department(db: Session) -> list:
    """Submission count per department."""
    rows = db.query(
        User.department,
        func.count(Submission.id).label("total_submissions"),
        func.count(User.id.distinct()).label("total_students"),
    ).join(Submission, Submission.student_id == User.id)\
    .group_by(User.department).all()

    return [
        {
            "department": row.department or "Unknown",
            "total_submissions": row.total_submissions,
            "total_students": row.total_students,
        }
        for row in rows
    ]