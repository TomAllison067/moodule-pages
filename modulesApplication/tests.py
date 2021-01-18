from django.test import TestCase
from django.db import connections


# Create your tests here.
class TestSQLiteDatabaseConnection(TestCase):
    """
    Tests that a connection can be made to a SQLite database.
    """
    def test_sqlite_database_connection(self):
        db_conn = connections['default']
        c = db_conn.cursor()
        self.assertIsNotNone(c, "The database cursor is None if there is no connection.")
