"""changed database

Revision ID: e8956d2bfc5a
Revises: af138887f318
Create Date: 2025-05-14 23:12:03.891976

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e8956d2bfc5a'
down_revision: Union[str, None] = 'af138887f318'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
