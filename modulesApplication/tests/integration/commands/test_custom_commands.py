from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from modulesApplication.models import *
from modulesApplication.tests.resources import expected


class TestCustomCommands(TestCase):
    def test_import_test_data(self):
        """
        Tests that the custom import_test_data management command imports the correct number of data objects and
        prints a success message.
        :return:
        """
        output = StringIO()
        call_command('import_test_data', stdout=output)
        self.assertEqual(expected.EXPECTED_MODULES, Module.objects.count())
        self.assertEqual(expected.EXPECTED_STRANDS, Strands.objects.count())
        self.assertEqual(expected.EXPECTED_PROGRAMMES, Programme.objects.count())
        self.assertEqual(expected.EXPECTED_OPTIONAL_MODULES, OptionalModule.objects.count())
        self.assertEqual(expected.EXPECTED_OPTION_RULES, OptionRule.objects.count())
        self.assertEqual(expected.EXPECTED_PEOPLE, People.objects.count())
        self.assertEqual(expected.EXPECTED_COURSE_LEADERS, CourseLeader.objects.count())
        self.assertEqual(expected.EXPECTED_MODULE_VARIANTS, ModuleVariant.objects.count())

