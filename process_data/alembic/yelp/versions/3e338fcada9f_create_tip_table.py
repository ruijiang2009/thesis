"""create tip table

Revision ID: 3e338fcada9f
Revises: 2f202fcd3a4f
Create Date: 2015-01-28 17:28:50.372970

"""

# revision identifiers, used by Alembic.
revision = '3e338fcada9f'
down_revision = '2f202fcd3a4f'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

"""
data format:
{
    'type': 'tip',
    'text': (tip text),
    'business_id': (encrypted business id),
    'user_id': (encrypted user id),
    'date': (date, formatted like '2012-03-14'),
    'likes': (count)
}

example:
{
    "user_id": "Vefj29mjork1DLhALLNAsg",
    "text": "Great food, huge portions and a gift shop and showers.",
    "business_id": "JwUE5GmEO-sH1FuwJgKBlQ",
    "likes": 0,
    "date": "2012-05-16",
    "type": "tip"
}
"""

def upgrade():

    op.create_table(
        'tip',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('business_id', sa.String(50), nullable=False),
        sa.Column('user_id', sa.String(22), nullable=False),
        # sa.Column('business_id', sa.String(50), sa.ForeignKey('business.business_id'), primary_key=True, nullable=False),
        # sa.Column('user_id', sa.String(22), sa.ForeignKey('yelp_user.user_id'), primary_key=True, nullable=False),
        sa.Column('text', sa.Text()),
        sa.Column('likes', sa.Integer),
        sa.Column('date', sa.Date()),
        sa.Column('type', sa.String(3))
        )


def downgrade():
    op.drop_table('tip')
