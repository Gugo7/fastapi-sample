"""add content column to posts table

Revision ID: f1d98c2d04cd
Revises: 5a129fbeb25b
Create Date: 2024-04-17 10:55:11.269074

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f1d98c2d04cd'
down_revision: Union[str, None] = '5a129fbeb25b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content',sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
