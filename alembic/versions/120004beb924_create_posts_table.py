"""create posts table

Revision ID: 120004beb924
Revises: 
Create Date: 2022-10-19 23:20:20.011210

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '120004beb924'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_table('posts')
