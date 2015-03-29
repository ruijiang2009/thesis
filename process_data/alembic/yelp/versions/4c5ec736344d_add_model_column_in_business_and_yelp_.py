"""add model column in business and yelp user

Revision ID: 4c5ec736344d
Revises: 16344287a627
Create Date: 2015-03-28 22:15:12.847087

"""

# revision identifiers, used by Alembic.
revision = '4c5ec736344d'
down_revision = '421b662d226b'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import BYTEA

def upgrade():
    op.add_column('yelp_user', sa.Column('model_topic_50', BYTEA()))
    op.add_column('yelp_user', sa.Column('model_topic_22', BYTEA()))
    op.add_column('business', sa.Column('model_topic_50', BYTEA()))
    op.add_column('business', sa.Column('model_topic_22', BYTEA()))




def downgrade():
    op.drop_column('yelp_user', 'model_topic_22')
    op.drop_column('yelp_user', 'model_topic_50')
    op.drop_column('business', 'model_topic_22')
    op.drop_column('business', 'model_topic_50')
