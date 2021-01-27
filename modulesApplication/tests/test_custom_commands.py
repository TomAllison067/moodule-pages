import sys
import unittest
from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase

from modulesApplication.models import Module, Strands

MODULES_CSV_COUNT = 113  # The number of modules to be imported from the csv
STRANDS_CSV_COUNT = 40  # The number of strands to be imported from the csv - 43 minus 3 with non-existing modules = 40
IMPORT_SUCCESS_MESSAGE = "Imported {} modules and {} strands successfully.\n"\
    .format(MODULES_CSV_COUNT, STRANDS_CSV_COUNT)


class TestCustomCommands(TestCase):
    def test_import_test_data(self):
        """
        Tests that the custom import_test_data management command imports the correct number of data objects and
        prints a success message.
        :return:
        """
        output = StringIO()
        call_command('import_test_data', stdout=output)
        self.assertEqual(MODULES_CSV_COUNT, Module.objects.count())
        self.assertEqual(STRANDS_CSV_COUNT, Strands.objects.count())
        self.assertEqual(IMPORT_SUCCESS_MESSAGE, output.getvalue())
