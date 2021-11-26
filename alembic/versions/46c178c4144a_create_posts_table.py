"""create posts table

Revision ID: 46c178c4144a
Revises: 
Create Date: 2021-11-25 14:21:01.337695

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46c178c4144a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', 
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('title', sa.String(), nullable=False))

    pass


def downgrade():
    op.drop_table('posts')
    pass
