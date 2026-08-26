from sqlalchemy import Column, String, DateTime, Enum, ForeignKey, Text
from app.db_types import GUID
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import uuid
import enum


class VerificationAction(str, enum.Enum):
    approved = "approved"
    rejected = "rejected"
    returned = "returned"


class Verification(Base):
    __tablename__ = "verifications"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    submission_id = Column(GUID(), ForeignKey("submissions.id"), nullable=False)
    verifier_id = Column(GUID(), ForeignKey("users.id"), nullable=False)
    action = Column(Enum(VerificationAction), nullable=False)
    note = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    hash = Column(String, nullable=True)

    submission = relationship("Submission", back_populates="verification")
    verifier = relationship("User")