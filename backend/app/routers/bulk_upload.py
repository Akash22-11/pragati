from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies.auth import require_role
from app.models.user import User, UserRole
from app.services.bulk_upload import parse_bulk_file, validate_rows, bulk_insert_submissions

router = APIRouter(prefix="/bulk-upload", tags=["Bulk Upload"])


@router.post("/submissions")
async def bulk_upload_submissions(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.faculty, UserRole.admin)),
):
    """Upload a CSV/Excel file to bulk create submissions.

    Required columns: student_email, title, description, category
    """
    file_bytes = await file.read()
    df = parse_bulk_file(file_bytes, file.filename)

    result = validate_rows(db, df)
    valid_rows = result["valid_rows"]
    errors = result["errors"]

    inserted_count = 0
    if valid_rows:
        inserted_count = bulk_insert_submissions(db, valid_rows)

    return {
        "message": f"{inserted_count} submissions created successfully",
        "total_rows": len(df),
        "inserted": inserted_count,
        "failed": len(errors),
        "errors": errors,
    }