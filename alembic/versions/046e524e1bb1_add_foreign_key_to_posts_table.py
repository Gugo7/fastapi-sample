"""add foreign key to posts table

Revision ID: 046e524e1bb1
Revises: 2dfa33bedf12
Create Date: 2024-04-17 11:21:57.818780

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '046e524e1bb1'
down_revision: Union[str, None] = '2dfa33bedf12'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk',
                          source_table='posts',
                          referent_table='users',
                          local_cols=['owner_id'],
                          remote_cols=['id'],
                          ondelete='CASCADE'
                          )
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
