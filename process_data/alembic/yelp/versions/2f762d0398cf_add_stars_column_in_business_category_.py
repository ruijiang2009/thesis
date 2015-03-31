"""add stars column in business_category table

Revision ID: 2f762d0398cf
Revises: 41c901d35239
Create Date: 2015-03-30 22:20:09.052150

"""

# revision identifiers, used by Alembic.
revision = '2f762d0398cf'
down_revision = '41c901d35239'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('business_category', sa.Column('stars', sa.Float(precision=1)))


def downgrade():
    op.drop_column('business_category', 'stars')
