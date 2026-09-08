"""Convert status to enum

Revision ID: 4c7b4f527570
Revises: 8684653e6f0a
Create Date: 2026-09-08 21:58:21.781255

"""
from typing import Sequence, Union
from sqlalchemy.dialects import postgresql
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4c7b4f527570'
down_revision: Union[str, None] = '8684653e6f0a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    contact_status_enum = postgresql.ENUM(
        'pending', 'contacted', 'in_progress', 'shipped', 'delivered',
        name='contactstatus'
    )
    contact_status_enum.create(op.get_bind(), checkfirst=True)

    op.alter_column(
        'contact_requests', 'status',
        existing_type=sa.VARCHAR(),
        type_=contact_status_enum,
        postgresql_using='status::contactstatus',
        existing_nullable=True
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    op.alter_column(
        'contact_requests', 'status',
        existing_type=sa.Enum('pending', 'contacted', 'in_progress', 'shipped', 'delivered', name='contactstatus'),
        type_=sa.VARCHAR(),
        postgresql_using='status::varchar',
        existing_nullable=True
    )

    contact_status_enum = postgresql.ENUM(
        'pending', 'contacted', 'in_progress', 'shipped', 'delivered',
        name='contactstatus'
    )
    contact_status_enum.drop(op.get_bind(), checkfirst=True)
    # ### end Alembic commands ###
