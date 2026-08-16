from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.profile import Profile
from app.models.submission import Submission, SubmissionStatus
from app.models.user import User
import uuid

def get_or_create_profile(db: Session, student_id: uuid.UUID) -> Profile:
    profile = db.query(Profile).filter(Profile.student_id == student_id).first()
    if not profile:
        profile = Profile(student_id=student_id)
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile

def get_full_profile(db: Session, student_id: uuid.UUID) -> dict:
    # Check student exists
    student = db.query(User).filter(User.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Get or create profile
    profile = get_or_create_profile(db, student_id)

    # Get only verified submissions
    verified_submissions = db.query(Submission).filter(
        Submission.student_id == student_id,
        Submission.status == SubmissionStatus.approved,
    ).all()

    return {
        "profile": profile,
        "student": student,
        "verified_submissions": verified_submissions,
    }