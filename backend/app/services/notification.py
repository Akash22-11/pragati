from sqlalchemy.orm import Session
from app.models.notification import Notification
from app.socket import send_notification
import uuid

async def create_and_send_notification(
    db: Session,
    user_id: uuid.UUID,
    type: str,
    message: str,
) -> Notification:
    # Save to database
    notification = Notification(
        user_id=user_id,
        type=type,
        message=message,
        read=False,
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)

    # Send real-time event via Socket.IO
    await send_notification(
        user_id=str(user_id),
        type=type,
        message=message,
    )

    return notification

def get_notifications(db: Session, user_id: uuid.UUID) -> list[Notification]:
    return db.query(Notification).filter(
        Notification.user_id == user_id
    ).order_by(Notification.created_at.desc()).all()

def mark_notification_read(db: Session, notification_id: uuid.UUID) -> Notification:
    notification = db.query(Notification).filter(
        Notification.id == notification_id
    ).first()
    if notification:
        notification.read = True
        db.commit()
        db.refresh(notification)
    return notification