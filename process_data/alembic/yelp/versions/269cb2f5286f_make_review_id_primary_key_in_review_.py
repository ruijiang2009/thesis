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
    op.execute("CREATE UNIQUE INDEX review_pkey ON review (review_id);")
    op.execute("ALTER TABLE review ADD CONSTRAINT pk_review PRIMARY KEY USING INDEX review_pkey;")


def downgrade():
    op.execute("ALTER TABLE review DROP CONSTRAINT pk_review;")
