"""create review table

Revision ID: 24b3581aa6bf
Revises: 4e345ed4e1a1
Create Date: 2015-01-29 12:37:51.859389

"""

# revision identifiers, used by Alembic.
revision = '24b3581aa6bf'
down_revision = '4e345ed4e1a1'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


"""
format: 
{
    'type': 'review',
    'business_id': (encrypted business id),
    'user_id': (encrypted user id),
    'stars': (star rating, rounded to half-stars),
    'text': (review text),
    'date': (date, formatted like '2012-03-14'),
    'votes': {(vote type): (count)},
}

example:
{
    "votes":
        {
            "funny": 0,
            "useful": 2,
            "cool": 1
        },
    "user_id": "Xqd0DzHaiyRqVH3WRG7hzg",
    "review_id": "15SdjuK7DmYqUAj6rjGowg",
    "stars": 5,
    "date": "2007-05-17",
    "text": "dr. goldberg offers everything i look for in a general practitioner.  he's nice and easy to talk to without being patronizing; he's always on time in seeing his patients; he's affiliated with a top-notch hospital (nyu) which my parents have explained to me is very important in case something happens and you need surgery; and you can get referrals to see specialists without having to see him first.  really, what more do you need?  i'm sitting here trying to think of any complaints i have about him, but i'm really drawing a blank.",
    "type": "review",
    "business_id": "vcNAWiLM4dR7D2nwwJ7nCA"
}
"""

def upgrade():
    op.create_table(
        'review',
        sa.Column('review_id', sa.String(22), unique=True, index=True),
        sa.Column('user_id', sa.String(22), sa.ForeignKey('yelp_user.user_id')),
        sa.Column('business_id', sa.String(22), sa.ForeignKey('business.business_id')),
        sa.Column('date', sa.Date()),
        sa.Column('stars', sa.Integer),
        sa.Column('text', sa.Text()),
        sa.Column('type', sa.String(6))
    )

    op.create_table(
        'review_vote',
        sa.Column('review_id', sa.String(22), sa.ForeignKey('review.review_id'), primary_key=True),
        sa.Column('vote', sa.String(10), primary_key=True),
        sa.Column('number', sa.Integer)
    )



def downgrade():
    op.drop_table('review_vote')
    op.drop_table('review')
