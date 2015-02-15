"""add topic table

Revision ID: 2f18399792ed
Revises: 4ee36ba7afe7
Create Date: 2015-02-15 11:45:00.784361

"""

# revision identifiers, used by Alembic.
revision = '2f18399792ed'
down_revision = '4ee36ba7afe7'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


"""
topic22 table can only have 22 topics
topic50 table can only have 50 topics
"""
def upgrade():
    op.create_table(
        'topic22',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.Unicode(200), nullable=False),
        sa.Column('content', sa.Text()),
        sa.Column('percentage', sa.Float(precision=20))
    )

    op.create_table(
        'business_topic22',
        sa.Column('topic_id', sa.Integer, sa.ForeignKey('topic22.id'), nullable=False),
        sa.Column('business_id', sa.String(22), sa.ForeignKey('business.business_id'), nullable=False),
        sa.Column('stars', sa.Float(precision=20)),
        sa.Column('relationship', sa.Float(precision=20))
    )

    op.create_table(
        'topic50',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.Unicode(200), nullable=False),
        sa.Column('content', sa.Text()),
        sa.Column('percentage', sa.Float(precision=20))
    )

    op.create_table(
        'business_topic50',
        sa.Column('topic_id', sa.Integer, sa.ForeignKey('topic50.id'), nullable=False),
        sa.Column('business_id', sa.String(22), sa.ForeignKey('business.business_id'), nullable=False),
        sa.Column('stars', sa.Float(precision=20)),
        sa.Column('relationship', sa.Float(precision=20))
    )

def downgrade():
    op.drop_table('business_topic22')
    op.drop_table('topic22')
    op.drop_table('business_topic50')
    op.drop_table('topic50')