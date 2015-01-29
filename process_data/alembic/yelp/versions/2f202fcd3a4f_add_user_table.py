"""add user table

Revision ID: 2f202fcd3a4f
Revises: 213809085eee
Create Date: 2015-01-28 15:59:57.144085

"""

# revision identifiers, used by Alembic.
revision = '2f202fcd3a4f'
down_revision = '213809085eee'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

# some information is not handled: votes, elite, compliments

def upgrade():
    op.create_table(
        'yelp_user',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.String(22), unique=True, index=True),
        sa.Column('type', sa.String(50)),
        sa.Column('name', sa.String(200)),
        sa.Column('review_count', sa.Integer),
        sa.Column('average_stars', sa.Float(precision=6)),
        sa.Column('yelping_since', sa.String()),
        sa.Column('compliments', sa.String(2000)),
        sa.Column('votes', sa.String(200)),
        sa.Column('elite', sa.String(200))
        )

    op.create_table(
        'friendship',
        sa.Column('user1', sa.String(22), sa.ForeignKey('yelp_user.user_id'), nullable=False, index=True, primary_key=True),
        sa.Column('user2', sa.String(22), sa.ForeignKey('yelp_user.user_id'), nullable=False, index=True, primary_key=True)
        )



def downgrade():
    op.drop_table('friendship')
    op.drop_table('yelp_user')
