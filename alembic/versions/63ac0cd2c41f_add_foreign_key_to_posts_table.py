"""add foreign-key to posts table

Revision ID: 63ac0cd2c41f
Revises: c089ac965074
Create Date: 2022-10-21 15:26:50.517691

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '63ac0cd2c41f'
down_revision = 'c089ac965074'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users',
                          local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts',)
    pass
