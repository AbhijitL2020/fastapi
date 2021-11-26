"""add fk to posts

Revision ID: 63651912b220
Revises: ff7627aed1b8
Create Date: 2021-11-26 07:42:41.002307

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '63651912b220'
down_revision = 'ff7627aed1b8'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',
        sa.Column('owner_id', sa.Integer(), nullable=False)
    )
    op.create_foreign_key('posts_user_fk', 
        source_table='posts', referent_table='users',
        local_cols=['owner_id'], remote_cols=['id'],
        ondelete='CASCADE'
    )
    pass


def downgrade():
    op.drop_constraint('posts_user_fk', table_name='posts')
    op.drop_column(table_name='posts', column_name='owner_id')
    pass
