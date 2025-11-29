"""problem is raised

Revision ID: 0ddbb655e7ab
Revises: 640fd5ec6ecf
Create Date: 2025-11-29 18:47:53.608097

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0ddbb655e7ab'
down_revision: Union[str, Sequence[str], None] = '640fd5ec6ecf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
