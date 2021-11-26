"""add more columns to posts

Revision ID: 2ae2c5ea85de
Revises: 63651912b220
Create Date: 2021-11-26 07:55:27.350925

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ae2c5ea85de'
down_revision = '63651912b220'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', 
        sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE')
    )
    op.add_column('posts', 
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))
    )
    pass


def downgrade():
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'published')
    pass
