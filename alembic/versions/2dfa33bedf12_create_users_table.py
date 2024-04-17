"""create users table

Revision ID: 2dfa33bedf12
Revises: f1d98c2d04cd
Create Date: 2024-04-17 11:06:11.604044

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2dfa33bedf12'
down_revision: Union[str, None] = 'f1d98c2d04cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email', 'username')
    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
