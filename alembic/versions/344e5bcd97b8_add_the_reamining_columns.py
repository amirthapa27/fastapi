"""add the reamining columns

Revision ID: 344e5bcd97b8
Revises: 63ac0cd2c41f
Create Date: 2022-10-21 15:53:17.738582

"""
from alembic import op
import alembic
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '344e5bcd97b8'
down_revision = '63ac0cd2c41f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(),
                  nullable=False, server_default='True'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(
        timezone=True), nullable=False, server_default=sa.text('now()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
