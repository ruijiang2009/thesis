"""add category column to business

Revision ID: 658a3c50857
Revises: 24b3581aa6bf
Create Date: 2015-02-02 10:57:25.433811

"""

# revision identifiers, used by Alembic.
revision = '658a3c50857'
down_revision = '24b3581aa6bf'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('business', sa.Column('category', sa.String(500)))


def downgrade():
    op.drop_column('business', 'category')
