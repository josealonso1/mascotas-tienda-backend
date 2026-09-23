"""Add artwork visibility

Revision ID: c9a7e8d4f211
Revises: 4c7b4f527570
Create Date: 2026-09-23
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'c9a7e8d4f211'
down_revision: Union[str, None] = '4c7b4f527570'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'artworks',
        sa.Column('visible', sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.alter_column('artworks', 'visible', server_default=None)


def downgrade() -> None:
    op.drop_column('artworks', 'visible')
