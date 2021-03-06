"""empty message

Revision ID: c55dfcbd1750
Revises: 209731eedc6e
Create Date: 2018-03-03 16:05:58.122069

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c55dfcbd1750'
down_revision = '209731eedc6e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('note', sa.Column('last_updated', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('note', 'last_updated')
    # ### end Alembic commands ###
