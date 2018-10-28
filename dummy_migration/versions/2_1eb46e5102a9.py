"""2

Revision ID: 1eb46e5102a9
Revises: 9ed275208514
Create Date: 2018-10-25 11:31:51.811472

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1eb46e5102a9'
down_revision = '9ed275208514'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('person', sa.Column('firstname', sa.Text(), nullable=True))
    op.add_column('person', sa.Column('lastname', sa.Text(), nullable=True))

    person_table = sa.sql.table(
        "person",
        sa.sql.column("id", sa.Integer),
        sa.sql.column("name", sa.Text),
        sa.sql.column("firstname", sa.Text),
        sa.sql.column("lastname", sa.Text),
    )

    connection = op.get_bind()

    for person in connection.execute(person_table.select()):
        name = person.name
        firstname, lastname = name.split()
        connection.execute(
            person_table.update()
            .values(firstname=firstname, lastname=lastname)
            .where(person_table.c.id == person.id)
        )

def downgrade():
    pass
