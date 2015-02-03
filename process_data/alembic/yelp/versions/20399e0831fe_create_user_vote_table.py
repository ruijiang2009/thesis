"""create user_vote table

Revision ID: 20399e0831fe
Revises: 181e3b8020f8
Create Date: 2015-02-02 15:34:14.661723

"""

# revision identifiers, used by Alembic.
revision = '20399e0831fe'
down_revision = '181e3b8020f8'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'user_vote',
        sa.Column('user_id', sa.String(22), sa.ForeignKey('yelp_user.user_id'), primary_key=True),
        sa.Column('vote', sa.String(10), primary_key=True),
        sa.Column('number', sa.Integer)
    )


def downgrade():
    op.drop_table('user_vote')
