"""add topic_22 column in business

Revision ID: 4ee36ba7afe7
Revises: 548a1f755f25
Create Date: 2015-02-15 11:21:36.501251

"""

# revision identifiers, used by Alembic.
revision = '4ee36ba7afe7'
down_revision = '548a1f755f25'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('business', sa.Column('predicted_topic_22', sa.Text()))

def downgrade():
    op.drop_column('business', 'predicted_topic_22')
