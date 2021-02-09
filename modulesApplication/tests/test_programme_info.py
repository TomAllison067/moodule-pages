from django.test import TestCase

import modulesApplication.programmeInfo.factory as factory
from modulesApplication.models import Programme
from . import utils


class TestProgrammeInfo(TestCase):

    def setUp(self):
        utils.read_test_programmes()

    def test_programme_object(self):
        """Test that a new ProgrammeInfo is instantiated with the correct Programme object."""
        p = factory.get_programme_info(prog_code='1067')
        expected = Programme.objects.get(prog_code='1067')
        self.assertEqual(expected, p.programme)
