"""Add user roles

Revision ID: cda12aab9e1c
Revises: ff01c4589a6f
Create Date: 2025-04-13 19:10:15.296996

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cda12aab9e1c'
down_revision: Union[str, None] = 'ff01c4589a6f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
