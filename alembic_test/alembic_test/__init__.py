from alembic.config import Config
from alembic import command
from sqlalchemy import create_engine
from sqlalchemy.schema import MetaData

from alembic_test.helpers import generate_fake_data

class Database():

    def __init__(self, config, database_url, before_rev, after_rev):
        self.before_rev = before_rev
        self.after_rev = after_rev
        self.alembic_cfg = Config(config)
        self.alembic_cfg.set_main_option("sqlalchemy.url", database_url)
        command.upgrade(self.alembic_cfg, before_rev)
        self.engine = create_engine(self.alembic_cfg.get_main_option("sqlalchemy.url"))
        self.metadata = MetaData()
        self.metadata.reflect(bind=self.engine)


    def insert(self, data):
        connection = self.engine.connect()
        for table_name, table_data in data.items():

            table = self.metadata.tables[table_name]

            for entry in table_data:
                for column in table.c:
                    if not column.nullable and column.name not in entry:
                        entry[column.name.split(".")[-1]] = generate_fake_data(column.type)
                print(entry)
                connection.execute(
                    table.insert().values(**entry)
                )
        connection.close()

    def migrate(self):
        command.upgrade(self.alembic_cfg, self.after_rev)
        self.metadata = MetaData()
        self.metadata.reflect(bind=self.engine)

    def get_table(self, table_name):
        return self.metadata.tables[table_name]

    def connection(self):
        return self.engine.connect()
