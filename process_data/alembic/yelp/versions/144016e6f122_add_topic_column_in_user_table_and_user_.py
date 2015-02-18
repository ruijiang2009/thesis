"""add topic column in user table and user_topic tables

Revision ID: 144016e6f122
Revises: 3f866da1246d
Create Date: 2015-02-17 20:03:39.662917

"""

# revision identifiers, used by Alembic.
revision = '144016e6f122'
down_revision = '3f866da1246d'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('yelp_user', sa.Column('predicted_topic_50', sa.Text()))
    op.add_column('yelp_user', sa.Column('predicted_topic_22', sa.Text()))

    op.create_table(
        'user_topic22',
        sa.Column('topic_id', sa.Integer, sa.ForeignKey('topic22.id'), nullable=False),
        sa.Column('user_id', sa.String(22), sa.ForeignKey('yelp_user.user_id'), nullable=False),
        sa.Column('stars', sa.Float(precision=20)),
        sa.Column('relationship', sa.Float(precision=20))
    )

    op.create_table(
        'user_topic50',
        sa.Column('topic_id', sa.Integer, sa.ForeignKey('topic50.id'), nullable=False),
        sa.Column('user_id', sa.String(22), sa.ForeignKey('yelp_user.user_id'), nullable=False),
        sa.Column('stars', sa.Float(precision=20)),
        sa.Column('relationship', sa.Float(precision=20))
    )

def downgrade():
    op.drop_column('yelp_user', 'predicted_topic_50')
    op.drop_column('yelp_user', 'predicted_topic_22')

    op.drop_table('user_topic22')
    op.drop_table('user_topic50')