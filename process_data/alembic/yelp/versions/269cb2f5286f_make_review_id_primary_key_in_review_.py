"""make review_id primary key in review table

Revision ID: 269cb2f5286f
Revises: 4e99911ac3ed
Create Date: 2015-02-21 23:13:04.019984

"""

# revision identifiers, used by Alembic.
revision = '269cb2f5286f'
down_revision = '4e99911ac3ed'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute("ALTER TABLE review ADD CONSTRAINT review_pkey PRIMARY KEY USING INDEX ix_review_review_id;")


def downgrade():
    op.execute("ALTER TABLE review DROP CONSTRAINT review_pkey;")
