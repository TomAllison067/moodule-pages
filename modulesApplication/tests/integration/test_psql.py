import environ
from django.db import connections
from django.db.utils import OperationalError, ConnectionDoesNotExist
from django.test import TestCase, tag


@tag('integration')
class TestPostgres(TestCase):
    """
    Tests the psql connection.
    """

    def test_psql_connection(self):
        """
        Tests that a connection can be made to a psql database.
        If not, then it's probably something to do with the DATABASE_URL in the .env
        """
        env = environ.Env()
        url = env.get_value('DATABASE_URL').split(':')[0]
        self.assertIn(url, ["postgresql", "postgres", "pgsql", "psql"],
                      "You're not using a psql database.")
        try:
            db_conn = connections['default']
            c = db_conn.cursor()
        except (OperationalError, ConnectionDoesNotExist):
            connected = False
        else:
            connected = True
        self.assertTrue(connected, "A database connection has not been made.")
