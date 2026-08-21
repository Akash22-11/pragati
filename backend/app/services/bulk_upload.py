import pandas as pd
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.submission import Submission, SubmissionCategory, SubmissionStatus
from app.models.user import User
import io


REQUIRED_COLUMNS = ["student_email", "title", "description", "category"]


def parse_bulk_file(file_bytes: bytes, filename: str) -> pd.DataFrame:
    """Parse CSV or Excel file into a DataFrame."""
    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(file_bytes))
        elif filename.endswith((".xlsx", ".xls")):
            df = pd.read_excel(io.BytesIO(file_bytes))
        else:
            raise HTTPException(status_code=400, detail="File must be .csv, .xlsx, or .xls")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not parse file: {str(e)}")

    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required columns: {', '.join(missing_cols)}"
        )

    return df


def validate_rows(db: Session, df: pd.DataFrame) -> dict:
    """Validate each row before insert. Returns valid rows and errors."""
    valid_rows = []
    errors = []

    for idx, row in df.iterrows():
        row_num = idx + 2  # account for header row + 0-index

        student = db.query(User).filter(User.email == row["student_email"]).first()
        if not student:
            errors.append({"row": row_num, "error": f"Student not found: {row['student_email']}"})
            continue

        category_value = str(row["category"]).strip().lower()
        valid_categories = [c.value for c in SubmissionCategory]
        if category_value not in valid_categories:
            errors.append({"row": row_num, "error": f"Invalid category: {row['category']}"})
            continue

        if pd.isna(row["title"]) or not str(row["title"]).strip():
            errors.append({"row": row_num, "error": "Title is required"})
            continue

        valid_rows.append({
            "student_id": student.id,
            "title": str(row["title"]).strip(),
            "description": str(row["description"]).strip() if not pd.isna(row.get("description")) else None,
            "category": category_value,
        })

    return {"valid_rows": valid_rows, "errors": errors}


def bulk_insert_submissions(db: Session, valid_rows: list) -> int:
    """Bulk insert validated submissions."""
    submissions = [
        Submission(
            student_id=row["student_id"],
            title=row["title"],
            description=row["description"],
            category=row["category"],
            status=SubmissionStatus.pending,
        )
        for row in valid_rows
    ]
    db.bulk_save_objects(submissions)
    db.commit()
    return len(submissions)