"""merge phase1 sync and phase2 postings branches

Revision ID: 6a5f0394de7a
Revises: 3dedac9507cd, phase2_postings_001
Create Date: 2026-09-04 15:24:44.827119

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6a5f0394de7a'
down_revision: Union[str, None] = ('3dedac9507cd', 'phase2_postings_001')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass