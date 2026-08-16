from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.notification import NotificationResponse, MarkReadRequest
from app.services.notification import get_notifications, mark_notification_read

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("/", response_model=list[NotificationResponse])
def list_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_notifications(db, current_user.id)

@router.patch("/read")
def mark_read(
    payload: MarkReadRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    notification = mark_notification_read(db, payload.notification_id)
    if not notification:
        return {"message": "Notification not found"}
    return {"message": "Notification marked as read"}