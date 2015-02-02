"""add index to review table

Revision ID: 181e3b8020f8
Revises: 658a3c50857
Create Date: 2015-02-02 12:50:59.342657

"""

# revision identifiers, used by Alembic.
revision = '181e3b8020f8'
down_revision = '658a3c50857'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_index('ix_review_business_id', 'review', ['business_id'])
    op.create_index('ix_review_user_id', 'review', ['user_id'])


def downgrade():
    op.drop_index('ix_review_business_id', 'review')
    op.drop_index('ix_review_user_id', 'review')
