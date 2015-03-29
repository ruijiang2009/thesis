"""add user category table

Revision ID: 3e64c7b89113
Revises: 4c5ec736344d
Create Date: 2015-03-29 09:17:34.355506

"""

# revision identifiers, used by Alembic.
revision = '3e64c7b89113'
down_revision = '4c5ec736344d'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'user_category',
        sa.Column('category_id', sa.Integer, sa.ForeignKey('category.id'), nullable=False, primary_key=True),
        sa.Column('user_id', sa.String(22), sa.ForeignKey('yelp_user.user_id'), nullable=False, primary_key=True),
        sa.Column('stars', sa.Float(precision=20)),
        sa.Column('relationship', sa.Float(precision=20))
    )
    op.create_index('ix_user_category_user_id', 'user_category', ['user_id'])


def downgrade():
    op.drop_index('ix_user_category_user_id', 'user_category')
    op.drop_table('user_category')
