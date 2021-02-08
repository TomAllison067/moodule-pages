from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from modulesApplication.models import Module, Strands, Programme
from modulesApplication.tests.resources import expected

EXPECTED_MODULES = expected.EXPECTED_MODULES
EXPECTED_PROGRAMMES = expected.EXPECTED_PROGRAMMES  # The number of programmes in the exported sqlite3 table
EXPECTED_STRANDS = expected.EXPECTED_STRANDS  # How many strands are in the csv
IMPORT_SUCCESS_MESSAGE = "Imported {} modules, {} strands, {} degree programmes and {} option_rules successfully.\n"\
    .format(EXPECTED_MODULES, EXPECTED_STRANDS, EXPECTED_PROGRAMMES, expected.EXPECTED_OPTION_RULES)


class TestCustomCommands(TestCase):
    def test_import_test_data(self):
        """
        Tests that the custom import_test_data management command imports the correct number of data objects and
        prints a success message.
        :return:
        """
        output = StringIO()
        call_command('import_test_data', stdout=output)
        self.assertEqual(EXPECTED_MODULES, Module.objects.count())
        self.assertEqual(EXPECTED_STRANDS, Strands.objects.count())
        self.assertEqual(EXPECTED_PROGRAMMES, Programme.objects.count())
        self.assertEqual(IMPORT_SUCCESS_MESSAGE, output.getvalue())
