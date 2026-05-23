"""fix updated_at default

Revision ID: adaa4619a3ef
Revises: efc286155b43
Create Date: 2026-05-21 02:45:13.926067

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'adaa4619a3ef'
down_revision: Union[str, Sequence[str], None] = 'a44ad623c01d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        'users',
        'updated_at',
        server_default=sa.func.now(),
        existing_type=sa.DateTime(timezone=True),
        nullable=False
    )

def downgrade() -> None:
    op.alter_column(
        'users',
        'updated_at',
        server_default=None,
        existing_type=sa.DateTime(timezone=True),
        nullable=True
    )


