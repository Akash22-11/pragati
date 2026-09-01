"""Phase 2: Create postings and applications tables

Revision ID: phase2_postings_001
Revises: phase1_recruiter_001
Create Date: 2026-09-01
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


revision = "phase2_postings_001"
down_revision = "phase1_recruiter_001"
branch_labels = None
depends_on = None


def upgrade() -> None:

    posting_type = sa.Enum("internship", "job", name="postingtype")
    posting_status = sa.Enum("open", "closed", name="postingstatus")
    application_status = sa.Enum(
        "applied", "shortlisted", "selected", "rejected", name="applicationstatus"
    )

    op.create_table(
        "postings",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "recruiter_id", UUID(as_uuid=True),
            sa.ForeignKey("users.id"),
            nullable=False,
        ),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("type", posting_type, nullable=False, server_default="internship"),
        sa.Column("location", sa.String(), nullable=True),
        sa.Column("stipend", sa.String(), nullable=True),
        sa.Column("positions", sa.Integer(), nullable=True, server_default="1"),
        sa.Column("skills_required", sa.JSON(), nullable=True),
        sa.Column("deadline", sa.DateTime(), nullable=True),
        sa.Column("status", posting_status, nullable=False, server_default="open"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()")),
    )
    op.create_index("ix_postings_recruiter_id", "postings", ["recruiter_id"])

    op.create_table(
        "applications",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "posting_id", UUID(as_uuid=True),
            sa.ForeignKey("postings.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "student_id", UUID(as_uuid=True),
            sa.ForeignKey("users.id"),
            nullable=False,
        ),
        sa.Column("status", application_status, nullable=False, server_default="applied"),
        sa.Column("cover_note", sa.Text(), nullable=True),
        sa.Column("applied_at", sa.DateTime(), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()")),
    )
    op.create_index("ix_applications_posting_id", "applications", ["posting_id"])
    op.create_index("ix_applications_student_id", "applications", ["student_id"])
    op.create_unique_constraint(
        "uq_posting_student", "applications", ["posting_id", "student_id"]
    )

    # cgpa was declared Float in phase1 but the model had drifted to String;
    # this migration is a no-op for the column itself but recorded here for
    # traceability -- see app/models/user.py fix.


def downgrade() -> None:
    op.drop_table("applications")
    op.drop_table("postings")
    op.execute("DROP TYPE IF EXISTS applicationstatus")
    op.execute("DROP TYPE IF EXISTS postingstatus")
    op.execute("DROP TYPE IF EXISTS postingtype")
