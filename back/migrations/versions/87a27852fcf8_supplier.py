"""supplier

Revision ID: 87a27852fcf8
Revises: f785968b2780
Create Date: 2025-03-13 23:07:14.222886

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87a27852fcf8'
down_revision = 'f785968b2780'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('receptions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('supplier', sa.String(length=100), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('receptions', schema=None) as batch_op:
        batch_op.drop_column('supplier')

    # ### end Alembic commands ###
