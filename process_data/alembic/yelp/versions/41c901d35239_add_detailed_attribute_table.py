"""add detailed attribute table

Revision ID: 41c901d35239
Revises: 3e64c7b89113
Create Date: 2015-03-29 14:45:01.691724

"""

# revision identifiers, used by Alembic.
revision = '41c901d35239'
down_revision = '3e64c7b89113'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'detailed_attribute',
        sa.Column('id', sa.Integer, primary_key=True, unique=True, autoincrement=True),
        sa.Column('parent_id', sa.Integer, sa.ForeignKey('detailed_attribute.id'), nullable=True),
        sa.Column('name', sa.String))

    op.create_table(
        'business_detailed_attribute',
        sa.Column('business_id', sa.String(22), sa.ForeignKey('business.business_id'), primary_key=True),
        sa.Column('attribute_id', sa.Integer, sa.ForeignKey('detailed_attribute.id'), primary_key=True),
        sa.Column('stars', sa.Float(precision=1)),
        sa.Column('value', sa.String(100)))

    op.create_index('ix_business_detailed_attribute_business_id', 'business_detailed_attribute', ['business_id'])

def downgrade():
    op.drop_index('ix_business_detailed_attribute_business_id', 'business_detailed_attribute')
    op.drop_table('business_detailed_attribute')
    op.drop_table('detailed_attribute')
