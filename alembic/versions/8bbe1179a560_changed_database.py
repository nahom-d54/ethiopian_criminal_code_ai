"""changed database

Revision ID: 8bbe1179a560
Revises: e8956d2bfc5a
Create Date: 2025-05-14 23:14:04.094558

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8bbe1179a560'
down_revision: Union[str, None] = 'e8956d2bfc5a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
