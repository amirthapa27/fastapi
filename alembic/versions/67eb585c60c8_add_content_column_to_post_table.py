"""add content column to post table

Revision ID: 67eb585c60c8
Revises: 120004beb924
Create Date: 2022-10-19 23:34:40.394212

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67eb585c60c8'
down_revision = '120004beb924'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
