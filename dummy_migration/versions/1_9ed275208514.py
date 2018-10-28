"""1

Revision ID: 9ed275208514
Revises:
Create Date: 2018-10-25 11:31:49.208522

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ed275208514'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('person',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.Text(), nullable=True),
        sa.Column('birthdate', sa.Date(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    pass
