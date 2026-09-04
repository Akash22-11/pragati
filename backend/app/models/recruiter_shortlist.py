from sqlalchemy import Column, ForeignKey, DateTime, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from app.db_types import GUID
import uuid


class RecruiterShortlist(Base):
    """
    Tracks which students a recruiter has saved/shortlisted
    for future reference — before any formal application exists.
    This is Phase 1 only. Phase 2 adds the full Application model.
    """
    __tablename__ = "recruiter_shortlists"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)

    recruiter_id = Column(
        GUID(),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    student_id = Column(
        GUID(),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    note = Column(Text, nullable=True)
    shortlisted_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("recruiter_id", "student_id", name="uq_recruiter_student"),
    )

    recruiter = relationship("User", foreign_keys=[recruiter_id])
    student = relationship("User", foreign_keys=[student_id])