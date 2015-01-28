"""create business table

Revision ID: 213809085eee
Revises: 
Create Date: 2015-01-27 15:09:19.427758

"""

# revision identifiers, used by Alembic.
revision = '213809085eee'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'category',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(200), unique=True)
    )

    # op.create_table(
    #     'hour',
    #     sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    #     sa.Column('weekday', sa.String(10)),
    #     sa.Column('open', sa.Time()),
    #     sa.Column('close', sa.Time()),
    #     )

    op.create_table(
        'business',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('business_id', sa.String(50), nullable=False, unique=True),
        sa.Column('name', sa.Unicode(200), nullable=False),
        sa.Column('neighborhoods', sa.String(200)),
        sa.Column('full_address', sa.String(200)),
        sa.Column('city', sa.String(200)),
        sa.Column('state', sa.String(20)),
        sa.Column('latitude', sa.Float(precision=6)),
        sa.Column('longitude', sa.Float(precision=6)),
        sa.Column('stars', sa.Float(precision=1)),
        sa.Column('review_count', sa.Integer),
        sa.Column('open', sa.Boolean),
        sa.Column('hours', sa.String(500)),
        sa.Column('attributes', sa.Text()),
        sa.Column('type', sa.String(50)),
    )

    op.create_table(
        'business_category',
        sa.Column('category_id', sa.Integer, sa.ForeignKey('category.id'), nullable=False),
        sa.Column('business_id', sa.Integer, sa.ForeignKey('business.id'), nullable=False),
    )

    # op.create_table(
    #     'business_hour',
    #     sa.Column('business_id', sa.Integer, sa.ForeignKey('business.id'), nullable=False),
    #     sa.Column('hour_id', sa.Integer, sa.ForeignKey('hour.id'), nullable=False),
    # )


def downgrade():
    op.drop_table('business_category')
    # op.drop_table('business_hour')
    # op.drop_table('hour')
    op.drop_table('business')
    op.drop_table('category')
