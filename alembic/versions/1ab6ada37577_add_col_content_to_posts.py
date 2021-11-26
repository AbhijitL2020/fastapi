"""add col content to posts

Revision ID: 1ab6ada37577
Revises: 46c178c4144a
Create Date: 2021-11-26 06:50:34.864112

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ab6ada37577'
down_revision = '46c178c4144a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
