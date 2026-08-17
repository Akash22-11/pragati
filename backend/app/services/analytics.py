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
    rows = db.query(
        Submission.category,
        func.count(Submission.id).label("total"),
        func.sum(
            func.cast(Submission.status == SubmissionStatus.approved, db.bind.dialect.name == "postgresql" and "integer" or "integer")
        ).label("verified"),
    ).group_by(Submission.category).all()

    results = []
    for row in rows:
        total = row.total or 0
        verified = row.verified or 0
        results.append({
            "category": row.category,
            "total": total,
            "verified": verified,
            "pending": db.query(Submission).filter(
                Submission.category == row.category,
                Submission.status == SubmissionStatus.pending,
            ).count(),
            "verification_rate": round((verified / total * 100) if total > 0 else 0, 1),
        })

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