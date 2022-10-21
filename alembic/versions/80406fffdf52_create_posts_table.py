"""create posts table

Revision ID: 80406fffdf52
Revises: 
Create Date: 2022-10-21 13:05:04.530795

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80406fffdf52'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer, nullable=False, primary_key=True),
                    sa.Column('title', sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
