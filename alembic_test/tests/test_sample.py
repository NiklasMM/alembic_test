import os
from alembic_test import Database

alembic_config = os.path.join(os.path.dirname(__file__), "..", "..", "alembic.ini")

def test_migration(tmpdir):

    url = "sqlite:///" + str(tmpdir) + "/db.sqlite"

    db = Database(alembic_config, url, "9ed275208514", "1eb46e5102a9")

    db.insert({
        "person": [{
            "id": 1,
            "name": "Tina Turner"
        }]
    })

    db.migrate()

    person_table = db.get_table("person")
    conn = db.connection()

    entry = conn.execute(person_table.select()).next()

    assert entry.firstname == "Tina"
    assert entry.lastname == "Turner"
