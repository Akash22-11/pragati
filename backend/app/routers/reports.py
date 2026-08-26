from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from app.database import get_db
from app.dependencies.auth import require_role
from app.models.user import User, UserRole
from app.services.reports import get_naac_data, get_nirf_data, generate_naac_pdf, generate_nirf_pdf

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/naac")
def download_naac_report(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.faculty, UserRole.admin)),
):
    data = get_naac_data(db, start_date, end_date)
    pdf_bytes = generate_naac_pdf(data)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=naac_report.pdf"},
    )


@router.get("/nirf")
def download_nirf_report(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.faculty, UserRole.admin)),
):
    data = get_nirf_data(db, start_date, end_date)
    pdf_bytes = generate_nirf_pdf(data)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=nirf_report.pdf"},
    )