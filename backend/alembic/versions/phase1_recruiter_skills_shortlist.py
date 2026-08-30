"""Phase 1: Add recruiter fields to users, skills to submissions, create recruiter_shortlists

Revision ID: phase1_recruiter_001
Revises: 96d13e17736a
Create Date: 2026-08-27
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import UUID


revision = "phase1_recruiter_001"
down_revision = "96d13e17736a"
branch_labels = None
depends_on = None


def upgrade() -> None:

    # 1. Add recruiter columns to users table
    op.add_column("users", sa.Column("company_name", sa.String(200), nullable=True))
    op.add_column("users", sa.Column("company_sector", sa.String(100), nullable=True))
    op.add_column("users", sa.Column("company_website", sa.String(300), nullable=True))
    op.add_column("users", sa.Column("company_description", sa.Text(), nullable=True))
    op.add_column("users", sa.Column(
        "is_verified_company", sa.Boolean(), nullable=False,
        server_default=sa.text("false")
    ))

    # 2. Add cgpa column to users table
    op.add_column("users", sa.Column("cgpa", sa.Float(), nullable=True))

    # 3. Add skills column to submissions table
    op.add_column("submissions", sa.Column(
        "skills",
        postgresql.JSON(astext_type=sa.Text()),
        nullable=True,
        server_default=sa.text("'[]'::json")
    ))

    # 4. Create recruiter_shortlists table
    op.create_table(
        "recruiter_shortlists",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "recruiter_id", UUID(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False
        ),
        sa.Column(
            "student_id", UUID(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False
        ),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column(
            "shortlisted_at", sa.DateTime(timezone=True),
            server_default=sa.text("now()")
        ),
    )

    # Indexes
    op.create_index(
        "ix_recruiter_shortlists_recruiter_id",
        "recruiter_shortlists", ["recruiter_id"]
    )
    op.create_index(
        "ix_recruiter_shortlists_student_id",
        "recruiter_shortlists", ["student_id"]
    )

    # Unique constraint
    op.create_unique_constraint(
        "uq_recruiter_student",
        "recruiter_shortlists",
        ["recruiter_id", "student_id"]
    )


def downgrade() -> None:

    op.drop_table("recruiter_shortlists")
    op.drop_column("submissions", "skills")
    op.drop_column("users", "cgpa")
    op.drop_column("users", "is_verified_company")
    op.drop_column("users", "company_description")
    op.drop_column("users", "company_website")
    op.drop_column("users", "company_sector")
    op.drop_column("users", "company_name")