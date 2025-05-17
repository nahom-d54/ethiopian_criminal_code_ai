"""changed database

Revision ID: af138887f318
Revises: f6a4596a6e6c
Create Date: 2025-05-14 23:10:39.745525

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "af138887f318"
down_revision: Union[str, None] = "f6a4596a6e6c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
