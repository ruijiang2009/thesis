"""add index to some tables

Revision ID: 421b662d226b
Revises: 269cb2f5286f
Create Date: 2015-02-22 12:33:41.544248

"""

# revision identifiers, used by Alembic.
revision = '421b662d226b'
down_revision = '269cb2f5286f'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute("CREATE INDEX ix_user_topic50_user_id ON user_topic50 (user_id);")
    op.execute("CREATE INDEX ix_user_topic22_user_id ON user_topic22 (user_id);")
    op.execute("CREATE INDEX ix_business_category_business_id ON business_category (business_id);")
    op.execute("CREATE INDEX ix_business_topic22_business_id ON business_topic22 (business_id);")
    op.execute("CREATE INDEX ix_business_topic50_business_id ON business_topic50 (business_id);")
    op.execute("CREATE INDEX ix_user_business_user_id ON user_business (user_id);")
    op.execute("CREATE INDEX ix_user_business_business_id ON user_business (business_id);")
    op.execute("CREATE INDEX ix_user_vote_user_id ON user_vote (user_id)")

def downgrade():
    op.execute("DROP INDEX ix_user_topic50_user_id;")
    op.execute("DROP INDEX ix_user_topic22_user_id;")
    op.execute("DROP INDEX ix_business_category_business_id;")
    op.execute("DROP INDEX ix_business_topic22_business_id;")
    op.execute("DROP INDEX ix_business_topic50_business_id")
    op.execute("DROP INDEX ix_user_business_user_id")
    op.execute("DROP INDEX ix_user_business_business_id")
    op.execute("DROP INDEX ix_user_vote_user_id")