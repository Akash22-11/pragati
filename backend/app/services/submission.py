from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.submission import Submission, SubmissionStatus
from app.models.verification import Verification, VerificationAction
from app.models.user import User
from app.services.email import send_verification_result
from datetime import datetime
import hashlib
import uuid

def get_submission_by_id(db: Session, submission_id: uuid.UUID) -> Submission:
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    return submission

def get_submissions_by_status(db: Session, status: SubmissionStatus = None, student_id: uuid.UUID = None):
    query = db.query(Submission)
    if status:
        query = query.filter(Submission.status == status)
    if student_id:
        query = query.filter(Submission.student_id == student_id)
    return query.all()

def verify_submission(db, submission_id, verifier, action, note=None):
    submission = get_submission_by_id(db, submission_id)
    student = db.query(User).filter(User.id == submission.student_id).first()

    if action == VerificationAction.approved:
        submission.status = SubmissionStatus.approved
    elif action == VerificationAction.rejected:
        submission.status = SubmissionStatus.rejected
    elif action == VerificationAction.returned:
        submission.status = SubmissionStatus.returned

    hash_value = None
    if action == VerificationAction.approved:
        timestamp = datetime.utcnow().isoformat()
        raw = f"{submission_id}{verifier.id}{timestamp}"
        hash_value = hashlib.sha256(raw.encode()).hexdigest()

    verification = Verification(
        submission_id=submission_id,
        verifier_id=verifier.id,
        action=action,
        note=note,
        timestamp=datetime.utcnow(),
        hash=hash_value
    )

    db.add(verification)
    db.commit()
    db.refresh(verification)

    if student:
        send_verification_result(
            student_email=student.email,
            student_name=student.full_name,
            title=submission.title,
            action=action,
            note=note
        )

    return verification