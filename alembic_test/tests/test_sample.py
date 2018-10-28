import datetime
import os
from alembic_test import Database

import pytest

alembic_config = os.path.join(os.path.dirname(__file__), "..", "..", "alembic.ini")

@pytest.fixture
def sqlite_db_url(tmpdir):
    return "sqlite:///" + str(tmpdir) + "/db.sqlite"

def test_simple_migration(sqlite_db_url):
    """ Verifies a simple migration using sqlite """
    db = Database(alembic_config, sqlite_db_url, "9ed275208514", "1eb46e5102a9")

    db.insert({
        "person": [{
            "id": 1,
            "name": "Tina Turner",
            "birthdate": datetime.date(1939, 11, 26),
        }]
    })

    db.migrate()

    person_table = db.get_table("person")
    conn = db.connection()

    entry = conn.execute(person_table.select()).next()

    assert entry.firstname == "Tina"
    assert entry.lastname == "Turner"


def test_auto_fill_fields(sqlite_db_url):
    db = Database(alembic_config, sqlite_db_url, "9ed275208514", "1eb46e5102a9")

    db.insert({
        "person": [{
            "name": "James Brown"
        }]
    })
