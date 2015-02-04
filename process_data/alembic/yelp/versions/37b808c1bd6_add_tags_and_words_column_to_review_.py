"""add tags and words column to review table

Revision ID: 37b808c1bd6
Revises: 20399e0831fe
Create Date: 2015-02-04 12:15:06.772850

"""

# revision identifiers, used by Alembic.
revision = '37b808c1bd6'
down_revision = '20399e0831fe'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('review', sa.Column('tags', sa.Text()))
    op.add_column('review', sa.Column('words', sa.Text()))


def downgrade():
    op.drop_column('review', 'tags')
    op.drop_column('review', 'words')
