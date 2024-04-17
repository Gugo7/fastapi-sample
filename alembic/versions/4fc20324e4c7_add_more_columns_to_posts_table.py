"""add more columns to posts table

Revision ID: 4fc20324e4c7
Revises: 046e524e1bb1
Create Date: 2024-04-17 11:28:52.719506

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4fc20324e4c7'
down_revision: Union[str, None] = '046e524e1bb1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('published', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('posts',sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                                    nullable=False, server_default=sa.text('now()')))
    pass


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
