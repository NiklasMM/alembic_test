from collections import defaultdict

from sqlalchemy.sql import sqltypes
from faker import Faker

fake = Faker()

faker_for_columntype = defaultdict(lambda: lambda: None)
faker_for_columntype.update({
    sqltypes.DATE: fake.date_object
})

def generate_fake_data(column_type):
    """ Generates fake data fitting to the columntype """
    return faker_for_columntype[type(column_type)]()
