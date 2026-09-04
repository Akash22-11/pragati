"""sync models with phase1 schema

Revision ID: 3dedac9507cd
Revises: phase1_recruiter_001
Create Date: 2026-09-04 15:09:25.041199

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from app.db_types import GUID


# revision identifiers, used by Alembic.
revision: str = '3dedac9507cd'
down_revision: Union[str, None] = 'phase1_recruiter_001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop the old integer sequence default before changing the column type
    op.execute("ALTER TABLE recruiter_shortlists ALTER COLUMN id DROP DEFAULT")

    op.alter_column(
        'recruiter_shortlists', 'id',
        existing_type=sa.INTEGER(),
        type_=GUID(),
        existing_nullable=False,
        postgresql_using='gen_random_uuid()',
    )

    # Clean up the now-unused sequence
    op.execute("DROP SEQUENCE IF EXISTS recruiter_shortlists_id_seq")

    op.alter_column('users', 'company_description',
               existing_type=sa.TEXT(),
               type_=sa.String(),
               existing_nullable=True)
    op.alter_column('users', 'is_verified_company',
               existing_type=sa.BOOLEAN(),
               nullable=True,
               existing_server_default=sa.text('false'))
    op.alter_column('users', 'cgpa',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               type_=sa.String(),
               existing_nullable=True)


def downgrade() -> None:
    op.alter_column('users', 'cgpa',
               existing_type=sa.String(),
               type_=sa.DOUBLE_PRECISION(precision=53),
               existing_nullable=True)
    op.alter_column('users', 'is_verified_company',
               existing_type=sa.BOOLEAN(),
               nullable=False,
               existing_server_default=sa.text('false'))
    op.alter_column('users', 'company_description',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               existing_nullable=True)
    op.alter_column(
        'recruiter_shortlists', 'id',
        existing_type=GUID(),
        type_=sa.INTEGER(),
        existing_nullable=False,
        postgresql_using='0',
    )