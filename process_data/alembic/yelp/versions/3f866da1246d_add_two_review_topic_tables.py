"""add two review topic tables

Revision ID: 3f866da1246d
Revises: 2f18399792ed
Create Date: 2015-02-15 22:02:51.317158

"""

# revision identifiers, used by Alembic.
revision = '3f866da1246d'
down_revision = '2f18399792ed'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'review_topic22',
        sa.Column('topic_id', sa.Integer, sa.ForeignKey('topic22.id'), nullable=False),
        sa.Column('review_id', sa.String(22), sa.ForeignKey('review.review_id'), nullable=False, index=True),
        sa.Column('stars', sa.Float(precision=20)),
        sa.Column('relationship', sa.Float(precision=20))
    )

    op.create_table(
        'review_topic50',
        sa.Column('topic_id', sa.Integer, sa.ForeignKey('topic50.id'), nullable=False),
        sa.Column('review_id', sa.String(22), sa.ForeignKey('review.review_id'), nullable=False, index=True),
        sa.Column('stars', sa.Float(precision=20)),
        sa.Column('relationship', sa.Float(precision=20))
    )

def downgrade():
    op.drop_table('review_topic22')
    op.drop_table('review_topic50')


