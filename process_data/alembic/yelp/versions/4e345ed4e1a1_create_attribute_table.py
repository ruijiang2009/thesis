"""create attribute table

Revision ID: 4e345ed4e1a1
Revises: 3e338fcada9f
Create Date: 2015-01-29 11:21:41.000082

"""

# revision identifiers, used by Alembic.
revision = '4e345ed4e1a1'
down_revision = '3e338fcada9f'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'attribute',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, index=True, unique=True),
        sa.Column('name', sa.String(200), index=True, primary_key=True),
        sa.Column('value', sa.String(2000), index=True, primary_key=True)
    )

    # alter attribute table's primary key
    op.drop_constraint('attribute_pkey', 'attribute', 'primary')
    op.create_primary_key('attribute_pkey', 'attribute', ["name", "value"])

    op.create_table(
        'business_attribute',
        sa.Column('attribute_id', sa.Integer, sa.ForeignKey('attribute.id'), nullable=False, index=True, primary_key=True),
        sa.Column('business_bid', sa.String(22), sa.ForeignKey('business.business_id'), nullable=False, index=True, primary_key=True),
        sa.Column('business_id', sa.Integer, sa.ForeignKey('business.id'), nullable=False, index=True)
    )


def downgrade():
    op.drop_table('business_attribute')
    op.drop_table('attribute')
