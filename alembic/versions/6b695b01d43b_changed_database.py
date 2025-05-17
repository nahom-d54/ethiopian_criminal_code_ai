"""changed database

Revision ID: 6b695b01d43b
Revises: 5bc409445cd9
Create Date: 2025-05-14 23:19:51.861857

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6b695b01d43b'
down_revision: Union[str, None] = '5bc409445cd9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
