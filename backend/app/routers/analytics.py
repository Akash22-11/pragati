from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies.auth import require_role
from app.models.user import User, UserRole
from app.services.analytics import get_stats, get_stats_by_category, get_stats_by_department

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/stats")
def analytics_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.faculty, UserRole.admin)),
):
    return get_stats(db)


@router.get("/category")
def analytics_by_category(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.faculty, UserRole.admin)),
):
    return get_stats_by_category(db)


@router.get("/dept")
def analytics_by_department(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.faculty, UserRole.admin)),
):
    return get_stats_by_department(db)