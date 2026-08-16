from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class NotificationResponse(BaseModel):
    id: UUID
    user_id: UUID
    type: str
    message: str
    read: bool
    created_at: datetime

    class Config:
        from_attributes = True

class MarkReadRequest(BaseModel):
    notification_id: UUID