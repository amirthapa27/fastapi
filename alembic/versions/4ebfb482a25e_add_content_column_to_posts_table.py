"""add content column to posts table

Revision ID: 4ebfb482a25e
Revises: 80406fffdf52
Create Date: 2022-10-21 13:18:13.404200

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ebfb482a25e'
down_revision = '80406fffdf52'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
