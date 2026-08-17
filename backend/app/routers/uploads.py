from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies.auth import get_current_user, require_role
from app.models.user import User, UserRole
from app.models.submission import Submission, SubmissionCategory
from app.services.cloudinary import upload_file
from app.services.email import send_submission_confirmation, send_admin_new_submission
import uuid

router = APIRouter(prefix="/uploads", tags=["Uploads"])

@router.post("/submission")
async def upload_submission(
    title: str = Form(...),
    description: str = Form(None),
    category: SubmissionCategory = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.student)),
):
    # Read file bytes
    file_bytes = await file.read()

    # Upload to Cloudinary
    filename = f"{current_user.id}_{uuid.uuid4()}_{file.filename}"
    file_url = upload_file(file_bytes, filename, folder="pragati/submissions")

    # Save submission to DB
    submission = Submission(
        student_id=current_user.id,
        title=title,
        description=description,
        category=category,
        file_url=file_url,
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)

    # Send confirmation email to student
    send_submission_confirmation(
        student_email=current_user.email,
        student_name=current_user.full_name,
        title=title,
    )

    # Send alert email to admin
    send_admin_new_submission(
        student_name=current_user.full_name,
        title=title,
        category=category,
    )

    return {
        "message": "Submission uploaded successfully",
        "submission_id": str(submission.id),
        "file_url": file_url,
        "status": submission.status,
    }