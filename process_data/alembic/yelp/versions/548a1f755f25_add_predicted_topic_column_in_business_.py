"""add predicted_topic_50 column in business table

Revision ID: 548a1f755f25
Revises: 37b808c1bd6
Create Date: 2015-02-10 09:43:16.098995

"""

# revision identifiers, used by Alembic.
revision = '548a1f755f25'
down_revision = '37b808c1bd6'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('business', sa.Column('predicted_topic_50', sa.Text()))

def downgrade():
    op.drop_column('business', 'predicted_topic_50')
