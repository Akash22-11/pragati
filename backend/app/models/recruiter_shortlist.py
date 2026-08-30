from sqlalchemy import (
    Column, Integer, ForeignKey, DateTime, Text,
    UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class RecruiterShortlist(Base):
    """
    Tracks which students a recruiter has saved/shortlisted
    for future reference — before any formal application exists.
    This is Phase 1 only. Phase 2 adds the full Application model.
    """
    __tablename__ = "recruiter_shortlists"

    id = Column(Integer, primary_key=True, index=True)

    recruiter_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    student_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    note = Column(Text, nullable=True)   # recruiter's private note about student
    shortlisted_at = Column(DateTime(timezone=True), server_default=func.now())

    # One recruiter can shortlist a student only once
    __table_args__ = (
        UniqueConstraint("recruiter_id", "student_id", name="uq_recruiter_student"),
    )

    # ── Relationships ──────────────────────────────────────────────
    recruiter = relationship(
        "User",
        back_populates="shortlisted_students",
        foreign_keys=[recruiter_id]
    )
    student = relationship(
        "User",
        foreign_keys=[student_id]
    )
