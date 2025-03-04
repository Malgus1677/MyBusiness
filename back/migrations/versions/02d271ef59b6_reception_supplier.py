"""reception supplier

Revision ID: 02d271ef59b6
Revises: 0776f2b50e16
Create Date: 2025-03-04 20:28:56.070426

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02d271ef59b6'
down_revision = '0776f2b50e16'
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
