"""create user_business table

Revision ID: 4e99911ac3ed
Revises: 144016e6f122
Create Date: 2015-02-21 16:30:58.099019

"""

# revision identifiers, used by Alembic.
revision = '4e99911ac3ed'
down_revision = '144016e6f122'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'user_business',
        sa.Column('user_id', sa.String(22), sa.ForeignKey('yelp_user.user_id'), nullable=False, primary_key=True),
        sa.Column('business_id', sa.String(22), sa.ForeignKey('business.business_id'), nullable=False, primary_key=True),
        sa.Column('stars', sa.Float(precision=20)),
    )


def downgrade():
    op.drop_table('user_business')
