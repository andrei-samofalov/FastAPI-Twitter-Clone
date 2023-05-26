"""Added column created_at to Tweet

Revision ID: e7e342ea53f6
Revises: 4867f1ff6fe9
Create Date: 2023-05-26 11:06:33.261124

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'e7e342ea53f6'
down_revision = '4867f1ff6fe9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tweets', sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tweets', 'created_at')
    # ### end Alembic commands ###
