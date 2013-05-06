"""Create basic (not so good) contact model.

Revision ID: 3821916c0277
Revises: None
Create Date: 2013-05-06 14:48:57.661203

"""

# revision identifiers, used by Alembic.
revision = '3821916c0277'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'contacts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('contacts')
