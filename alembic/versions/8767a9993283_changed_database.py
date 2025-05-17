"""changed database

Revision ID: 8767a9993283
Revises: 8bbe1179a560
Create Date: 2025-05-14 23:15:59.907454

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8767a9993283'
down_revision: Union[str, None] = '8bbe1179a560'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
