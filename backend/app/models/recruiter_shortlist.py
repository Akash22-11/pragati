from sqlalchemy import (
    Column, Integer, ForeignKey, DateTime, Text,
    UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class RecruiterShortlist(Base):
    """
    Tracks which students a recruiter has saved/shortlisted.
    One-directional relationships only -- User model is not modified.
    """
    __tablename__ = "recruiter_shortlists"

    id = Column(Integer, primary_key=True, index=True)

    recruiter_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    student_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    note = Column(Text, nullable=True)
    shortlisted_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("recruiter_id", "student_id", name="uq_recruiter_student"),
    )

    # No back_populates -- one-directional only, avoids touching User model
    recruiter = relationship("User", foreign_keys=[recruiter_id])
    student = relationship("User", foreign_keys=[student_id])
