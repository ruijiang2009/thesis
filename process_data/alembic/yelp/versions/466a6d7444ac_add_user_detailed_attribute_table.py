"""add user_detailed_attribute table

Revision ID: 466a6d7444ac
Revises: 2f762d0398cf
Create Date: 2015-04-01 22:41:09.142969

"""

# revision identifiers, used by Alembic.
revision = '466a6d7444ac'
down_revision = '2f762d0398cf'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'user_detailed_attribute',
        sa.Column('user_id', sa.String(22), sa.ForeignKey('yelp_user.user_id'), primary_key=True),
        sa.Column('detailed_attribute_id', sa.Integer, sa.ForeignKey('detailed_attribute.id'), primary_key=True),
        sa.Column('stars', sa.Float(precision=20)),
        sa.Column('relationship', sa.Float(precision=20))
        )
    op.create_index('ix_user_detailed_attribute_user_id', 'user_detailed_attribute', ['user_id'])

def downgrade():
    op.drop_index('ix_user_detailed_attribute_user_id')
    op.drop_table('user_detailed_attribute')
