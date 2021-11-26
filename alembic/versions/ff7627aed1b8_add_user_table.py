"""add user table

Revision ID: ff7627aed1b8
Revises: 1ab6ada37577
Create Date: 2021-11-26 07:23:44.417159

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.schema import Column, UniqueConstraint
from sqlalchemy.sql.sqltypes import TIMESTAMP


# revision identifiers, used by Alembic.
revision = 'ff7627aed1b8'
down_revision = '1ab6ada37577'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', 
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
            server_default=sa.text('now()'), nullable=False),
        sa.UniqueConstraint('email')
        )

    pass


def downgrade():
    op.drop_table('users')
    pass
